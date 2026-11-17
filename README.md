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
- 음성 인식부터 PC 제어까지 전체 기능 통합
