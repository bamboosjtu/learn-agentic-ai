import os
from openai import OpenAI
from PIL import Image
from io import BytesIO
import base64

API_KEY = os.environ.get('AIHUBMIX_API_KEY')
BASE_URL = os.environ.get('AIHUBMIX_BASE_URL')

# 创建客户端
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

# 可选参数（OpenAI接口不支持 4K 图片，默认为 1K)
aspect_ratio = "2:3"   # 支持: 1:1（默认）, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9

prompt = (
    """A cinematic portrait of LinaBell reimagined in a Renaissance cyberpunk world, standing in the heart of a grand futuristic Florence at twilight. She is a clever pink fox detective dressed in an elegant fusion of 16th-century aristocratic fashion and high-tech cybernetic design: embroidered velvet gown panels, luminous fiber-optic lace, a jeweled corset with holographic filigree, metallic shoulder armor shaped like angel wings, and a glowing mechanical magnifying lens hanging from her belt. Her expression is curious, brave, and intelligent.

    The story scene: LinaBell has just uncovered a hidden conspiracy inside a cathedral-like data sanctuary, where ancient frescoes are animated by neon circuits and stained-glass windows project encrypted constellations across the marble floor. In one paw, she holds a glowing crystalline key containing forbidden memories; in the other, a delicate Renaissance notebook filled with sketches, clues, and coded symbols. Behind her, shadowy masked figures and floating surveillance drones emerge from the darkness, showing that she is being pursued after discovering the truth.

    The environment should feel like a collision between Leonardo da Vinci and a futuristic megacity: towering domes, marble statues enhanced with robotic limbs, candlelight mixed with holographic light, mechanical cherubs flying through mist, and golden cathedral arches threaded with electric cables. The mood is dramatic, mysterious, and poetic, as if this is the turning point of a beautiful detective epic. Rich Renaissance composition, painterly lighting, deep crimson, gold, teal, and neon violet palette, ultra-detailed textures, emotional storytelling, majestic atmosphere, masterpiece quality."""
    )

response = client.chat.completions.create(
    model="gemini-3.1-flash-image-preview-free",
    messages=[
        {"role": "system", "content": f"aspect_ratio={aspect_ratio}"},
        {"role": "user", "content": [{"type": "text", "text": prompt}]},
    ],
    modalities=["text", "image"]
)

# 保存图片 & 输出文本
try:
    parts = response.choices[0].message.multi_mod_content
    if parts:
        for part in parts:
            if "text" in part:
                print(part["text"])
            if "inline_data" in part:
                image_data = base64.b64decode(part["inline_data"]["data"])
                image = Image.open(BytesIO(image_data))
                filename = f"linabell_{aspect_ratio.replace(':','-')}.png"
                image.save(filename)
                print(f"Image saved: {filename}")
    else:
        print("No valid multimodal response received.")
except Exception as e:
    print(f"Error: {str(e)}")

