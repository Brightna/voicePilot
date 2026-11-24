# VoicePilot

음성 명령을 통해 PC를 제어하는 음성 비서 프로젝트입니다.

사용자의 한국어 음성을 텍스트로 변환하고, 명령어를 분석하여 프로그램 실행, 웹 검색, 파일 열기 등의 작업을 수행하는 것을 목표로 합니다.

## 1. 개발 환경

- OS: Windows 11
- Python: 3.12
- 음성 인식: faster-whisper
- 오디오 입력: sounddevice
- 데이터 처리: numpy

## 2. 프로젝트 구조

```text
voicePilot/
├── speech/
│   ├── __init__.py
│   ├── recognition.py
│   └── command_parser.py
├── mic_test.py
├── test_parser.py
├── test_pipeline.py
├── README.md
└── .gitignore
```

## 3. 설치 방법

가상환경을 생성하고 활성화합니다.

```bash
py -3.12 -m venv .venv
source .venv/Scripts/activate
```

필요한 라이브러리를 설치합니다.

```bash
python -m pip install numpy sounddevice faster-whisper
```

## 4. 주요 기능

### ① 음성 인식 (`speech/recognition.py`)

- 마이크를 통해 음성 입력
- faster-whisper 모델을 이용한 한국어 음성 인식
- CPU 환경에서 int8 방식으로 모델 실행
- 인식 결과를 문자열로 반환

### ② 명령어 분석 (`speech/command_parser.py`)

인식된 문장을 분석하여 실행할 명령어를 딕셔너리 형태로 반환합니다.

지원하는 명령어 유형:

| 명령어          | 반환 유형    |
| --------------- | ------------ |
| 프로그램 실행   | `open_app`   |
| 웹 검색         | `web_search` |
| 파일 열기       | `open_file`  |
| 알 수 없는 명령 | `unknown`    |

예시:

```python
parse_command("크롬 실행해 줘")
```

결과:

```python
{"type": "open_app", "target": "chrome"}
```

## 5. 실행 및 테스트

명령어 분석 테스트:

```bash
python test_parser.py
```

음성 인식과 명령어 분석 파이프라인 테스트:

```bash
python test_pipeline.py
```

실제 마이크 음성 인식 테스트:

```bash
python -c "from speech.recognition import listen; print(listen())"
```

※ `test_pipeline.py`는 실제 마이크 녹음이 아닌 테스트 문장을 사용합니다.

## 6. 팀 역할

- A파트: 음성 인식 및 명령어 분석
- B파트: PC 제어 및 명령 실행

※ 각 모듈은 최종 통합 과정에서 연결합니다.

## 7. 향후 개선 사항

- 실제 음성 인식 정확도 검증
- tiny, base, small 모델 성능 비교
- 다양한 한국어 명령어 표현 지원
- # 음성 인식부터 PC 제어까지 전체 기능 통합

## PC 제어 모듈 (control/)

PyAutoGUI 기반으로 프로그램 실행, 웹 검색, 파일 검색 및 열기 기능을 구현한 모듈입니다.

### 파일별 역할

| 파일              | 기능                                                            |
| ----------------- | --------------------------------------------------------------- |
| `gui_utils.py`    | PyAutoGUI를 이용한 Windows 실행 창(`Win + R`) 조작 및 명령 입력 |
| `app_launcher.py` | 프로그램 실행 (메모장, Chrome, 계산기, 파일 탐색기)             |
| `web_search.py`   | 검색 URL 생성 및 기본 브라우저에서 검색 페이지 열기             |
| `file_opener.py`  | 지정 폴더에서 파일 검색 후 열기                                 |
| `executor.py`     | 명령 종류에 따라 기능 호출 및 결과 반환                         |
| `__init__.py`     | 외부에서 `execute()` 함수를 가져올 수 있도록 연결               |

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
