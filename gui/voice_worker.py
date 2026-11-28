import time

from PySide6.QtCore import QThread, Signal

from speech.recognition import (
    load_model,
    record_audio,
    transcribe_audio
)
from speech.wake_word import detect_wake_word
from speech.command_parser import parse_command
from control import execute


class VoiceWorker(QThread):
    state_changed = Signal(str)
    message_changed = Signal(str)
    exit_requested = Signal()

    def run(self):
        try:
            self.message_changed.emit("준비 중...")
            load_model("base")

            while not self.isInterruptionRequested():

                # 1. 호출어 대기
                self.state_changed.emit("idle")
                self.message_changed.emit("피코야! 라고 불러 줘.")

                audio = record_audio(2)
                text = transcribe_audio(audio, "base")
                print("호출어 인식 결과:", repr(text))

                if self.isInterruptionRequested():
                    break

                if not detect_wake_word(text):
                    continue

                # 2. 명령어 듣기
                # 2. 명령어 듣기 준비
                self.state_changed.emit("listening")
                self.message_changed.emit("잠시만요!")

                # 1초간 준비 시간
                time.sleep(1)

                if self.isInterruptionRequested():
                    break

                #명령어 녹음 시작
                self.message_changed.emit("말씀하세요!")
                audio = record_audio(5)

                if self.isInterruptionRequested():
                    break

                # 3. 음성 인식 및 명령 분석
                self.state_changed.emit("thinking")
                self.message_changed.emit("생각 중...")

                text = transcribe_audio(audio, "base")

                # 음성 종료 명령
                if "종료" in text:
                    self.message_changed.emit("다음에 또 만나요!")
                    time.sleep(1)
                    self.exit_requested.emit()
                    return

                command = parse_command(text)

                if self.isInterruptionRequested():
                    break

                # 4. 명령 실행
                if command["type"] == "unknown":
                    self.message_changed.emit(
                        "잘 이해하지 못했어요."
                    )
                else:
                    result = execute(command)

                    if result["success"]:
                        self.state_changed.emit("success")

                    self.message_changed.emit(
                        result["message"]
                    )

                # 5. 결과 표시 후 대기
                for _ in range(20):
                    if self.isInterruptionRequested():
                        break

                    time.sleep(0.1)

        except Exception as e:
            self.message_changed.emit(f"오류: {e}")
            print("음성 처리 오류:", e)