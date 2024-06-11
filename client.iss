#define MyAppName "HLS Video Downloader Client"
#define MyAppPublisher "CSSNR"
#define MyAppURL "https://github.com/cssnr/hls-downloader-client"
#define MyAppExeName "client.exe"
#define MyAppFolder "org.cssnr.hls.downloader"
#ifndef MyAppVersion
#define MyAppVersion "0.0.1"
#endif

[Setup]
AppId={{451A067A-06E7-4979-92EB-745C1E14AD5F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
Compression=lzma
DefaultDirName={localappdata}\{#MyAppFolder}
;DisableDirPage=yes
DisableProgramGroupPage=yes
DefaultGroupName={#MyAppName}
InfoBeforeFile=INSTALL.md
OutputBaseFilename=install-win
OutputDir=out
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
SetupIconFile=src\favicon.ico
SolidCompression=yes
UninstallDisplayIcon={app}\{#MyAppExeName}
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
;Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\client\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
Source: "dist\manifest-chrome.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\manifest-firefox.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\ffmpeg.exe"; DestDir: "{app}"; Flags: ignoreversion

[Registry]
Root: HKCU; Subkey: "Software\Google\Chrome\NativeMessagingHosts\{#MyAppFolder}"; ValueType: string; ValueData: "{app}\manifest-chrome.json"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Chromium\NativeMessagingHosts\{#MyAppFolder}"; ValueType: string; ValueData: "{app}\manifest-chrome.json"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Microsoft\Edge\NativeMessagingHosts\{#MyAppFolder}"; ValueType: string; ValueData: "{app}\manifest-chrome.json"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Mozilla\NativeMessagingHosts\{#MyAppFolder}"; ValueType: string; ValueData: "{app}\manifest-firefox.json"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Waterfox\NativeMessagingHosts\{#MyAppFolder}"; ValueType: string; ValueData: "{app}\manifest-firefox.json"; Flags: uninsdeletekey

[UninstallDelete]
Type: files; Name: "{app}\log.txt"
