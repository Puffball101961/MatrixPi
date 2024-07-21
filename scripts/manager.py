# MatrixPi System Manager
# sudo fastapi run ./scripts/manager.py --host 0.0.0.0 --port 8000

import os
import subprocess
import time
import signal

from fastapi import FastAPI
from contextlib import asynccontextmanager
import yaml

with open('./apps/library.yaml', 'r') as file:
    appLib = yaml.safe_load(file)

APP_DIRECTORY = {}

for app in appLib['apps']:
    APP_DIRECTORY[app] = appLib['apps'][app]['executable']

with open('./scripts/main.config', 'r') as file:
    mainConf = yaml.safe_load(file)


BOOT_APP =  mainConf['BOOT_APP']
MATRIX_ARGS = ""
MATRIX_ARGS += str(mainConf["MATRIX_HEIGHT"]) + " " + str(mainConf["MATRIX_WIDTH"]) + " " + mainConf["MATRIX_DRIVER"]

procList = []

# Splash screen
os.chdir("/home/pi/MatrixPi")
os.system(f"sudo python3 ./scripts/splash.py {MATRIX_ARGS}")


def killApp(): 
    for app in procList:
        try:
            os.kill(os.getpgid(app.pid), signal.SIGTERM)
        except:
            pass

def spawnApp(appName):
    if appName not in APP_DIRECTORY.keys():
        return False
    args = ["sudo", "python3", f"./apps/{appName}/{APP_DIRECTORY[appName]}.py"]
    args.extend(MATRIX_ARGS.split(" "))
    app = subprocess.Popen(args, cwd=r'/home/pi/MatrixPi', start_new_session=True)
    return app

def getRunningAppName(app):
    return app.args[2].split('/')[2]

# runningApp = spawnApp(BOOT_APP)
procList.append(spawnApp(BOOT_APP))

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up!")
    yield
    killApp()

api = FastAPI(lifespan=lifespan)

@api.get("/")
async def root():
    return {"message": "matrixpi backend api is operational"}

@api.get("/startApp")
def getStartApp(appName: str = "home"):
    killApp()
    procList.append(spawnApp(appName))
    return {"success":f"{appName} started"}

@api.get("/closeApp")
def getCloseApp():
    killApp()
    procList.append(spawnApp("home"))
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
