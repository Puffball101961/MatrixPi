# App installation script
# Usage: sudo python ./scripts/appInstaller.py <sourceType> <source>
# Args:
#   - sourceType: Either "github" or "local". Local refers to a directory on the local machine
#   - source: Github repository or local directory where app package is stored
#

# TODO: Support github sources

import yaml
import sys
import os
import shutil

sourceType = sys.argv[1]
source = sys.argv[2]

try:
    customManifest = sys.argv[3]
except IndexError:
    customManifest = False

if sourceType != "local" and sourceType != "github":
    exit(1)

# Verify folder exists
if (not os.path.isdir(source)):
    print("Invalid Directory")
    exit(1)
    
source = os.path.abspath(source) # Change source to absolute path
    
print("Installing app from directory: " + os.path.abspath(source))

# Verify Manifest
print("Verifying manifest")

with open(os.path.join(source, "manifest.yaml"), 'r') as file:
    manifest = yaml.safe_load(file)

class InvalidOption(Exception):
    pass

try:
    name = list(manifest.keys())[0]
    appid = manifest[name]['appid']
    language = manifest[name]['language']
    if (language != "py" and language != "cpp"):
        raise(InvalidOption)
    executable = manifest[name]['executable']
    humanName = manifest[name]['humanName']
    description = manifest[name]['description']
    author = manifest[name]['author']
    version = manifest[name]['version']
except (KeyError, InvalidOption):
    print("Manifest verification failed")
    exit(1)
    
file.close()
    
print("Manifest verified")

# Check if app installed already
with open("./apps/library.yaml", 'r') as file:
    appLibrary = yaml.safe_load(file)
    
update = False 

for app in appLibrary['apps']:
    if appid == app: # App already installed
        oldVer = appLibrary['apps'][app]['version']
        if version > oldVer:
            update = True
            break
        else:
            print("Installation failed, downgrading app not allowed using appInstaller.")
            exit(1)


if update:
    print(f"App already installed, proceeding with app update to version: v{version} over v{oldVer}")
else:
    print("App not presently installed, proceeding with clean install")
    
file.close()
    
# Copy files
shutil.copytree(source, os.path.join('./apps/', appid), dirs_exist_ok=True)

if (not os.path.isdir(os.path.join('./apps/', appid))): # Check that the directory copied
    print("General copy failure")
    exit(1)
    
# Assume that files copied OK
# Update library.yaml

newData = {
    appid: {
        "name": name,
        "language": language,
        "executable": executable,
        "humanName": humanName,
        "description": description,
        "author": author,
        "version": version
    }
}

with open("./apps/library.yaml", "r") as file:
    currLibrary = yaml.safe_load(file)
    currLibrary['apps'].update(newData)

if currLibrary:
    with open ("./apps/library.yaml", "w") as file:
        yaml.safe_dump(currLibrary, file, sort_keys=False)
file.close()