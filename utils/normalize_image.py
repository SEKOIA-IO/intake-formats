import math
import io
import os
from pathlib import Path

from PIL import Image
import numpy as np
import typer

INTAKES_PATH = os.path.dirname(os.path.dirname(__file__))


def get_logo_path(base_path: Path, temp: bool = False) -> Path:
    image_name = "logo.png" if not temp else "logo_tmp.png"

    return base_path / "_meta" / image_name


def replace_image(original: Path, new_image: Path) -> None:
    os.remove(original)
    os.rename(new_image, original)


def transparent_background(image: Image, fuzz: int) -> Image:
    """
    Replace white background into transparent background
    """
    x = np.asarray(image.convert('RGBA')).copy()

    threshold = int(255 * (100 - fuzz) / 100)

    r, g, b, a = np.rollaxis(x, axis=-1)  # split into 4 n x m arrays
    r_m = r < threshold  # binary mask for red channel, True for all non white values
    g_m = g < threshold  # binary mask for green channel, True for all non white values
    b_m = b < threshold  # binary mask for blue channel, True for all non white values

    # combine the three masks using the binary "or" operation 
    # multiply the combined binary mask with the alpha channel
    a = a * ((r_m == 1) | (g_m == 1) | (b_m == 1))

    # stack the img back together 
    return Image.fromarray(np.dstack([r, g, b, a]), 'RGBA')


def resize_canvas(image: Image, canvas_width: int = 500, canvas_height: int = 500) -> Image:
    """
    Resize the canvas of the image

    Args:
        image: Image
        canvas_width: int
        canvas_height: int

    Returns:
        Image:
    """
    old_width, old_height = image.size

    # Center the image
    x1 = int(math.floor((canvas_width - old_width) / 2))
    y1 = int(math.floor((canvas_height - old_height) / 2))

    # Compute background according the image mode
    mode = image.mode
    new_background: float | tuple[float, ...] | str | None = None

    match mode:
        case "L" | "1":
            new_background = 255
        case "RGB" | "RGBA" | "CMYK":
            new_background = (255, 255, 255, 0)

    # Create new image and paste the original into
    new_image = Image.new(mode, (canvas_width, canvas_height), new_background)
    new_image.paste(image, (x1, y1, x1 + old_width, y1 + old_height))

    return new_image


def square_canvas(image: Image) -> Image:
    """
    Square the canvas of the image

    Args:
        image: Image

    Returns:
        Image:
    """
    max_size = max(image.size)

    return resize_canvas(image, max_size, max_size)


def lighten_image(original: Image, size: int, max_iteration: int = 100) -> Image:
    """
    Downsize the image until its weight is lesser than the supplied parameter

    Args:
        original: Image
        size: int
        max_iteration: int

    Returns:
        Image:
    """
    image = original.copy()

    for _ in range(max_iteration):
        buffer = io.BytesIO()
        image.save(buffer, "png")
        current_size = len(buffer.getvalue())

        if current_size <= size:
            return image

        ratio = (size / current_size)
        width, height = image.size
        image = image.resize((int(width * ratio), int(height * ratio)))

    raise Exception("Unable to resize the image in the maximum iteration")


app = typer.Typer()


@app.command("transparent_background")
def cli_transparent_background(source: Path, destination: Path, fuzz: int = 0):
    """
    Transform the white background into transparent one
    """
    transparent_background(Image.open(source), fuzz).save(destination)


@app.command("resize_canvas")
def cli_resize_canvas(source: Path, destination: Path, canvas_width: int = 500, canvas_height: int = 500):
    """
    Resize the canvas of the image
    """
    resize_canvas(Image.open(source), canvas_width=canvas_width, canvas_height=canvas_height).save(destination)


@app.command("square_canvas")
def cli_square_canvas(source: Path, destination: Path):
    """
    Square the canvas of the image
    """
    square_canvas(Image.open(source)).save(destination)


@app.command("lighten_image")
def cli_lighten_image(source: Path, destination: Path, size: int = 50000):
    """
    Downsize the image until its weight is lesser than the supplied parameter 
    """
    lighten_image(Image.open(source), size).save(destination)


@app.command("normalize_image")
def cli_normalize_image(source: Path, destination: Path, fuzz: int = 0, ligthen_image: bool = True, size: int = 50000):
    """
    Normalize the image

    - transform white background into transparent one
    - square the canvas
    - downsize the image until its weight is lesser than the supplied parameter
    """
    image = square_canvas(transparent_background(Image.open(source), fuzz))

    if ligthen_image:
        image = lighten_image(image, size)

    image.save(destination)


@app.command("normalize_logo")
def cli_normalize_logo(module: str | None = None, format: str | None = None):
    if not module and not format:
        raise ValueError("module or format is required")

    logo: Path | None = None
    new_logo: Path | None = None

    if module:
        for subdir in os.listdir(INTAKES_PATH):
            if subdir == module:
                module_path = os.path.join(INTAKES_PATH, subdir)
                logo = get_logo_path(Path(module_path), temp=False)
                new_logo = get_logo_path(Path(module_path), temp=True)

    if format:
        for subdir in os.listdir(INTAKES_PATH):
            module_path = os.path.join(INTAKES_PATH, subdir)
            if os.path.isdir(module_path):
                for format_dir in os.listdir(module_path):
                    if format_dir == format:
                        format_path = os.path.join(module_path, format_dir)

                        logo = get_logo_path(Path(format_path), temp=False)
                        new_logo = get_logo_path(Path(format_path), temp=True)
    if logo and new_logo:
        cli_normalize_image(logo, new_logo, ligthen_image=True, size=50000)
        replace_image(logo, new_logo)

        return
    raise ValueError("module or format not found")


if __name__ == "__main__":
    # Example of usage:
    # poetry run python normalize_image.py normalize_logo --module=Ubika
    # poetry run python normalize_image.py normalize_logo --format=windows

    app()
