import os
import shutil
from pathlib import Path

from .gui_utils import open_with_run


APPS = {
    "notepad": "notepad",
    "calculator": "calc",
    "explorer": "explorer",
}


def find_chrome():
    chrome = shutil.which("chrome.exe")

    if chrome:
        return chrome

    for base in [
        os.environ.get("PROGRAMFILES"),
        os.environ.get("PROGRAMFILES(X86)"),
        os.environ.get("LOCALAPPDATA"),
    ]:
        if base:
            path = Path(base) / "Google/Chrome/Application/chrome.exe"

            if path.is_file():
                return str(path)

    return None


def launch_app(app_name):
    if not isinstance(app_name, str):
        raise ValueError("프로그램 이름은 문자열이어야 합니다.")

    app_name = app_name.strip().lower()

    if app_name == "chrome":
        chrome_path = find_chrome()

        if chrome_path is None:
            raise FileNotFoundError("Chrome을 찾을 수 없습니다.")

        open_with_run(f'"{chrome_path}"', use_clipboard=True)

    elif app_name in APPS:
        open_with_run(APPS[app_name])

    else:
        raise ValueError(f"지원하지 않는 프로그램: {app_name}")

    return f"{app_name} 실행 요청 완료"
