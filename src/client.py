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
from typing import Any, Dict, List, Union
from urllib.parse import urlparse

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


def read_message() -> Dict[str, Any]:
    length = sys.stdin.buffer.read(4)
    if len(length) == 0:
        logger.warning('Message length is 0')
        sys.exit(0)
    message_length = struct.unpack('I', length)[0]
    data = sys.stdin.buffer.read(message_length).decode('utf-8')
    return json.loads(data)


def send_response(data: Dict[str, Any], success: bool = True) -> None:
    data['success'] = success
    text = json.dumps(data)
    logger.debug('response: %s', text)
    length = struct.pack('@I', len(text))
    msg = {'length': length, 'content': text}
    sys.stdout.buffer.write(msg['length'])
    sys.stdout.write(msg['content'])
    sys.stdout.flush()


def run(args: Union[List[str], str]) -> subprocess.CompletedProcess:
    result = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        logger.error('Error: %s', result.stderr)
    logger.debug('result.returncode: %s', result.returncode)
    return result


def version_check() -> None:
    logger.debug('version_check')
    with open('version.txt', 'r') as file:
        current_version = file.read().strip()
    send_response({
        'current_version': current_version,
    })


def open_folder(file: str) -> None:
    logger.debug('Opening File: %s', file)
    system = platform.system()
    if system == 'Windows':
        run(f'explorer /select,"{file}"')
    elif system == 'Linux':
        run(['xdg-open', os.path.dirname(file)])
    elif system == 'Darwin':
        run(['open', '-R', file])
    else:
        logger.warning('Unsupported System: %s', system)
        return send_response({'message': 'Unable to open on this system.'}, False)

    send_response({'message': 'opened'})


def download(message: Dict[str, Any]) -> None:
    logger.debug('----- download: BEGIN')
    url = message['download']
    logger.info('Downloading URL: %s', url)
    parsed = urlparse(url)
    name = os.path.basename(parsed.path)
    logger.debug('name: %s', name)

    directory = os.path.join(Path.home(), 'Downloads')
    if not os.path.exists(directory):
        logger.info('Created Downloads Directory: %s', directory)
        os.makedirs(directory)

    filename, _ = os.path.splitext(name)
    fullname = filename + '.mp4'
    filepath = os.path.join(directory, fullname)
    logger.debug('filepath: %s', filepath)
    if os.path.exists(filepath):
        logger.debug('filepath exists, adding random')
        rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        logger.debug('rand: %s', rand)
        fullname = filename + '_' + rand + '.mp4'
        filepath = os.path.join(directory, fullname)
        logger.debug('filepath: %s', filepath)

    logger.info('Destination File Path: %s', filepath)
    ffmpeg = shutil.which('ffmpeg')
    if not ffmpeg:
        ffmpeg = os.path.join(os.getcwd(), 'ffmpeg')
    args = [ffmpeg, '-i', url]
    if 'extra' in message and message['extra']:
        args.extend(['-i', message['extra']])
    args.extend(['-c', 'copy', '-bsf:a', 'aac_adtstoasc', filepath])
    logger.debug('args: %s', args)
    result = run(args)
    logger.debug('----- download: END')
    if result.returncode != 0:
        send_response({
            'message': result.stderr.decode().splitlines()[-1],
        }, False)
    else:
        send_response({
            'message': 'Download Finished.',
            'path': filepath,
        })


def ytdlp(message: Dict[str, Any]) -> None:
    url = message['ytdlp']
    logger.info('Downloading yt-dlp: %s', url)
    directory = os.path.join(Path.home(), 'Downloads')
    if not os.path.exists(directory):
        logger.info('Created Downloads Directory: %s', directory)
        os.makedirs(directory)
    yt_dlp = shutil.which('yt-dlp')
    logger.debug('yt_dlp: %s', yt_dlp)

    logger.info('Destination Directory: %s', directory)
    args = [yt_dlp, '-P', directory, url]
    logger.debug('args: %s', args)
    result = run(args)
    if result.returncode != 0:
        return send_response({
            'message': result.stderr.decode().splitlines()[-1],
        }, False)

    stdout = result.stdout.decode('utf-8').split('\n')
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
        send_response({'message': 'Unable to Parse Output File.'}, False)


try:
    message = read_message()
    logger.debug('message: %s', message)
    if 'version' in message:
        version_check()
    elif 'open' in message:
        open_folder(message['open'])
    elif 'download' in message:
        download(message)
    elif 'ytdlp' in message:
        ytdlp(message)
    else:
        send_response({'message': 'Host Client Working.'})

except Exception as error:
    logger.exception(error)
    send_response({'message': str(error)}, False)
