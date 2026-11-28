
import re


# 1. 문장 정규화
def normalize_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[.!?,。！？]+$", "", text)
    return text.strip()


# 부정 명령 검사
def is_negative_command(text: str) -> bool:
    patterns = [
        r"지\s*마(?:세요|요)?$",
        r"지\s*말아\s*줘$",
        r"지\s*말아\s*주세요$",
        r"필요\s*없어(?:요)?$",
        r"하지\s*않았으면\s*좋겠어$"
    ]

    return any(re.search(pattern, text) for pattern in patterns)

# 2. 프로그램 실행 명령 분석
def parse_app_command(text: str) -> dict:
    text = re.sub(r"\s*,\s*", " ", text).strip()

    apps = {
        "크롬": "chrome",
        "chrome": "chrome",
        "인터넷 브라우저": "chrome",
        "인터넷": "chrome",
        "메모장": "notepad",
        "계산기": "calculator"
    }

    action = (
        r"(?:실행(?:\s*해)?|켜|열어|띄워|시작(?:\s*해)?)"
        r"\s*(?:줘|주|주세요|줄래|봐|부탁해)?"
    )

    indirect = (
        r"(?:쓰고|사용하고|하고|열고|켜고)"
        r"\s*싶어(?:요)?"
    )

    for app_name, target in apps.items():
        pattern = (
            r"(?:나\s+|저\s+)?"
            + re.escape(app_name)
            + r"(?:을|를)?\s*"
            + r"(?:(?:좀|한번|한\s*번)\s*)?"
            + r"(?:" + action + "|" + indirect + r")"
        )

        if re.fullmatch(pattern, text.lower()):
            return {"type": "open_app", "target": target}

    return None

# 3. 파일 열기 명령 분석
def parse_file_command(text: str) -> dict:
    folder_aliases = {
        "바탕화면": "desktop",
        "데스크톱": "desktop",
        "내 바탕화면": "desktop",
        "문서": "documents",
        "내 문서": "documents",
        "다운로드": "downloads"
    }

    # 문장 끝의 파일 열기 요청 분리
    match = re.fullmatch(
        r"(?P<body>.*?)\s*"
        r"(?:찾아서\s*)?"
        r"열어\s*(?:줘|주세요|줄래|봐)",
        text
    )

    if not match:
        return None

    body = match.group("body").strip()
    folder = ""

    # 폴더명 추출
    for alias in sorted(folder_aliases, key=len, reverse=True):
        pattern = (
            r"^" + re.escape(alias)
            + r"\s*(?:폴더)?\s*"
            + r"(?:에\s*있는|있는|의|에서)\s*"
        )

        folder_match = re.match(pattern, body)

        if folder_match:
            folder = folder_aliases[alias]
            body = body[folder_match.end():].strip()
            break

    # 파일명 뒤에 붙은 요청 표현 제거
    name = re.sub(
        r"\s*(?:파일|문서)(?:을|를)?$",
        "",
        body
    ).strip()

    # 파일명이 없는 경우 실행 차단
    if not name:
        return None

    return {
        "type": "open_file",
        "name": name,
        "folder": folder
    }

# 4. 웹 검색 명령 분석
def parse_search_command(text: str) -> dict:
    pattern = (
        r"(?P<query>.*?)\s*"
        r"(?:좀\s*)?"
        r"(?:검색(?:해)?|찾아(?:봐)?|알아\s*봐)"
        r"\s*(?:줘|주세요|줄래|봐)?$"
    )

    match = re.fullmatch(pattern, text)

    if not match:
        return None

    query = match.group("query").strip()

    # 검색 엔진 지정 표현 제거
    query = re.sub(
        r"^(?:네이버|구글)에서\s*",
        "",
        query
    ).strip()

    # 검색어가 없는 경우 실행하지 않음
    if not query:
        return None

    return {
        "type": "web_search",
        "query": query
    }

# 5. 전체 명령어 분석
def parse_command(text: str) -> dict:
    raw_text = text
    text = normalize_text(text)

    if not text or is_negative_command(text):
        return {
            "type": "unknown",
            "raw_text": raw_text
        }

    # 프로그램 실행
    result = parse_app_command(text)
    if result is not None:
        return result

    # 파일 열기
    result = parse_file_command(text)
    if result is not None:
        return result

    # 웹 검색
    result = parse_search_command(text)
    if result is not None:
        return result

    # 알 수 없는 명령
    return {
        "type": "unknown",
        "raw_text": raw_text
    }
