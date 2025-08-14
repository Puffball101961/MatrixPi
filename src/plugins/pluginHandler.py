import os
import importlib
import inspect


PLUGINS = {}
PLUGIN_INSTANCES = {}
IGNORE = ['__init__.py', '__pycache__', 'base']

def loadPlugins(pluginDir) -> None:
    # Get all directories in the plugin directory
    for plugin_name in os.listdir(pluginDir):
        if plugin_name in IGNORE:
            continue
        
        plugin_path = os.path.join(pluginDir, plugin_name)
        
        # Check if it's a directory
        if os.path.isdir(plugin_path):
            try:
                # Dynamically import the plugin module
                module = importlib.import_module(f'plugins.{plugin_name}.{plugin_name}')
                
                # Check for classes in the module that inherit from PluginBase
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if 'PluginBase' in [base.__name__ for base in obj.__bases__]:
                        PLUGINS[name] = obj
                        print(f"Loaded plugin: {plugin_name} ({name})")
                        
            except Exception as e:
                print(f"Failed to load plugin {plugin_name}: {e}")

def initialisePlugins(FPS) -> None:
    global PLUGIN_INSTANCES
    plugins = PLUGINS
    pluginInstances = {}
    for pluginName, pluginClass in plugins.items():
        try:
            pluginInstance = pluginClass(FPS)
            pluginInstances[pluginName] = pluginInstance
            print(f"Plugin {pluginName} initialised successfully.")
        except Exception as e:
            print(f"Failed to initialise plugin {pluginName}: {e}")
    
    PLUGIN_INSTANCES = pluginInstances