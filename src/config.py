import json
from datetime import datetime

class Config:
    configKeys = []
    acceptableVersions = []
    
    def __init__(self, configFile):
        self.configFile = configFile
        self.config = self.loadConfig()
    
    def loadConfig(self):
        try:
            with open(self.configFile, 'r') as file:
                configData = json.load(file)
            
            if not isinstance(configData, dict):
                raise ValueError("Config data must be a dictionary")
            
            if "version" not in configData or configData["version"] not in self.acceptableVersions:
                raise ValueError(f"Invalid version: {configData.get('version', 'None')}. Acceptable versions: {self.acceptableVersions}")
            
            for key in self.configKeys:
                if key not in configData:
                    raise KeyError(f"Missing required config key: {key}")
            
            return configData
        
        except (FileNotFoundError, json.JSONDecodeError, ValueError, KeyError) as e:
            print(f"Error loading config: {e}")
            return None


class MatrixConfig(Config):
    configKeys = ["version", "matrixWidth", "matrixHeight", "matrixColourMapping", "matrixDriver"]
    acceptableVersions = [1]


class SleepingConfig(Config):
    configKeys = ["version", "sleepingEnabled", "startTime", "endTime", "brightness"]
    acceptableVersions = [1]
    
    def loadConfig(self):
        configData = super().loadConfig()
        if configData is not None:
            # Validate time formats
            for key in ["startTime", "endTime"]:
                try:
                    datetime.strptime(configData[key], "%H:%M")
                except ValueError:
                    print(f"Invalid time format for {key}: {configData[key]}. Expected format: HH:MM")
                    return None
        return configData

    def isSleeping(self):
        if not self.config or not self.config['sleepingEnabled']:
            return False

        current_time = datetime.now().time()
        start_time = datetime.strptime(self.config['startTime'], "%H:%M").time()
        end_time = datetime.strptime(self.config['endTime'], "%H:%M").time()

        if start_time <= end_time:
            return start_time <= current_time <= end_time
        else:
            return current_time >= start_time or current_time <= end_time


class PlaylistConfig(Config):
    configKeys = ["version", "playlists"]
    acceptableVersions = [1]
    
    def __init__(self, configFile, pluginNames):
        self.pluginNames = pluginNames
        super().__init__(configFile)

    def loadConfig(self):
        configData = super().loadConfig()
        if configData is not None:
            for playlist in configData['playlists']:
                required_keys = ["name", "default", "changeEvery", "startTime", "endTime", "plugins"]
                if not all(k in playlist for k in required_keys):
                    print(f"Invalid playlist configuration: {playlist}")
                    return None
                
                # Check for at least one default=true playlist
                if not any(p['default'] for p in configData['playlists']):
                    print("At least one playlist must have 'default' set to true.")
                    return None
                
                try:
                    datetime.strptime(playlist['startTime'], "%H:%M")
                    datetime.strptime(playlist['endTime'], "%H:%M")
                except ValueError:
                    print(f"Invalid time format in playlist '{playlist.get('name', '')}': {playlist['startTime']} or {playlist['endTime']}. Expected format: HH:MM")
                    return None
                
                for plugin in playlist['plugins']:
                    if plugin not in self.pluginNames:
                        print(f"Plugin '{plugin}' not found in available plugins: {self.pluginNames}")
                        return None
            
            # Check to make sure time intervals do not overlap
            for i, playlist in enumerate(configData['playlists']):
                start_time = datetime.strptime(playlist['startTime'], "%H:%M")
                end_time = datetime.strptime(playlist['endTime'], "%H:%M")
                
                for j, other_playlist in enumerate(configData['playlists']):
                    if i != j:
                        other_start_time = datetime.strptime(other_playlist['startTime'], "%H:%M")
                        other_end_time = datetime.strptime(other_playlist['endTime'], "%H:%M")
                        
                        if (start_time < other_end_time and end_time > other_start_time):
                            print(f"Time intervals overlap between playlists '{playlist['name']}' and '{other_playlist['name']}'")
                            return None
        return configData
