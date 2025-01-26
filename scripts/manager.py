# MatrixPi System Manager
# sudo fastapi run ./scripts/manager.py --host 0.0.0.0 --port 8000

import os
import subprocess
import time
import signal

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from contextlib import asynccontextmanager
import yaml

with open('./apps/library.yaml', 'r') as file:
    appLib = yaml.safe_load(file)

APP_DIRECTORY = {}
APP_NAMES = {}

for app in appLib['apps']:
    APP_DIRECTORY[app] = appLib['apps'][app]['executable']
    APP_NAMES[app] = appLib['apps'][app]['name']

with open('./scripts/main.config', 'r') as file:
    mainConf = yaml.safe_load(file)


BOOT_APP =  mainConf['BOOT_APP']
MATRIX_ARGS = ""
MATRIX_ARGS += str(mainConf["MATRIX_HEIGHT"]) + " " + str(mainConf["MATRIX_WIDTH"]) + " " + mainConf["MATRIX_DRIVER"]
APP_CRASH_LIMIT = 10

procList = []

# Splash screen
# os.chdir("/home/pi/MatrixPi")
os.system(f"sudo python3 ./scripts/splash.py {MATRIX_ARGS}")


def killApp(): 
    for app in procList:
        try:
            os.kill(os.getpgid(app.pid), signal.SIGTERM)
            procList.pop()
        except:
            pass

def spawnApp(appName):
    if appName not in APP_NAMES.keys():
        return False

    appID = appName
    appName = APP_NAMES[appName]

    if (appLib['apps'][appID]['language'] == "py"):
        args = ["sudo", "python3", f"./apps/{appID}/{APP_DIRECTORY[appID]}.py"]
    elif (appLib['apps'][appID]['language'] == "cpp"):
        args = ["sudo", f"./apps/{appID}/{APP_DIRECTORY[appID]}.app"]
    else:
        return False
    
    args.extend(MATRIX_ARGS.split(" "))
    app = subprocess.Popen(args, cwd=os.getcwd(), start_new_session=True)
    return app

def getRunningAppName(app):
    return app.args[2].split('/')[2]

def checkIfAppIDIsValid(appID):
    return appID in APP_NAMES.keys()

procList.append(spawnApp(BOOT_APP))

api = FastAPI()

@api.on_event("shutdown") # TODO: Deprecated apparently, find a way to make work with lifecycle manager
async def shutdownApps():
    killApp()

@api.get("/")
async def root():
    return {"message": "matrixpi backend api is operational"}

@api.get("/startApp")
def getStartApp(appID: str = BOOT_APP):
    if checkIfAppIDIsValid(appID):
        killApp()
        procList.append(spawnApp(appID))
        return {"success":f"{appID} started"}
    else:
        return {"failure":"appID invalid"}

@api.get("/closeApp")
def getCloseApp():
    killApp()
    print(APP_NAMES)
    procList.append(spawnApp(BOOT_APP)) # Spawn the home app
    return {"success":"app closed"}

@api.get("/currentApp")
async def getCurrentApp():
    return {"success": getRunningAppName(procList[0])}

@api.get("/info")
async def getInfo():
    with open('version', 'r') as f:
        ver = f.read()
    return {
        "version":ver,
        "runningApp":getRunningAppName(procList[0]),
        "appLibrary":APP_DIRECTORY
    }

@api.on_event("startup") # TODO: Deprecated apparently, find a way to make work with lifecycle manager
@repeat_every(seconds=5)
def checkProcHealth():
    crashCount = 0
    while procList[0].poll() != None:
        print(f"app crash: {procList[0].poll()}")
        if crashCount >= APP_CRASH_LIMIT:
            os.system("sudo systemctl restart matrixpi") # Uncomment for prod
        killApp()
        spawnApp()
        crashCount += 1        
    
