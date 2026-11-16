## PC 제어 모듈 (control/)

PyAutoGUI 기반으로 프로그램 실행, 웹 검색, 파일 검색 및 열기 기능을 구현한 모듈입니다.

### 파일별 역할

| 파일 | 기능 |
|---|---|
| `gui_utils.py` | PyAutoGUI를 이용한 Windows 실행 창(`Win + R`) 조작 및 명령 입력 |
| `app_launcher.py` | 프로그램 실행 (메모장, Chrome, 계산기, 파일 탐색기) |
| `web_search.py` | 검색 URL 생성 및 기본 브라우저에서 검색 페이지 열기 |
| `file_opener.py` | 지정 폴더에서 파일 검색 후 열기 |
| `executor.py` | 명령 종류에 따라 기능 호출 및 결과 반환 |
| `__init__.py` | 외부에서 `execute()` 함수를 가져올 수 있도록 연결 |

### 지원 기능

**1. 프로그램 실행 (`open_app`)**

지원 프로그램:
- `notepad`: 메모장
- `chrome`: Google Chrome
- `calculator`: 계산기
- `explorer`: 파일 탐색기

**2. 웹 검색 (`web_search`)**

검색어를 Google 검색 URL로 변환한 뒤, PyAutoGUI를 이용하여 Windows 기본 브라우저에서 검색 페이지를 엽니다. 검색 결과를 직접 수집하는 방식은 아닙니다.

**3. 파일 열기 (`open_file`)**

지원 폴더:
- `desktop`: 바탕화면
- `documents`: 문서
- `downloads`: 다운로드

지정 폴더와 하위 폴더에서 파일 이름을 검색합니다. 일치하는 파일이 여러 개일 경우 오류 메시지를 반환합니다.

### 명령 인터페이스 (A → B)

```python
{"type": "open_app", "target": "chrome"}
{"type": "web_search", "query": "오늘 날씨"}
{"type": "open_file", "name": "보고서", "folder": "documents"}
{"type": "unknown", "raw_text": "인식된 원문"}
```

### 결과 인터페이스 (B → main)

```python
{
    "success": True,
    "message": "chrome 실행 요청 완료",
    "elapsed": 1.523
}
```

- `success`: 명령 처리 성공 여부 (`bool`)
- `message`: 실행 결과 또는 오류 메시지 (`str`)
- `elapsed`: PC 제어 요청 처리시간 (`float`, 초 단위)

`elapsed`에는 음성인식 및 명령 분석 시간이 포함되지 않습니다.

현재 `success=True`는 GUI 실행 요청 과정에서 예외가 발생하지 않았다는 의미이며, 실제 프로그램이나 파일이 완전히 열렸는지를 자동 검증하는 것은 아닙니다.

### 사용한 라이브러리

- **PyAutoGUI**: 키보드 자동화 및 Windows GUI 제어
- **Pyperclip**: 한글 파일 경로를 클립보드로 전달
- **Python 표준 라이브러리**: `os`, `winreg`, `pathlib`, `shutil`, `urllib.parse`, `time`

### 실행 환경

- Windows
- Python 3
- PyAutoGUI 및 Pyperclip 설치 필요

```powershell
python -m pip install pyautogui pyperclip
```

### 테스트

프로그램 실행(메모장·계산기·Chrome), 한글 웹 검색, 문서 폴더의 파일 검색 및 열기 기능을 수동 테스트하여 정상 작동을 확인하였습니다.

지원하지 않는 프로그램, 빈 검색어, 존재하지 않는 파일, 지원하지 않는 폴더 및 알 수 없는 명령에 대한 예외 처리도 확인하였습니다.