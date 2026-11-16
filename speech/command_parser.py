
import re


def parse_command(text: str) -> dict:
    raw_text = text
    text = text.strip()

    if not text:
        return {
            "type": "unknown",
            "raw_text": raw_text
        }

    lower_text = text.lower()

    # 1. 프로그램 실행 명령
    apps = {
        "크롬": "chrome",
        "chrome": "chrome"
    }

    for app_name, target in apps.items():
        if app_name in lower_text:
            if any(word in lower_text for word in ["실행", "켜", "열어"]):
                return {
                    "type": "open_app",
                    "target": target
                }

    # 2. 웹 검색 명령
    search_words = ["검색", "찾아줘", "찾아 줘"]

    if any(word in text for word in search_words):
        query = text

        remove_words = [
            "검색해 줘", "검색해줘", "검색해 주세요",
            "검색해", "검색", "찾아 줘", "찾아줘"
        ]

        for word in remove_words:
            query = query.replace(word, "")

        query = re.sub(r"(네이버|구글)에서", "", query)
        query = query.strip()

        return {
            "type": "web_search",
            "query": query
        }

    # 3. 파일 열기 명령
    if any(word in text for word in ["파일 열", "문서 열", "열어 줘", "열어줘", "열어주세요"]):

        # 폴더 정보가 포함된 경우
        folder_match = re.search(
            r"(.+?)\s*폴더에\s*있는\s*(.+?)\s*(?:파일|문서)?\s*(?:열어\s*줘|열어줘|열어주세요)$",
            text
        )

        if folder_match:
            folder = folder_match.group(1).strip()
            name = folder_match.group(2).strip()

        else:
            folder = ""
            name = text

            remove_words = ["파일", "문서", "열어 줘", "열어줘", "열어주세요"]

            for word in remove_words:
                name = name.replace(word, "")

            name = name.strip()

        return {
            "type": "open_file",
            "name": name,
            "folder": folder
        }

    # 4. 인식할 수 없는 명령
    return {
        "type": "unknown",
        "raw_text": raw_text
    }
