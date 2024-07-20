# MatrixPi System Manager

import os
import subprocess
import time
import signal

from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

APP_DIRECTORY = { # "directoryName":"executableName"
    "home":"home",
    "test":"testApp"
}
BOOT_APP = "home"
MATRIX_ARGS = "--led-no-hardware-pulse 32 128 adafruit-hat"

# Splash screen
os.chdir("/home/pi/MatrixPi")
os.system(f"sudo python3 ./scripts/splash.py {MATRIX_ARGS}")


def killApp(app): 
    global runningApp
    # TODO: Add checks for non-existent app
    os.kill(os.getpgid(app.pid), signal.SIGTERM)

def spawnApp(appName):
    # TODO: Add checks for app already running
    if appName not in APP_DIRECTORY.keys():
        return False
    args = ["sudo", "python3", f"./apps/{appName}/{APP_DIRECTORY[appName]}.py"]
    args.extend(MATRIX_ARGS.split(" "))
    app = subprocess.Popen(args, cwd=r'/home/pi/MatrixPi', start_new_session=True)
    return app

def getRunningAppName(app):
    return app.args[2].split('/')[2]

runningApp = spawnApp(BOOT_APP)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global runningApp
    print("Starting up!")
    yield
    killApp(runningApp)

api = FastAPI(lifespan=lifespan)

@api.get("/")
async def root():
    return {"message": "matrixpi backend api is operational"}

@api.get("/startApp")
async def getStartApp(appName: str = "home"):
    global runningApp
    killApp(runningApp)
    runningApp = spawnApp(appName)
    return {"success":f"{appName} started"}

@api.get("/closeApp")
async def getCloseApp():
    global runningApp
    killApp(runningApp)
    runningApp = spawnApp("home")
    return {"success":"app closed"}