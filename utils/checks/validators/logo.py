import argparse
import os

from . import Validator
from .constants import CheckResult


class LogoValidator(Validator):
    @classmethod
    def validate(cls, result: CheckResult, args: argparse.Namespace) -> None:
        if not result.options.get("meta_dir"):
            return

        module_meta_dir = result.options["meta_dir"]
        logo_path = os.path.join(module_meta_dir, "logo.png")

        check_logo_image(image_path=logo_path, result=result)


def check_logo_image(image_path: str, result: CheckResult) -> None:
    from PIL import Image

    def has_transparency(img: Image):
        if img.info.get("transparency", None) is not None:
            return True

        elif img.mode == "P":
            transparent = img.info.get("transparency", -1)
            for _, index in img.getcolors():
                if index == transparent:
                    return True

        elif img.mode == "RGBA":
            extrema = img.getextrema()
            if extrema[3][0] < 255:
                return True

        return False

    if not os.path.isfile(image_path):
        result.errors.append(f"Logo (`{image_path}`) is missing")
        return

    image = Image.open(image_path)
    if image.format != "PNG":
        result.errors.append("Logo is not in PNG format")

    if image.width != image.height:
        result.errors.append(f"Logo is not square - {image.width}x{image.height}px")

    if not has_transparency(image):
        result.errors.append("Logo background is not transparent")

    if os.path.getsize(image_path) > 50 * 1024:
        result.errors.append("Logo file weights more than 50 KiB")

    image.close()

    result.options["logo_path"] = image_path
