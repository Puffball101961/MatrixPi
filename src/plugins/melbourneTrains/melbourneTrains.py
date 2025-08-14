from PIL import Image, ImageFont, ImageDraw
import os
import plugins.melbourneTrains.serviceAlerts as serviceAlerts
import plugins.melbourneTrains.stationDepartures as stationDepartures
from datetime import datetime

from plugins.base.pluginBase import PluginBase

STATION_NAME = "Sunbury Station"
TRAIN_LINES = ["Sunbury", "Pakenham"]


class MelbourneTrains(PluginBase):
    def __init__(self, FPS):
        self.PLUGIN_DIR = os.path.dirname(__file__)
        self.FPS = FPS
        self.lineStatuses = {}
        self.getServiceAlerts()
        self.getDepartures()
        
    def generateFrameSequence(self):
        self.getDepartures()
        sequence = []
        
        for i in range(5):  # Generate 5 frames
            image = Image.new('RGBA', (128, 32))
            draw = ImageDraw.Draw(image)
            
            draw.text((1, 1), f"{datetime.strftime(datetime.now(), "%H:%M:%S %d/%m/%Y")}", font=ImageFont.load(self.PLUGIN_DIR + "/fonts/5x7.pil"), fill=(255, 255, 255, 0))
            
            sequence.append(image)

        return sequence
    
    def getServiceAlerts(self):
        self.serviceAlerts = serviceAlerts.fetch_and_parse_feed()
        for line, info in sorted(self.serviceAlerts.items()):
            if line in TRAIN_LINES:
                self.lineStatuses[line] = info
                
    def getDepartures(self):
        self.invStationIDs, self.filteredDepartures, self.tripNames = stationDepartures.processData(STATION_NAME, self.PLUGIN_DIR)
        
            
# Debugging
if __name__ == "__main__":
    plugin = MelbourneTrains()
