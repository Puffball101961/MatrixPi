# Usage: python checkColourMapping.py rows cols mapping colourMap

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw
import sys
import time

rows = int(sys.argv[2])
cols = int(sys.argv[3])
mapping = sys.argv[4]
colourMap = sys.argv[5]

options = RGBMatrixOptions()
options.rows = rows # height of the display
options.cols = cols # width of the display
options.parallel = 1
options.led_rgb_sequence = colourMap
options.hardware_mapping = mapping

matrix = RGBMatrix(options = options)

time.sleep(4)

# Display Test Pattern
splash = Image.new('RGBA', (cols, rows))
draw = ImageDraw.Draw(splash)
draw.rectangle((0,0,cols,rows), fill=(255,0,0)) # RED
matrix.SetImage(splash.convert('RGB'))
time.sleep(1)
matrix.Clear()
splash = Image.new('RGBA', (cols, rows))
draw = ImageDraw.Draw(splash)
draw.rectangle((0,0,cols,rows), fill=(0,255,0)) # GREEN
matrix.SetImage(splash.convert('RGB'))
time.sleep(1)
matrix.Clear()
splash = Image.new('RGBA', (cols, rows))
draw = ImageDraw.Draw(splash)
draw.rectangle((0,0,cols,rows), fill=(0,0,255)) # BLUE
matrix.SetImage(splash.convert('RGB'))
time.sleep(1)
matrix.Clear()