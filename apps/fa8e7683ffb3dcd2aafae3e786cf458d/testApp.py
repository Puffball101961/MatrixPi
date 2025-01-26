# Dummy home.py file for testing
# python home.py rows cols mapping colourMap

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

nameFont = ImageFont.load("./apps/fa8e7683ffb3dcd2aafae3e786cf458d/pil/6x10.pil")

splash = Image.new('RGBA', (cols, rows))
draw = ImageDraw.Draw(splash)
draw.text((1,0), "Test App!", font=nameFont, fill=(255,255,255))
matrix.SetImage(splash.convert('RGB'))

# Main loop
while True:
    time.sleep(1)

matrix.Clear()