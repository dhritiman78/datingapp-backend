import os

from PIL import Image
from io import BytesIO

from dotenv import load_dotenv
from tinify import tinify

load_dotenv()
tinify.key = os.getenv("TINIFY_API_KEY")

async def compress_image_tinypng(contents: bytes) -> BytesIO:
    try:
        source = tinify.from_buffer(contents)
        compressed = BytesIO(source.to_buffer())
        compressed.seek(0)

        return compressed
    except Exception as e:
        raise


async def compress_image_using_pill(contents: bytes, reduce_percent: float = 0.6) -> BytesIO:
    original_size_kb = len(contents) / 1024
    target_size_kb = original_size_kb * (1 - reduce_percent)

    buffer = BytesIO(contents)
    img = Image.open(buffer).convert("RGB")
    compressed = BytesIO()
    quality = 85

    while True:
        compressed.seek(0)
        compressed.truncate()

        img.save(compressed, format="JPEG", quality=quality, optimize=True)
        current_kb = compressed.tell() / 1024

        if current_kb <= target_size_kb or quality <= 40:
            break

        quality -= 5

    compressed.seek(0)

    return compressed


async def compress_image(contents: bytes) -> BytesIO:
    # try:
    #     return await compress_image_tinypng(contents)
    # except Exception:
    #     return await compress_image_using_pill(contents)
    return await compress_image_using_pill(contents)
