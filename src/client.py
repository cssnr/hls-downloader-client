#!/usr/bin/env python3

import json
import os
import logging
import platform
import random
import string
import shutil
import struct
import sys
import subprocess
from logging.handlers import RotatingFileHandler
from pathlib import Path

logging.basicConfig(
    handlers=[RotatingFileHandler(
        filename='log.txt',
        maxBytes=1_000_000,
        backupCount=2,
    )],
    format='%(asctime)s %(name)s %(levelname)s - %(message)s',
    level=logging.getLevelName('DEBUG'),
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger('client')


def read_message():
    length = sys.stdin.buffer.read(4)
    if len(length) == 0:
        logger.warning('Message length is 0')
        sys.exit(0)
    message_length = struct.unpack('I', length)[0]
    data = sys.stdin.buffer.read(message_length).decode('utf-8')
    return json.loads(data)


def send_response(data, success=True):
    data['success'] = success
    text = json.dumps(data)
    length = struct.pack('@I', len(text))
    msg = {'length': length, 'content': text}
    sys.stdout.buffer.write(msg['length'])
    sys.stdout.write(msg['content'])
    sys.stdout.flush()


def download(url):
    logger.info(f'Downloading URL: {url}')
    name = os.path.basename(url)
    logger.debug(f'name: {name}')

    directory = os.path.join(Path.home(), 'Downloads')
    if not os.path.exists(directory):
        logger.info(f'Created Downloads Directory: {directory}')
        os.makedirs(directory)

    filename, _ = os.path.splitext(name)
    fullname = filename + '.mp4'
    filepath = os.path.join(directory, fullname)
    logger.debug(f'filepath: {filepath}')
    if os.path.exists(filepath):
        logger.debug('filepath exists, adding random')
        rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        logger.debug(f'rand: {rand}')
        fullname = filename + '_' + rand + '.mp4'
        filepath = os.path.join(directory, fullname)
        logger.debug(f'filepath: {filepath}')

    logger.info(f'Destination File Path: {filepath}')
    ffmpeg = shutil.which('ffmpeg')
    if not ffmpeg:
        ffmpeg = os.path.join(os.getcwd(), 'ffmpeg')
    args = [ffmpeg, '-i', url, '-c', 'copy', '-bsf:a', 'aac_adtstoasc', filepath]
    logger.debug(f'args: {args}')
    ffmpeg_result = subprocess.run(args)
    logger.debug(f'ffmpeg_result: {ffmpeg_result}')
    return filepath


def open_folder(file):
    logger.debug(f'Opening File: {file}')
    system = platform.system()
    if system == 'Windows':
        open_result = subprocess.run(f'explorer /select,"{file}"')
    elif system == 'Linux':
        open_result = subprocess.run(['xdg-open', os.path.dirname(file)])
    elif system == 'Darwin':
        open_result = subprocess.run(['open', '-R', file])
    else:
        logger.info(f'Unsupported System: {system}')
        return
    logger.debug(f'open_result: {open_result}')


try:
    message = read_message()
    logger.debug(f'message: {message}')
    if 'download' in message:
        logger.debug('----- download: BEGIN')
        path = download(message['download'])
        response = {
            'message': 'Download Finished.',
            'path': path,
        }
        logger.debug('----- download: END')
        send_response(response)
    elif 'open' in message:
        open_folder(message['open'])
        send_response({'message': 'opened'})
    else:
        send_response({'message': 'Host Client Working.'})

except Exception as error:
    logger.exception(error)
    send_response({'message': str(error)}, False)
