#!/usr/bin/env bash

set -e

APP_NAME="org.cssnr.hls.downloader"
DEST="dist"
FFMPEG_ZIP="https://evermeet.cx/ffmpeg/ffmpeg-6.1.1.zip"

echo "DEST: ${DEST}"
ls -lah "${DEST}"

touch "${DEST}/log.txt"

mkdir "${DEST}/firefox"
mkdir "${DEST}/chrome"

mv "${DEST}/manifest-firefox.json" "${DEST}/firefox/${APP_NAME}.json"
mv "${DEST}/manifest-chrome.json" "${DEST}/chrome/${APP_NAME}.json"

curl "${FFMPEG_ZIP}" -o "${DEST}/ffmpeg.zip"
unzip "${DEST}/ffmpeg.zip" -d "${DEST}"

echo "debug"
pwd
ls -lah

packagesbuild client.pkgproj
mkdir out
mv "${DEST}/hls-downloader-client.pkg" "out/install-macos.pkg"
