"""Module to handle font loading and identification utilities."""

from PIL import ImageFont

font: ImageFont.FreeTypeFont = ImageFont.truetype("assets/UniverseCondensed.ttf", 24)


def display_font_metadata(font_instance: ImageFont.FreeTypeFont) -> None:
    """Logs the identifying name of the provided font instance to the console.

    Args:
        font_instance: The initialized FreeTypeFont object to inspect.
    """
    print(font_instance.getname())


display_font_metadata(font)
