# HLS Video Downloader Client

HLS Video Downloader Native Messaging client for Windows, Linux and macOS.

## Browsers

Tested and working in the following browsers:

- Firefox
- Waterfox
- Edge
- Chrome
- Chromium
- Brave
- Opera
- Vivaldi
- Ghost

## Installing

Download and run the installer for your operating system from the latest 
[release](https://github.com/smashedr/python-native-messaging/releases/latest).

## Building

### Windows

Build the App:
```shell
python -m pip install pyinstaller
pyinstaller --noconfirm client.spec
python manifest.py
```

Create the Installer:
```shell
iscc.exe install-win.iss
```

### Linux

```shell
python manifest.py
bash install-linux.sh
```

### MacOS Install

> [!NOTE]  
> macOS must be manually installed until an automated installer process is created.

```shell
python manifest.py
```

Manifest files must be renamed to: `org.cssnr.hls.downloader.json`

Manifest key `path` must be set to the absolute path to the `client.py` location.

Manifest files must be placed in specific directories:

- Firefox: `~/Library/Application Support/Mozilla/NativeMessagingHosts`
- Chromium: `~/Library/Application Support/Chromium/NativeMessagingHosts`
- Google Chrome: `~/Library/Application Support/Google/Chrome/NativeMessagingHosts`

If the `client` location is not writable by the user, a writable `log.txt`
must be created at that location due to the current logging configuration in the [client.py](src%2Fclient.py).

The `client.py` must be executable by the user with Python installed and working.
