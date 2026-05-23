import os
import base64
from openai import OpenAI

# ====================== 固定配置 ======================
PIC_FOLDER = "./pic"       # 扫描这个文件夹下所有图片
OUTPUT_FILE = "result.txt" # 所有结果输出到这里
API_BASE = "http://127.0.0.1:1234/v1"
MODEL_NAME = "qwen3.5-4b-instruct"
# ======================================================

PROMPT = "请提取这张图片里的所有有用信息，输出文字内容。"

def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def main():
    client = OpenAI(base_url=API_BASE, api_key="lm-studio")

    # 遍历 ./pic 下所有图片（支持 png/jpg/jpeg/bmp）
    if not os.path.exists(PIC_FOLDER):
        print(f"❌ 错误：文件夹 {PIC_FOLDER} 不存在！")
        return

    images = [
        f for f in os.listdir(PIC_FOLDER)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))
    ]

    if not images:
        print("❌ pic 文件夹里没有图片")
        return

    print(f"✅ 找到 {len(images)} 张图片，开始处理...")

    # 清空结果文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("=== 图片识别结果 ===\n\n")

    # 逐张处理
    for idx, img_name in enumerate(images, 1):
        img_path = os.path.join(PIC_FOLDER, img_name)
        print(f"[{idx}/{len(images)}] 处理：{img_name}")

        try:
            b64 = image_to_base64(img_path)
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": PROMPT},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
                    ]
                }],
                temperature=0.1,
            )

            # 安全读取结果
            msg = response.choices[0].message
            text = msg.content.strip() if msg and msg.content else "无返回内容"

            # 写入文件
            with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                f.write(f"===== 图片：{img_name} =====\n")
                f.write(text + "\n\n")

            print(f"✅ 完成：{img_name}\n")

        except Exception as e:
            print(f"❌ 出错：{str(e)}\n")
            with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                f.write(f"===== 图片：{img_name} =====\n识别失败\n\n")

    print(f"\n🎉 全部处理完成！结果已保存到：{OUTPUT_FILE}")

if __name__ == "__main__":
    main()