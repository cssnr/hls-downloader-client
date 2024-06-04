#!/usr/bin/env bash

set -e

PKG_NAME="hls-downloader-client"
APP_NAME="org.cssnr.hls.downloader"
SOURCE="dist"
VERSION="0.1"

if [ "${GITHUB_EVENT_NAME}" == "release" ];then
    VERSION="${GITHUB_REF_NAME}"
fi
echo "Building version: ${VERSION}"

PACKAGE="${PKG_NAME}_${VERSION}"

echo "SOURCE: ${SOURCE}"
ls -lah "${SOURCE}"
echo "dest: ${PACKAGE}"

chrome="${PACKAGE}/etc/opt/chrome/native-messaging-hosts"
chromium="${PACKAGE}/etc/chromium/native-messaging-hosts"
firefox="${PACKAGE}/usr/lib/mozilla/native-messaging-hosts"

mkdir -p "${PACKAGE}/DEBIAN"
mkdir -p "${PACKAGE}/opt/${APP_NAME}"
mkdir -p "${chrome}"
mkdir -p "${chromium}"
mkdir -p "${firefox}"

cp -f "src/client.py" "${PACKAGE}/opt/${APP_NAME}/client.py"
chmod +x "${PACKAGE}/opt/${APP_NAME}/client.py"
cp -f "dist/ffmpeg" "${PACKAGE}/opt/${APP_NAME}/ffmpeg"
chmod +x "${PACKAGE}/opt/${APP_NAME}/ffmpeg"
touch "${PACKAGE}/opt/${APP_NAME}/log.txt"
chmod g+w "${PACKAGE}/opt/${APP_NAME}/log.txt"

cp -f "${SOURCE}/manifest-chrome.json" "${chrome}/${APP_NAME}.json"
cp -f "${SOURCE}/manifest-chrome.json" "${chromium}/${APP_NAME}.json"
cp -f "${SOURCE}/manifest-firefox.json" "${firefox}/${APP_NAME}.json"

cat <<-EOF > "${PACKAGE}/DEBIAN/control"
Package: ${PKG_NAME}
Version: ${VERSION}
Section: base
Priority: optional
Architecture: i386
Maintainer: CSSNR
Description:  CSSNR Python Native Messaging
 https://github.com/smashedr/python-native-messaging
EOF

echo "Debian: ${PACKAGE}/DEBIAN/control"
cat "${PACKAGE}/DEBIAN/control"

echo "Building: ${PACKAGE}"
dpkg-deb --build "${PACKAGE}"

mkdir out
mv "${PACKAGE}.deb" "out/install-linux.deb"
