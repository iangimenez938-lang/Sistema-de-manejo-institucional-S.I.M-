import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib import error, request

APP_NAME = "CalculadoraExpo"


def load_app_version_from_manifest():
    base_dir = Path(__file__).resolve().parent
    manifest_path = base_dir / "version.json"
    if not manifest_path.exists():
        return "1.0.0"

    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return "1.0.0"

    if not isinstance(payload, dict):
        return "1.0.0"

    version = payload.get("version")
    return str(version) if version else "1.0.0"


APP_VERSION = load_app_version_from_manifest()

DEFAULT_REMOTE_UPDATE_URL = (
    "https://raw.githubusercontent.com/your-user/your-repo/main/version.json"
)


def parse_version(version):
    if version is None:
        return ()
    digits = re.findall(r"\d+", str(version))
    if not digits:
        return ()
    return tuple(int(part) for part in digits)


def is_newer_version(remote_version, local_version):
    remote_parts = parse_version(remote_version)
    local_parts = parse_version(local_version)
    max_len = max(len(remote_parts), len(local_parts))
    if len(remote_parts) < max_len:
        remote_parts = remote_parts + (0,) * (max_len - len(remote_parts))
    if len(local_parts) < max_len:
        local_parts = local_parts + (0,) * (max_len - len(local_parts))
    return remote_parts > local_parts


def _candidate_manifest_paths():
    paths = []
    base_dir = Path(__file__).resolve().parent
    # Prefer a manifest placed next to the running executable (app_dir)
    # so local deployments can override the packaged manifest.
    app_dir = Path(sys.executable).resolve().parent if getattr(sys, "executable", None) else base_dir
    paths.append(app_dir / "version.json")
    paths.append(base_dir / "version.json")
    return paths


def _candidate_manifest_urls():
    urls = []
    env_url = os.getenv("CALCULADORA_EXPO_UPDATE_URL") or os.getenv("EXPO_UPDATE_URL")
    if env_url:
        urls.append(env_url)
    if DEFAULT_REMOTE_UPDATE_URL and "your-user" not in DEFAULT_REMOTE_UPDATE_URL and "example.com" not in DEFAULT_REMOTE_UPDATE_URL:
        urls.append(DEFAULT_REMOTE_UPDATE_URL)
    return urls


def _load_json_from_file(path):
    file_path = Path(path)
    if not file_path.exists():
        return None
    try:
        payload = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return None
    return payload if isinstance(payload, dict) else None


def _fetch_json_from_url(url):
    if not url or not url.startswith(("http://", "https://")):
        return None
    try:
        with request.urlopen(url, timeout=8) as response:
            content = response.read()
        payload = json.loads(content.decode("utf-8"))
    except (ValueError, TypeError, error.URLError, error.HTTPError, TimeoutError):
        return None
    return payload if isinstance(payload, dict) else None


def read_update_manifest():
    # Prefer remote manifests so installed apps can detect newer versions
    # hosted externally. Fall back to local manifests if no remote is available.
    for candidate in _candidate_manifest_urls():
        manifest = _fetch_json_from_url(candidate)
        if manifest:
            return manifest

    for candidate in _candidate_manifest_paths():
        manifest = _load_json_from_file(candidate)
        if manifest:
            return manifest

    return None


def check_for_updates(current_version=None):
    current_version = current_version or APP_VERSION
    manifest = read_update_manifest()
    if not manifest:
        return {
            "has_update": False,
            "current_version": current_version,
            "latest_version": current_version,
            "download_url": "",
            "notes": "",
            "error": "No update manifest found.",
        }

    latest_version = str(manifest.get("version") or current_version)
    download_url = manifest.get("download_url") or ""
    notes = manifest.get("notes") or ""
    return {
        "has_update": is_newer_version(latest_version, current_version),
        "current_version": current_version,
        "latest_version": latest_version,
        "download_url": download_url,
        "notes": notes,
        "error": "",
    }


def _download_file_to_path(download_url, destination_path):
    if not download_url:
        return False
    destination = Path(destination_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    if download_url.startswith(("http://", "https://")):
        try:
            with request.urlopen(download_url, timeout=20) as response, open(destination, "wb") as file_handle:
                shutil.copyfileobj(response, file_handle)
            return True
        except (error.URLError, error.HTTPError, TimeoutError, OSError):
            return False

    source_path = Path(download_url)
    if source_path.exists():
        try:
            shutil.copy2(source_path, destination)
            return True
        except OSError:
            return False
    return False


def schedule_update_install(new_executable_path, current_executable_path=None):
    current_executable = Path(current_executable_path or sys.executable).resolve()
    downloaded_exe = Path(new_executable_path).resolve()
    if not downloaded_exe.exists():
        return False

    batch_path = current_executable.parent / "update_calculadora_expo.bat"
    batch_text = (
        "@echo off\n"
        "setlocal\n"
        "ping -n 4 127.0.0.1 > NUL\n"
        f"copy /Y \"{downloaded_exe}\" \"{current_executable}\" > NUL\n"
        f"start \"\" \"{current_executable}\"\n"
        f"del /f /q \"{batch_path}\"\n"
        "exit /b 0\n"
    )
    try:
        batch_path.write_text(batch_text, encoding="utf-8")
        subprocess.Popen(["cmd.exe", "/c", str(batch_path)], shell=False)
        return True
    except (OSError, ValueError):
        return False


def download_and_apply_update(download_url, current_executable_path=None):
    current_executable = Path(current_executable_path or sys.executable).resolve()
    temp_dir = Path(tempfile.gettempdir())
    temp_target = temp_dir / f"{APP_NAME}_update.exe"

    if not _download_file_to_path(download_url, temp_target):
        return False

    return schedule_update_install(temp_target, current_executable)
