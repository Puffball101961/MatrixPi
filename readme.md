<img src="media/header.png">

# MatrixPi: An RGB Matrix app framework Powered by Raspberry Pi
<img src="https://img.shields.io/badge/License-GNU_GPLv3-blue">

## App List
- Home (Core)
- Testing App

## App Repository Structure
Apps can be written in Python (recommended) or C++. 
If using C++, the app must be compiled and the executable in the app directory must be in the format `<appName>.app`
C++ Support is extremely limited at the moment.
```
app-name/
├─ executable
├─ manifest.yaml
├─ assets/ (your internal app configs/ assets/ whatever, optional)
│  ├─ config.yaml
│  ├─ background.png
│  ├─ ...
```
## App Manifests
Each app must have an app manifest. This has general information about the app, including its name, version, author, and whether the app is in Python or C++.
The app manifest must also include a unique `appID`. This is crucial so the app doesn't conflict with others. Currently, the built-in apps use a random 32 character long hex string.

## Installing Apps
Use `sudo python ./scripts/appInstaller.py <sourceType> <source>`
- There is currently no mechanism to uninstall apps.
- The only valid source type right now is "local". Git support is planned.
- When using the local source type, provide the full directory of the package to be installed as the source argument.

## Manual App Installation Procedure
1. Clone your app into the `apps` directory
2. Add your app manifest details into the app library yaml (`library.yaml`)
3. Start your app by accessing the internal API, `https://ip-address-of-pi:8000/startApp?appID=appID`