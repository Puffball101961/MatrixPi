from PIL import Image, ImageFont, ImageDraw
import time
import os
import yaml

from plugins.base.pluginBase import PluginBase


class Clock(PluginBase):
    def __init__(self, FPS):
        self.PLUGIN_DIR = os.path.dirname(__file__)
        self.FPS = FPS
        
    def generateFrameSequence(self):
        image = Image.new('RGBA', (128,32))
        draw = ImageDraw.Draw(image)
        
        draw.text((1,0), time.strftime("%I:%M %p"), font=ImageFont.load(self.PLUGIN_DIR + "/fonts/10x20.pil"), fill=(255,255,255, 0))
        draw.text((1,20), time.strftime("%a %d/%m/%Y"), font=ImageFont.load(self.PLUGIN_DIR + "/fonts/6x10.pil"), fill=(255,255,255))
        
        return [image]