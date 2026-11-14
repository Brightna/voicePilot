import time
import pyautogui

from .app_launcher import launch_app
from .web_search import search_web
from .file_opener import open_file


def execute(command: dict) -> dict:
    start = time.perf_counter()

    try:
        if not isinstance(command, dict):
            raise ValueError("명령은 딕셔너리여야 합니다.")

        command_type = command.get("type")

        if command_type == "open_app":
            message = launch_app(
                command.get("target", "")
            )

        elif command_type == "web_search":
            message = search_web(
                command.get("query", "")
            )

        elif command_type == "open_file":
            message = open_file(
                command.get("name", ""),
                command.get("folder", "")
            )

        elif command_type == "unknown":
            raise ValueError("인식할 수 없는 명령입니다.")

        else:
            raise ValueError(
                f"지원하지 않는 명령: {command_type}"
            )

        success = True

    except pyautogui.FailSafeException:
        success = False
        message = "사용자가 자동화를 중단했습니다."

    except (ValueError, OSError, RuntimeError, TypeError,
            pyautogui.PyAutoGUIException) as e:
        success = False
        message = str(e)

    elapsed = round(time.perf_counter() - start, 3)

    return {
        "success": success,
        "message": message,
        "elapsed": elapsed
    }

