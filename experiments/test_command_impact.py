import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from speech.command_parser import parse_command

sentences = [
    "바탕화면에 있는 사진 열어줘",
    "바탕화면 있는 사진 열어줘",
    "메모장이 어디 있더라",
    "메모장 어디 있더라",
    "인공지능이 미래 사회에 미치는 영향 검색해줘",
    "인공지능 미래 사회에 미치는 영향 검색해줘",
    "그럼 실행해줘",
    "크롬 실행해줘",
    "그럼 내일 만나자",
    "크롬 내일 만나자",
    "계산기 켜지 마",
    "계산기 켜줘",
    "계산기",
    ""
]

for text in sentences:
    print("\n입력:", text)
    print("분석:", parse_command(text))