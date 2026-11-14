import time
import pyautogui
import pyperclip

# PyAutoGUI 기본 설정
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2


def open_with_run(text, use_clipboard=False):
    # 1. Windows 실행 창 열기
    pyautogui.hotkey("win", "r")
    time.sleep(0.7)

    # 2. 기존 입력 내용 지우기
    pyautogui.hotkey("ctrl", "a")

    # 3. 실행할 명령 또는 경로 입력
    if use_clipboard:
        previous_clipboard = pyperclip.paste()

        try:
            pyperclip.copy(text)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.3)
        finally:
            pyperclip.copy(previous_clipboard)
    else:
        pyautogui.write(text, interval=0.02)

    # 4. Enter를 눌러 실행
    pyautogui.press("enter")

    return "실행 명령을 입력했습니다."
