import argparse
import os
from pathlib import Path

from . import INTAKES_PATH, Validator
from .constants import CheckResult


class LogoValidator(Validator):
    @classmethod
    def validate(cls, result: CheckResult, args: argparse.Namespace) -> None:
        if not result.options.get("meta_dir"):
            return

        module_meta_dir: Path = result.options["meta_dir"]
        logo_path = module_meta_dir / "logo.png"

        check_logo_image(image_path=logo_path, result=result)


def check_logo_image(image_path: Path, result: CheckResult) -> None:
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

    if not image_path.is_file():
        result.errors.append(
            f"Logo (`{image_path.relative_to(INTAKES_PATH)}`) is missing"
        )
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
