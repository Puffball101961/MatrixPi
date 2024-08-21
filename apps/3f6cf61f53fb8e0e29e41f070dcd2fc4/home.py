# Home App

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
# from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageFilter
import sys
import time
import yaml

rows = int(sys.argv[1])
cols = int(sys.argv[2])
mapping = sys.argv[3] # UNCOMMENT FOR PROD

# TEMP
# rows = 32
# cols = 128
# mapping = 'adafruit-hat'

options = RGBMatrixOptions()
options.rows = rows # height of the display
options.cols = cols # width of the display
options.parallel = 1
options.led_rgb_sequence = "RBG"
options.hardware_mapping = mapping

matrix = RGBMatrix(options = options)

with open ("./apps/home/config/config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

CONFIG_SLEEP_START = cfg['sleepStart']
CONFIG_SLEEP_BRIGHTNESS = cfg['sleepBrightness']
CONFIG_SLEEP_END = cfg['sleepEnd']
CONFIG_AWAKE_BRIGHTNESS = cfg['awakeBrightness']


# Main loop
while True:
    if time.localtime().tm_hour >= CONFIG_SLEEP_END and time.localtime().tm_hour < CONFIG_SLEEP_START:
        matrix.brightness = CONFIG_AWAKE_BRIGHTNESS
    else:
        matrix.brightness = CONFIG_SLEEP_BRIGHTNESS
    
    image = Image.new('RGBA', (128,32))
    draw = ImageDraw.Draw(image)
    
    draw.text((1,0), time.strftime("%I:%M %p"), font=ImageFont.load("./fonts/10x20.pil"), fill=(255,255,255))
    draw.text((1,20), time.strftime("%a %d/%m/%Y"), font=ImageFont.load("./fonts/6x10.pil"), fill=(255,255,255))
    
    matrix.Clear()
    matrix.SetImage(image.convert('RGB'))
    
    time.sleep(60-time.localtime().tm_sec)