# App installation script
# Usage: sudo python ./scripts/appInstaller.py <sourceType> <source> [customManifest.yaml]
# Args:
#   - sourceType: Either "github" or "local". Local refers to a directory on the local machine
#   - source: Github repository or local directory where app package is stored
#   - OPTIONAL: customManifest.yaml: Use a custom manifest file instead of the manifest bundled with the app
#

import yaml
import sys

sourceType = sys.argv[1]
source = sys.argv[2]

try:
    customManifest = sys.argv[3]
except IndexError:
    customManifest = False

if sourceType != "local" and sourceType != "github":
    exit(1)


