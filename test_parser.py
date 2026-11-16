
from speech.command_parser import parse_command

tests = [
    ("크롬 실행해 줘",
     {"type": "open_app", "target": "chrome"}),

    ("오늘 날씨 검색해 줘",
     {"type": "web_search", "query": "오늘 날씨"}),

    ("보고서 파일 열어 줘",
     {"type": "open_file", "name": "보고서", "folder": ""}),

    ("다운로드 폴더에 있는 보고서 파일 열어줘",
     {"type": "open_file", "name": "보고서", "folder": "다운로드"}),

    ("안녕 반가워",
     {"type": "unknown", "raw_text": "안녕 반가워"}),

    ("크롬 켜 줘",
     {"type": "open_app", "target": "chrome"}),

    ("구글에서 인공지능 검색해 줘",
     {"type": "web_search", "query": "인공지능"}),

    ("내 문서 폴더에 있는 과제 파일 열어 줘",
     {"type": "open_file", "name": "과제", "folder": "내 문서"}),

    ("계산기 실행해 줘",
     {"type": "unknown", "raw_text": "계산기 실행해 줘"}),

    ("내일 뭐 하지?",
     {"type": "unknown", "raw_text": "내일 뭐 하지?"})
]

passed = 0

for text, expected in tests:
    result = parse_command(text)

    if result == expected:
        print("[통과]", text)
        passed += 1
    else:
        print("[실패]", text)
        print("예상:", expected)
        print("실제:", result)

print(f"\n결과: {passed}/{len(tests)} 통과")