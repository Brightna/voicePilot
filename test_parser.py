
from speech.command_parser import parse_command

tests = [
    # 기존 테스트
    ("크롬 실행해 줘",
     {"type": "open_app", "target": "chrome"}),

    ("오늘 날씨 검색해 줘",
     {"type": "web_search", "query": "오늘 날씨"}),

    ("보고서 파일 열어 줘",
     {"type": "open_file", "name": "보고서", "folder": ""}),

    ("다운로드 폴더에 있는 보고서 파일 열어줘",
     {"type": "open_file", "name": "보고서", "folder": "downloads"}),

    ("안녕 반가워",
     {"type": "unknown", "raw_text": "안녕 반가워"}),

    ("크롬 켜 줘",
     {"type": "open_app", "target": "chrome"}),

    ("구글에서 인공지능 검색해 줘",
     {"type": "web_search", "query": "인공지능"}),

    ("내 문서 폴더에 있는 과제 파일 열어 줘",
     {"type": "open_file", "name": "과제", "folder": "documents"}),

    ("계산기 실행해 줘",
     {"type": "open_app", "target": "calculator"}),

    ("내일 뭐 하지?",
     {"type": "unknown", "raw_text": "내일 뭐 하지?"}),

    # 신규 프로그램 실행 테스트
    ("메모장 실행해 줘",
     {"type": "open_app", "target": "notepad"}),

    ("계산기 켜 줘",
     {"type": "open_app", "target": "calculator"}),

    ("크롬 열어 줘",
     {"type": "open_app", "target": "chrome"}),

    # 신규 폴더 검색 테스트
    ("바탕화면에 있는 과제 파일 열어줘",
     {"type": "open_file", "name": "과제", "folder": "desktop"}),

    ("문서 폴더에 있는 보고서 파일 열어줘",
     {"type": "open_file", "name": "보고서", "folder": "documents"}),

    ("다운로드 폴더에 있는 사진 파일 열어줘",
     {"type": "open_file", "name": "사진", "folder": "downloads"}),
         # 한국어 표현 다양성 테스트
    ("메모장 좀 켜줘",
     {"type": "open_app", "target": "notepad"}),

    ("메모장 띄워 줘",
     {"type": "open_app", "target": "notepad"}),

    ("계산기 좀 실행해 줘",
     {"type": "open_app", "target": "calculator"}),

    ("크롬 좀 켜줘",
     {"type": "open_app", "target": "chrome"}),

    ("바탕화면에 있는 과제 열어줘",
     {"type": "open_file", "name": "과제", "folder": "desktop"}),

    ("다운로드 폴더의 사진 파일 열어 줘",
     {"type": "open_file", "name": "사진", "folder": "downloads"}),

    ("네이버에서 맛집 찾아줘",
     {"type": "web_search", "query": "맛집"}),

    ("인공지능 자료 찾아 줘",
     {"type": "web_search", "query": "인공지능 자료"}),
         # 새로운 표현 테스트
    ("메모장 좀 띄워줄래?",
     {"type": "open_app", "target": "notepad"}),

    ("계산기 한번 켜봐",
     {"type": "open_app", "target": "calculator"}),

    ("크롬 좀 시작해 줘",
     {"type": "open_app", "target": "chrome"}),

    ("다운로드에 있는 사진 열어줘",
     {"type": "open_file", "name": "사진", "folder": "downloads"}),

    ("바탕화면의 과제 파일 열어줘",
     {"type": "open_file", "name": "과제", "folder": "desktop"}),

    ("요즘 인공지능 동향 좀 알아봐",
     {"type": "web_search", "query": "요즘 인공지능 동향"}),

    ("구글에서 파이썬 공부법 찾아봐",
     {"type": "web_search", "query": "파이썬 공부법"}),

    ("오늘 기분이 좋아",
     {"type": "unknown", "raw_text": "오늘 기분이 좋아"})
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
