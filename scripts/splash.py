# Splash Screen

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
# from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageFilter
import sys
import time

rows = int(sys.argv[1])
cols = int(sys.argv[2])
mapping = sys.argv[3]

options = RGBMatrixOptions()
options.rows = rows # height of the display
options.cols = cols # width of the display
options.parallel = 1
options.led_rgb_sequence = "RBG"
options.hardware_mapping = mapping

matrix = RGBMatrix(options = options)

nameFont = ImageFont.load("./fonts/6x10.pil")

# Display Test Text
splash = Image.new('RGBA', (cols, rows))
draw = ImageDraw.Draw(splash)
draw.text((1,0), "MatrixPi v0.0.0", font=nameFont, fill=(255,255,255))
matrix.SetImage(splash.convert('RGB'))
time.sleep(5)
matrix.Clear()