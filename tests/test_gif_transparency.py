from io import BytesIO
from os.path import abspath, dirname, join

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine

STICKER = abspath(join(dirname(__file__), "../course/images/sticker.gif"))


def test_resized_gif_keeps_transparent_background():
    config = Config(
        SECURITY_KEY="ACME-SEC",
        ENGINE="thumbor.engines.pil",
        PILLOW_PRESERVE_INDEXED_MODE=True,
    )
    engine = Engine(Context(config=config))
    with open(STICKER, "rb") as image_file:
        engine.load(image_file.read(), ".gif")

    source = Image.open(STICKER)
    assert "transparency" in source.info
    assert source.convert("RGBA").getpixel((0, 0))[3] == 0

    engine.resize(240, 160)
    result = Image.open(BytesIO(engine.read(".gif")))

    assert "transparency" in result.info
    assert result.convert("RGBA").getpixel((0, 0))[3] == 0
