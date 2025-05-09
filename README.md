[![GitHub Downloads](https://img.shields.io/github/downloads/cssnr/hls-downloader-client/total?logo=github)](https://github.com/cssnr/hls-downloader-client/releases/latest)
[![GitHub Release](https://img.shields.io/github/v/release/cssnr/hls-downloader-client?logo=github)](https://github.com/cssnr/hls-downloader-client/releases/latest)
[![Workflow Build](https://img.shields.io/github/actions/workflow/status/cssnr/hls-downloader-client/build.yaml?logo=github&label=build)](https://github.com/cssnr/hls-downloader-client/actions/workflows/build.yaml)
[![Workflow Lint](https://img.shields.io/github/actions/workflow/status/cssnr/hls-downloader-client/lint.yaml?logo=github&label=lint)](https://github.com/cssnr/hls-downloader-client/actions/workflows/lint.yaml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=cssnr_hls-downloader-client&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=cssnr_hls-downloader-client)

# HLS Video Downloader Client

HLS Video Downloader Native Messaging Client for Windows, Linux and macOS.

-   Windows: [install-win.exe](https://github.com/cssnr/hls-downloader-client/releases/latest/download/install-win.exe)
-   Linux: [install-linux.deb](https://github.com/cssnr/hls-downloader-client/releases/latest/download/install-linux.deb)
-   macOS: [install-macos.pkg](https://github.com/cssnr/hls-downloader-client/releases/latest/download/install-macos.pkg)

> [!NOTE]  
> On macOS you need to Ctrl+Click or Right-Click the .pkg and then choose Open to install.

This is the client for this Web Extension: https://github.com/cssnr/hls-video-downloader

## Browsers

Tested and working in the following browsers:

-   Firefox
-   Waterfox
-   Edge
-   Chrome
-   Chromium
-   Brave
-   Opera
-   Vivaldi
-   Ghost

## Installing

Download and run the installer for your operating system from the latest
[release](https://github.com/cssnr/hls-downloader-client/releases/latest).

## Running From Source

This can be run directly from the `client.py` source file. To do this, all the configuration must be in place and
Python installed. You can either run the installer first or manually configure the app (see [More Info](#More-Info)).

Then, place the [client.bat](assets/client.bat) (Windows) or the [client.sh](assets/client.sh)
(Linux/macOS) into the installation directory and update it to point to your source `client.py` file.
Note: You may need to place an `ffmpeg` executable in the `src` directory on some operating systems.

```python
ffmpeg = shutil.which("ffmpeg")
if not ffmpeg:
    ffmpeg = os.path.join(os.getcwd(), "ffmpeg")
```

Lastly, update the installed manifest file for your browser to point to the client.bat or client.sh.

This information is only here for advanced users.
Different operating systems and browsers have different requirements.
For this purpose, I created an [Installers](#Installing) for each OS.
For more details, see the [More Info](#More-Info) section below.

## Building

This guide is for reference only. The release builds are built with GitHub Actions.
See [build.yaml](.github/workflows/build.yaml) for more details.

### Windows

> [!NOTE]  
> The Windows installer uses [Inno Setup](https://jrsoftware.org/isinfo.php)
> which must be manually installed.

Note: FFmpeg must be placed in `dist/ffmpeg.exe`

Build the App:

```shell
python -m pip install -r requirements.txt
pyinstaller --noconfirm client.spec
python manifest.py
```

Create the Installer:

```shell
iscc.exe client.iss
```

### Linux

Note: FFmpeg must be placed in `dist/ffmpeg`

```shell
#python -m pip install -r requirements.txt
python manifest.py
bash build-linux.sh
```

### MacOS

> [!NOTE]  
> The macOS installer uses [Packages](http://s.sudre.free.fr/Software/Packages/about.html)
> which must be manually installed.

Note: FFmpeg must be placed in `dist/ffmpeg`

Build the App:

```shell
python -m pip install -r requirements.txt
pyinstaller --noconfirm client.spec
python manifest.py
```

Create the Package:

```shell
bash build-mac.sh
```

## More Info

Windows requires corresponding registry entries for the manifest files (see location links below).

Windows and macOS requires packaging the app with `pyinstaller` to bundle python.

Manifest files must be renamed to `org.cssnr.hls.downloader.json` on Linux and macOS.

Manifest key `path` must be set to the absolute path to the `client` location.

Manifest files must be placed in specific directories:

-   Firefox: https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_manifests#manifest_location
-   Chrome: https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging#native-messaging-host-location

The `client` location must be writable by the user and a writable `log.txt`
must be present in that location due to the current logging configuration in the [client.py](src/client.py).

The `client.py` must be executable by the user with Python installed and working.
