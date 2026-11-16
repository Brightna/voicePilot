
from speech.recognition import listen
from speech.command_parser import parse_command

# 실제 음성 대신 테스트 문장을 사용
recognized_text = "오늘 날씨 검색해 줘"

print("인식된 문장:", recognized_text)

command = parse_command(recognized_text)

print("분석 결과:", command)
