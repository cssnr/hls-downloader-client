[![GitHub Release](https://img.shields.io/github/v/release/cssnr/hls-downloader-client?logo=github)](https://github.com/cssnr/hls-downloader-client/releases/latest)
[![GitHub Downloads](https://img.shields.io/github/downloads/cssnr/hls-downloader-client/total?logo=rolldown&logoColor=white)](https://github.com/cssnr/hls-downloader-client/releases)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=cssnr_hls-downloader-client&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=cssnr_hls-downloader-client)
[![Workflow Build](https://img.shields.io/github/actions/workflow/status/cssnr/hls-downloader-client/build.yaml?logo=testcafe&logoColor=white&label=build)](https://github.com/cssnr/hls-downloader-client/actions/workflows/build.yaml)
[![Workflow Lint](https://img.shields.io/github/actions/workflow/status/cssnr/hls-downloader-client/lint.yaml?logo=testcafe&logoColor=white&label=lint)](https://github.com/cssnr/hls-downloader-client/actions/workflows/lint.yaml)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/cssnr/hls-downloader-client?logo=listenhub&label=updated)](https://github.com/cssnr/hls-downloader-client/pulse)
[![GitHub Repo Size](https://img.shields.io/github/repo-size/cssnr/hls-downloader-client?logo=buffer&label=repo%20size)](https://github.com/cssnr/hls-downloader-client?tab=readme-ov-file#readme)
[![GitHub Top Language](https://img.shields.io/github/languages/top/cssnr/hls-downloader-client?logo=devbox)](https://github.com/cssnr/hls-downloader-client?tab=readme-ov-file#readme)
[![GitHub Contributors](https://img.shields.io/github/contributors-anon/cssnr/hls-downloader-client?logo=southwestairlines)](https://github.com/cssnr/hls-downloader-client/graphs/contributors)
[![GitHub Issues](https://img.shields.io/github/issues/cssnr/hls-downloader-client?logo=codeforces&logoColor=white)](https://github.com/cssnr/hls-downloader-client/issues)
[![GitHub Discussions](https://img.shields.io/github/discussions/cssnr/hls-downloader-client?logo=theconversation)](https://github.com/cssnr/hls-downloader-client/discussions)
[![GitHub Forks](https://img.shields.io/github/forks/cssnr/hls-downloader-client?style=flat&logo=forgejo&logoColor=white)](https://github.com/cssnr/hls-downloader-client/forks)
[![GitHub Repo Stars](https://img.shields.io/github/stars/cssnr/hls-downloader-client?style=flat&logo=gleam&logoColor=white)](https://github.com/cssnr/hls-downloader-client/stargazers)
[![GitHub Org Stars](https://img.shields.io/github/stars/cssnr?style=flat&logo=apachespark&logoColor=white&label=org%20stars)](https://cssnr.github.io/)
[![Discord](https://img.shields.io/discord/899171661457293343?logo=discord&logoColor=white&label=discord&color=7289da)](https://discord.gg/wXy6m2X8wY)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-72a5f2?logo=kofi&label=support)](https://ko-fi.com/cssnr)

# HLS Video Downloader Client

- [Browsers](#Browsers)
- [Installing](#Installing)
- [Building](#Building)
- [Support](#Support)
- [Contributing](#Contributing)

HLS Video Downloader Native Messaging Client for Windows, Linux and macOS.

[![Chrome](https://raw.githubusercontent.com/smashedr/repo-images/refs/heads/master/os/windows48.png)](https://github.com/cssnr/hls-downloader-client/releases/latest/download/install-win.exe)
[![Firefox](https://raw.githubusercontent.com/smashedr/repo-images/refs/heads/master/os/linux48.png)](https://github.com/cssnr/hls-downloader-client/releases/latest/download/install-linux.deb)
[![Edge](https://raw.githubusercontent.com/smashedr/repo-images/refs/heads/master/os/macos48.png)](https://github.com/cssnr/hls-downloader-client/releases/latest/download/install-macos.pkg)

- Windows: [install-win.exe](https://github.com/cssnr/hls-downloader-client/releases/latest/download/install-win.exe)
- Linux: [install-linux.deb](https://github.com/cssnr/hls-downloader-client/releases/latest/download/install-linux.deb)
- macOS: [install-macos.pkg](https://github.com/cssnr/hls-downloader-client/releases/latest/download/install-macos.pkg)

> [!NOTE]  
> On macOS you need to Ctrl+Click or Right-Click the .pkg and then choose Open to install.

This is the client for this Web Extension: https://github.com/cssnr/hls-video-downloader

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
[release](https://github.com/cssnr/hls-downloader-client/releases/latest).

## Running From Source

This can be run directly from the `client.py` source file. To do this, all the configuration must be in place and
Python installed. You can either run the installer first or manually configure the app (see [Additional Info](#additional-information)).

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
For this purpose, I created an [Installers](#installing) for each OS.
For more details, see the [Additional Info](#additional-information) section below.

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
python -m pip install -U pip
python -m pip install --group build
run pyinstaller
run manifest
```

Create the Installer:

```shell
iscc.exe client.iss
```

### Linux

Note: FFmpeg must be placed in `dist/ffmpeg`

```shell
#python -m pip install -U pip
#python -m pip install --group build
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
python -m pip install -U pip
python -m pip install --group build
run pyinstaller
run manifest
```

Create the Package:

```shell
bash build-mac.sh
```

### Additional Information

Windows requires corresponding registry entries for the manifest files (see location links below).

Windows and macOS requires packaging the app with `pyinstaller` to bundle python.

Manifest files must be renamed to `org.cssnr.hls.downloader.json` on Linux and macOS.

Manifest key `path` must be set to the absolute path to the `client` location.

Manifest files must be placed in specific directories:

- Firefox: https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_manifests#manifest_location
- Chrome: https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging#native-messaging-host-location

The `client` location must be writable by the user and a writable `log.txt`
must be present in that location due to the current logging configuration in the [client.py](src/client.py).

The `client.py` must be executable by the user with Python installed and working.

# Support

If you run into any issues or need help getting started, please do one of the following:

- Report an Issue: <https://github.com/cssnr/hls-downloader-client/issues>
- Q&A Discussion: <https://github.com/cssnr/hls-downloader-client/discussions/categories/q-a>
- Request a Feature: <https://github.com/cssnr/hls-downloader-client/issues/new?template=1-feature.yaml>
- Chat with us on Discord: <https://discord.gg/wXy6m2X8wY>

[![Features](https://img.shields.io/badge/features-brightgreen?style=for-the-badge&logo=rocket&logoColor=white)](https://github.com/cssnr/hls-downloader-client/issues/new?template=1-feature.yaml)
[![Issues](https://img.shields.io/badge/issues-red?style=for-the-badge&logo=southwestairlines&logoColor=white)](https://github.com/cssnr/hls-downloader-client/issues)
[![Discussions](https://img.shields.io/badge/discussions-blue?style=for-the-badge&logo=theconversation&logoColor=white)](https://github.com/cssnr/hls-downloader-client/discussions)
[![Discord](https://img.shields.io/badge/discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/wXy6m2X8wY)

# Contributing

If you would like to submit a PR, please review the [CONTRIBUTING.md](#contributing-ov-file).

Please consider making a donation to support the development of this project
and [additional](https://cssnr.com/) open source projects.

[![Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cssnr)

For a full list of current projects visit: [https://cssnr.github.io/](https://cssnr.github.io/)
