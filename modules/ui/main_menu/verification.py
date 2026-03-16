from PIL import ImageFont

# Load a specific TrueType font file from the assets directory with a size of 24
# The font variable holds an instance of FreeTypeFont
font: ImageFont.FreeTypeFont = ImageFont.truetype("assets/UniverseCondensed.ttf", 24)

# Print the name of the loaded font to the console
print(font.getname())
