# Home App

# from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageFilter
import sys
import time

# rows = int(sys.argv[2])
# cols = int(sys.argv[3])
# mapping = sys.argv[4] # UNCOMMENT FOR PROD


# TEMP
rows = 32
cols = 128
mapping = 'adafruit-hat'

options = RGBMatrixOptions()
options.rows = rows # height of the display
options.cols = cols # width of the display
options.parallel = 1
options.led_rgb_sequence = "RBG"
options.hardware_mapping = mapping

matrix = RGBMatrix(options = options)

# Main loop
while True:
    image = Image.new('RGBA', (128,32))
    draw = ImageDraw.Draw(image)
    
    
    draw.text((1,0), time.strftime("%I:%M %p"), font=ImageFont.load("./fonts/10x20.pil"), fill=(255,255,255))
    draw.text((1,20), time.strftime("%a %d/%m/%Y"), font=ImageFont.load("./fonts/6x10.pil"), fill=(255,255,255))
    
    matrix.Clear()
    matrix.SetImage(image.convert('RGB'))
    
    time.sleep(60-time.localtime().tm_sec)

matrix.Clear()