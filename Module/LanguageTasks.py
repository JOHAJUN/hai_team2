import openai
import json
import tiktoken

def count_tokens(text, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def extract_highlight_only(transcript, max_tokens=3000, model="gpt-4"):
    """
    Uses GPT to extract only highlight-worthy transcript segments.
    Returns: List of segments: [{start, end, text}, ...]
    """

    formatted_segments = []
    total_tokens = 0


    for i, seg in enumerate(transcript):
        line = f"[{seg['start']:.2f} - {seg['end']:.2f}] {seg['text']}"
        tokens = count_tokens(line, model=model)
        if total_tokens + tokens > max_tokens:
            break
        formatted_segments.append(f"{i}: {line}")
        total_tokens += tokens

    full_script = "\n".join(formatted_segments)

    prompt = f"""
유튜브 쇼츠 영상 편집자이다. 영상 전체 자막을 주겠다.
각 줄은 자막의 인덱스, 시간, 텍스트로 구성되어 있습니다.

가장 흥미롭고 감정적으로 강한 부분만 선택해서 출력하세요.
각 하이라이트는 다음과 같은 JSON 형식으로 반환하세요:

[
  {{ "start": 15.2, "end": 18.1, "text": "이건 진짜 대박이야!" }},
  ...
]

스크립트:
{full_script}
"""

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert YouTube Shorts editor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        content = response.choices[0].message['content']


        highlights = json.loads(content) if content.strip().startswith("[") else eval(content)

        return highlights

    except Exception as e:
        print("❌ GPT highlight extraction failed:", e)
        return []
