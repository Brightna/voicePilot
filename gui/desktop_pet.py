import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QLabel, QWidget, QMenu
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from gui.voice_worker import VoiceWorker


ASSETS = Path(__file__).parent / "assets"
PET_SIZE = 120


class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()

        self.pet_size = PET_SIZE
        self.state = "idle"
        self.drag_position = None
        self.closing = False

        # 투명 배경 및 항상 위에 표시
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        # 캐릭터
        self.character = QLabel(self)
        self.character.setAlignment(Qt.AlignCenter)
        self.character.setAttribute(
            Qt.WA_TransparentForMouseEvents
        )

        # 말풍선
        self.bubble = QLabel(self)
        self.bubble.setAlignment(Qt.AlignCenter)
        self.bubble.setWordWrap(True)

        self.bubble.setStyleSheet("""
            QLabel {
                background-color: white;
                color: #344054;
                border: 1px solid #B8D4E8;
                border-radius: 14px;
                padding: 6px;
                font-size: 12px;
            }
        """)

        self.bubble.setText("준비 중...")
        self.set_size(self.pet_size)

        # 화면 오른쪽 아래에 배치
        screen = QApplication.primaryScreen().availableGeometry()

        self.move(
            screen.right() - self.width() - 20,
            screen.bottom() - self.height() - 20
        )

        # 음성 처리 스레드 연결
        self.worker = VoiceWorker(self)

        self.worker.state_changed.connect(self.set_state)
        self.worker.message_changed.connect(self.set_message)
        self.worker.finished.connect(self.on_worker_finished)

        # 음성 종료 신호 연결
        self.worker.exit_requested.connect(self.close)

        self.worker.start()

    # 캐릭터 크기 변경
    def set_size(self, size):
        self.pet_size = size

        width = max(size, 180)

        self.resize(width, size + 65)

        self.bubble.setGeometry(
            0, 0, width, 60
        )

        self.character.setGeometry(
            (width - size) // 2,
            65,
            size,
            size
        )

        self.set_state(self.state)

    # 캐릭터 상태 변경
    def set_state(self, state):
        if self.closing:
            return

        self.state = state

        pixmap = QPixmap(
            str(ASSETS / f"{state}.png")
        )

        self.character.setPixmap(
            pixmap.scaled(
                self.pet_size,
                self.pet_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

    # 말풍선 변경
    def set_message(self, message):
        if not self.closing:
            self.bubble.setText(message)

    # 마우스로 캐릭터 잡기
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint()
                - self.pos()
            )

    # 캐릭터 이동
    def mouseMoveEvent(self, event):
        if self.drag_position is not None:
            self.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )

    def mouseReleaseEvent(self, event):
        self.drag_position = None

    # 우클릭 메뉴
    def contextMenuEvent(self, event):
        if self.closing:
            return

        menu = QMenu(self)

        size_menu = menu.addMenu("크기 변경")

        for size in [80, 100, 120, 150]:
            action = size_menu.addAction(f"{size}px")

            action.triggered.connect(
                lambda checked=False, s=size:
                self.set_size(s)
            )

        menu.addSeparator()

        exit_action = menu.addAction("피코 종료")
        exit_action.triggered.connect(self.close)

        menu.exec(event.globalPos())

    # 프로그램 종료
    def closeEvent(self, event):
        if self.worker.isRunning():
            self.closing = True
            self.bubble.setText("종료 중...")
            self.worker.requestInterruption()
            event.ignore()
        else:
            event.accept()
            QApplication.instance().quit()

    # 음성 처리 스레드 종료 후 프로그램 종료
    def on_worker_finished(self):
        if self.closing:
            self.close()
            QApplication.instance().quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    pet = DesktopPet()
    pet.show()

    sys.exit(app.exec())