from urllib.parse import quote

from .gui_utils import open_with_run


def search_web(query):
    if not isinstance(query, str):
        raise ValueError("검색어는 문자열이어야 합니다.")

    query = query.strip()

    if not query:
        raise ValueError("검색어가 비어 있습니다.")

    # 한글 검색어를 URL 형식으로 변환
    encoded_query = quote(query)

    # 구글 검색 주소 생성
    url = f"https://www.google.com/search?q={encoded_query}"

    # PyAutoGUI로 Windows 실행 창 조작
    open_with_run(url)

    return f"'{query}' 웹 검색 요청 완료"
