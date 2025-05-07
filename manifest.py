import json
import os
import platform
from typing import Dict, List, Union


# Configuration

data: Dict[str, Union[str, List[str]]] = {
    "name": "org.cssnr.hls.downloader",
    "description": "HLS Video Downloader Client",
    "type": "stdio",
}
firefox_ids: List[str] = [
    "hls-video-downloader@cssnr.com",
]
chrome_ids: List[str] = [
    "mpmiiaolodhanoalpjncddpmnkbjicbo",
]

output_dir = "dist"
name_firefox = "manifest-firefox.json"
name_chrome = "manifest-chrome.json"

system = platform.system()
if system == "Windows":
    client_path = "client.exe"
elif system == "Linux":
    client_path = f'/opt/{data["name"]}/client.py'
elif system == "Darwin":
    client_path = f'/opt/{data["name"]}/client'
else:
    raise ValueError(f"Unsupported System: {system}")

# Script

print(f"Using client path: {client_path}")
data["path"] = client_path

manifest_firefox = data.copy()
manifest_firefox["allowed_extensions"] = firefox_ids

manifest_chrome = data.copy()
manifest_chrome["allowed_origins"] = []
for _id in chrome_ids:
    manifest_chrome["allowed_origins"].append(f"chrome-extension://{_id}/")  # type: ignore

output_firefox = os.path.join(output_dir, name_firefox)
output_chrome = os.path.join(output_dir, name_chrome)

firefox = json.dumps(manifest_firefox, ensure_ascii=False, indent=2)
chrome = json.dumps(manifest_chrome, ensure_ascii=False, indent=2)

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

print(f"Writing Firefox to: {output_firefox}\n{firefox}")
with open(output_firefox, "w", encoding="utf-8") as f:
    f.write(firefox)

print(f"Writing Chrome to: {output_chrome}\n{chrome}")
with open(output_chrome, "w", encoding="utf-8") as f:
    f.write(chrome)
