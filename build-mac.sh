#!/usr/bin/env bash

set -e

APP_NAME="org.cssnr.hls.downloader"
DEST="dist"
VERSION="0.0.1"

if [ "${GITHUB_EVENT_NAME}" == "release" ];then
    VERSION="${GITHUB_REF_NAME}"
fi
echo "Building version: ${VERSION}"

echo "DEST: ${DEST}"
ls -lah "${DEST}"

touch "${DEST}/log.txt"

mkdir -p "${DEST}/firefox"
mkdir -p "${DEST}/chrome"

cp -f "${DEST}/manifest-firefox.json" "${DEST}/firefox/${APP_NAME}.json"
cp -f "${DEST}/manifest-chrome.json" "${DEST}/chrome/${APP_NAME}.json"

packagesbuild client.pkgproj --package-version "${VERSION}"
mkdir -p out
mv "build/hls-downloader-client.pkg" "out/install-macos.pkg"
