# Usage: python checkHardwareMapping.py --led-no-hardware-pulse rows cols mapping

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageFont, ImageDraw
import sys
import time

rows = int(sys.argv[2])
cols = int(sys.argv[3])
mapping = sys.argv[4]

options = RGBMatrixOptions()
options.rows = rows # height of the display
options.cols = cols # width of the display
options.parallel = 1
options.led_rgb_sequence = "RBG"
options.hardware_mapping = mapping


nameFont = ImageFont.load("./pil/6x10.pil")

matrix = RGBMatrix(options = options)

# Display Test Text
splash = Image.new('RGBA', (cols, rows))
draw = ImageDraw.Draw(splash)
draw.text((1,0), "MatrixPi", font=nameFont, fill=(255,255,255))
matrix.SetImage(splash.convert('RGB'))
time.sleep(5)
matrix.Clear()