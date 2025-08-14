# Abstact base class for plugins in MatrixPi

class PluginBase:        
    def __init__(self, FPS):
        self.PLUGIN_DIR = None
        self.FPS = FPS
        
    def generateFrameSequence() -> list:
        NotImplementedError("Implement me in sub-classes!")