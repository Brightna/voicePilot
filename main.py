from speech.recognition import listen
from speech.wake_word import wait_for_wake_word
from speech.command_parser import parse_command
from control import execute


def process_command():
    text = listen()

    if not text:
        print("음성을 인식하지 못했습니다.")
        return

    command = parse_command(text)
    print("분석 결과:", command)

    if command["type"] == "unknown":
        print("실행 가능한 명령이 아닙니다.")
        return

    result = execute(command)

    print("성공 여부:", result["success"])
    print("실행 결과:", result["message"])
    print("제어 소요 시간:", result["elapsed"], "초")


def main():
    print("=== VoicePilot - PICO ===")

    try:
        while True:
            wait_for_wake_word()
            process_command()

            print("\n대기 상태로 돌아갑니다.\n")

    except KeyboardInterrupt:
        print("\n피코를 종료합니다.")


if __name__ == "__main__":
    main()