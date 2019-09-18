import os
from Core.constants import Const


class FunConst(Const):
    FONTS_ROOT = os.path.join(Const.BASE_DIR, "Fonts")
    FONTS = {
        "impact": os.path.join(FONTS_ROOT, "impact", "impact.ttf"),
        "arial": os.path.join(FONTS_ROOT, "arial", "arial.ttf"),
    }

    IMAGES_PATH = os.path.join(Const.BASE_DIR, "Images")
    IMAGES_TMP_PATH = os.path.join(IMAGES_PATH, "Temp")
    IMAGES_TEMPLATE_PATH = os.path.join(IMAGES_PATH, "PNG")

    IMGUR_CLIENT_ID = "9ff97800dfceb1e"
    IMGUR_CLIENT_SECRET = "7cfb78f7dfbf5397fe5638e66d787164ed497166"