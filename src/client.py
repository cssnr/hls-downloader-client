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
        backupCount=1,
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
    logger.debug(f'response: {text}')
    length = struct.pack('@I', len(text))
    msg = {'length': length, 'content': text}
    sys.stdout.buffer.write(msg['length'])
    sys.stdout.write(msg['content'])
    sys.stdout.flush()


def run(args):
    result = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        logger.debug(f'Error: {result.stderr}')
    return result


def open_folder(file):
    logger.debug(f'Opening File: {file}')
    system = platform.system()
    if system == 'Windows':
        result = run(f'explorer /select,"{file}"')
    elif system == 'Linux':
        result = run(['xdg-open', os.path.dirname(file)])
    elif system == 'Darwin':
        result = run(['open', '-R', file])
    else:
        logger.info(f'Unsupported System: {system}')
        send_response({'message': 'Unable to open on this system.'}, False)
        return
    logger.debug(f'returncode: {result.returncode}')
    send_response({'message': 'opened'})


def download(message):
    logger.debug('----- download: BEGIN')
    url = message['download']
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
    args = [ffmpeg, '-i', url]
    if 'extra' in message and message['extra']:
        args.extend(['-i', message['extra']])
    args.extend(['-c', 'copy', '-bsf:a', 'aac_adtstoasc', filepath])
    logger.debug(f'args: {args}')
    result = run(args)
    logger.debug(f'returncode: {result.returncode}')
    response = {
        'message': 'Download Finished.',
        'path': filepath,
    }
    logger.debug('----- download: END')
    send_response(response)


def ytdlp(message):
    url = message['ytdlp']
    logger.info(f'Downloading yt-dlp: {url}')
    directory = os.path.join(Path.home(), 'Downloads')
    if not os.path.exists(directory):
        logger.info(f'Created Downloads Directory: {directory}')
        os.makedirs(directory)
    yt_dlp = shutil.which('yt-dlp')
    logger.debug(f'yt_dlp: {yt_dlp}')

    logger.info(f'Destination Directory: {directory}')
    args = [yt_dlp, '-P', directory, url]
    logger.debug(f'args: {args}')
    result = run(args)
    stdout = result.stdout.decode('utf-8').split('\n')
    logger.debug(f'++returncode: {result.returncode}')
    logger.debug(f'--stdout: {stdout}')
    dest = None
    for out in reversed(stdout):
        if out.startswith('[Merger] Merging formats into '):
            dest = out.replace('[Merger] Merging formats into ', '', 1)
        if out.startswith('[download] ') and out.endswith(' has already been downloaded'):
            dest = out.replace('[download] ', '').replace(' has already been downloaded', '')

    if dest:
        send_response({
            'message': 'Download Finished.',
            'path': dest.strip('"'),
        })
    else:
        send_response({'message': 'Error Processing Download.'}, False)


try:
    message = read_message()
    logger.debug(f'message: {message}')
    if 'download' in message:
        download(message)
    elif 'open' in message:
        open_folder(message['open'])
    elif 'ytdlp' in message:
        ytdlp(message)
    else:
        send_response({'message': 'Host Client Working.'})

except Exception as error:
    logger.exception(error)
    send_response({'message': str(error)}, False)
