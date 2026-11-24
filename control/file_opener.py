import winreg
import os
from pathlib import Path

from .gui_utils import open_with_run


# Windows 사용자 폴더 식별자
FOLDER_IDS = {
    "desktop": "{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}",
    "documents": "{FDD39AD0-238F-46AF-ADB4-6C85480369C7}",
    "downloads": "{374DE290-123F-4565-9164-39C4925E467B}",
}



def get_user_folder(folder_name):
    if not isinstance(folder_name, str):
        raise ValueError("폴더 이름은 문자열이어야 합니다.")

    folder_name = folder_name.strip().lower()

    if folder_name not in FOLDER_IDS:
        raise ValueError(f"지원하지 않는 폴더: {folder_name}")

    registry_path = (
        r"Software\Microsoft\Windows"
        r"\CurrentVersion\Explorer\User Shell Folders"
    )

    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            registry_path
        ) as key:
            raw_path, _ = winreg.QueryValueEx(
                key, FOLDER_IDS[folder_name]
            )

        folder_path = Path(
            os.path.expandvars(raw_path)
        ).expanduser()

    except FileNotFoundError:
        # 레지스트리에서 값을 찾지 못하면 기본 경로 사용
        folder_path = Path.home() / {
            "desktop": "Desktop",
            "documents": "Documents",
            "downloads": "Downloads",
        }[folder_name]

    if not folder_path.is_dir():
        raise FileNotFoundError(
            f"폴더가 존재하지 않습니다: {folder_path}"
        )

    return folder_path



def open_file(name, folder):
    if not isinstance(name, str):
        raise ValueError("파일 이름은 문자열이어야 합니다.")

    name = name.strip()

    if not name:
        raise ValueError("파일 이름이 비어 있습니다.")

    # 1. 폴더 이름을 실제 경로로 변환
    folder_path = get_user_folder(folder)

    # 2. 해당 폴더 내부에서 파일 검색
    matches = [
        path for path in folder_path.rglob("*")
        if path.is_file()
        and name.casefold() in path.name.casefold()
    ]

    # 3. 검색 결과 확인
    if not matches:
        raise FileNotFoundError(
            f"'{name}' 파일을 찾을 수 없습니다."
        )

    if len(matches) > 1:
        raise ValueError(
            f"일치하는 파일이 {len(matches)}개입니다. "
            "파일 이름을 더 구체적으로 지정하세요."
        )

    # 4. 실행 창에 파일 경로를 붙여넣어 열기
    file_path = str(matches[0])

    open_with_run(
        f'"{file_path}"',
        use_clipboard=True
    )

    return f"파일 열기 요청 완료: {matches[0].name}"

