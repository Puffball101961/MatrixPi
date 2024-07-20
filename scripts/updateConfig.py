# CLI: python3 ./scripts/updateConfig.py width height driver colour

import sys
import yaml

width = sys.argv[1]
height = sys.argv[2]
driver = sys.argv[3]
colour = sys.argv[4]

configVals = {
    "MATRIX_WIDTH":int(width),
    "MATRIX_HEIGHT":int(height),
    "MATRIX_DRIVER":driver,
    "MATRIX_COLOUR":colour,
}

with open ("./scripts/main.config", "r") as file:
    config = yaml.safe_load(file)
    
for val in configVals.keys():
    config[val] = configVals[val]
    
with open ("./scripts/main.config", "w") as file:
    yaml.safe_dump(config, file, sort_keys=False)
    
