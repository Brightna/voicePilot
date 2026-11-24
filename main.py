from speech.recognition import listen
from speech.command_parser import parse_command
from control import execute


def main():
    print("=== VoicePilot ===")

    # 1. 음성 인식
    text = listen()

    if not text:
        print("음성을 인식하지 못했습니다.")
        return

    # 2. 명령어 분석
    command = parse_command(text)
    print("분석 결과:", command)

    # 3. PC 제어
    result = execute(command)

    # 4. 실행 결과 출력
    print("성공 여부:", result["success"])
    print("실행 결과:", result["message"])
    print("제어 소요 시간:", result["elapsed"], "초")


if __name__ == "__main__":
    main()