
import re


# 1. 문장 정규화
def normalize_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


# 2. 프로그램 실행 명령 분석
def parse_app_command(text: str) -> dict:
    apps = {
        "크롬": "chrome",
        "chrome": "chrome",
        "인터넷 브라우저": "chrome",
        "메모장": "notepad",
        "계산기": "calculator"
    }

    action_words = ["실행", "켜", "열어", "띄워", "시작"]
    lower_text = text.lower()

    for app_name, target in apps.items():
        if app_name in lower_text:
            if any(word in text for word in action_words):
                return {
                    "type": "open_app",
                    "target": target
                }

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

    end_words = r"(?:열어\s*줘|열어줘|열어주세요)$"

    folder_match = re.search(
        r"(?P<folder>.+?)\s*(?:폴더에\s*있는|폴더의|에\s*있는|의)"
        r"\s*(?P<name>.+?)\s*(?:파일|문서)?\s*" + end_words,
        text
    )

    if folder_match:
        folder = folder_match.group("folder").strip()
        name = folder_match.group("name").strip()

        folder = re.sub(r"\s*폴더$", "", folder)
        folder = folder_aliases.get(folder, "")

        if folder:
            return {
                "type": "open_file",
                "name": name,
                "folder": folder
            }

    # 폴더가 지정되지 않은 파일 열기
    if re.search(r"(?:파일|문서)\s*열|열어\s*줘|열어줘|열어주세요", text):
        name = text

        remove_words = [
            "파일", "문서",
            "열어 줘", "열어줘", "열어주세요"
        ]

        for word in remove_words:
            name = name.replace(word, "")

        name = name.strip()

        return {
            "type": "open_file",
            "name": name,
            "folder": ""
        }

    return None


# 4. 웹 검색 명령 분석
def parse_search_command(text: str) -> dict:
    search_words = [
        "검색", "찾아줘", "찾아 줘",
        "찾아봐", "찾아 봐",
        "알아봐", "알아 봐"
    ]

    if not any(word in text for word in search_words):
        return None

    query = text

    remove_words = [
        "검색해 줘", "검색해줘",
        "검색해 주세요", "검색해",
        "검색", "찾아 줘", "찾아줘",
        "찾아 봐", "찾아봐",
        "좀 알아봐", "알아 봐", "알아봐"
    ]

    for word in remove_words:
        query = query.replace(word, "")

    query = re.sub(r"(네이버|구글)에서", "", query)
    query = query.strip()

    return {
        "type": "web_search",
        "query": query
    }


# 5. 전체 명령어 분석
def parse_command(text: str) -> dict:
    raw_text = text
    text = normalize_text(text)

    if not text:
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
