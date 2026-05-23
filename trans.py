from openai import OpenAI

# 配置
INPUT_TXT = "result.txt"
OUTPUT_TXT = "final_sort.txt"
API_URL = "http://127.0.0.1:1234/v1"
MODEL = "qwen3.5-4b-instruct"

def read_raw_content():
    with open(INPUT_TXT, "r", encoding="utf-8") as f:
        return f.read()

def sort_by_llm(raw_text):
    client = OpenAI(base_url=API_URL, api_key="lm-studio")
    prompt = f"""
请梳理整合下面的零散内容，围绕智能助学生物产业专利案例主题，理顺逻辑、精简冗余、规整结构，形成通顺完整的格式化内容：
{raw_text}
"""
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"user","content":prompt}],
        temperature=0.2
    )
    return resp.choices[0].message.content or "整理失败"

if __name__ == "__main__":
    raw = read_raw_content()
    print("开始调用大模型整理内容...")
    res = sort_by_llm(raw)
    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        f.write(res)
    print(f"整理完成，结果保存至 {OUTPUT_TXT}")