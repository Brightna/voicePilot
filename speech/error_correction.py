import unicodedata


def decompose_hangul(text):
    return unicodedata.normalize("NFD", text)

def edit_distance(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]

    for i in range(len(a) + 1):
        dp[i][0] = i

    for j in range(len(b) + 1):
        dp[0][j] = j

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )

    return dp[len(a)][len(b)]

def similarity(a, b, use_jamo=False):
    if use_jamo:
        a = decompose_hangul(a)
        b = decompose_hangul(b)

    max_length = max(len(a), len(b))

    if max_length == 0:
        return 1.0

    distance = edit_distance(a, b)

    return 1 - distance / max_length

def correct_word(word, vocabulary, threshold=0.6, use_jamo=False):
    best_word = word
    best_score = 0.0

    for candidate in vocabulary:
        score = similarity(word, candidate, use_jamo)

        if score > best_score:
            best_score = score
            best_word = candidate

    if best_score >= threshold:
        return best_word

    return word

def correct_text(text, vocabulary, threshold=0.6, use_jamo=False):
    words = text.split()
    corrected_words = []

    for word in words:
        corrected = correct_word(
            word, vocabulary, threshold, use_jamo
        )
        corrected_words.append(corrected)

    return " ".join(corrected_words)

if __name__ == "__main__":
    vocabulary = [
        "계산기",
        "크롬",
        "메모장",
        "파일 탐색기",
        "바탕화면",
        "다운로드",
        "문서",
        "파이썬",
        "인공지능"
    ]

    sentences = [
        "그럼 실행해줘",
        "메모짱 열어줘",
        "파이선 사용법 찾아줘",
        "인공지는 뉴스 검색해줘",
        "개상지 켜줘",
        "세탁기 돌려줘",
        "그럼 내일 만나자",
        "오늘 너무 피곤하다",
        "계산기 켜지 마",
        "계산기 켜줘",
        ""
    ]

    for text in sentences:
        char_result = correct_text(
            text, vocabulary, 0.6, False
        )

        jamo_result = correct_text(
            text, vocabulary, 0.6, True
        )

        print(f"\n원본: {text}")
        print("일반 문자 보정:", char_result)
        print("한글 자모 보정:", jamo_result)