# OpoSqueue v0.1.0

## Introduction
OpoSqueue (or OpoSQ for short), is a Python-based CLI tool that allows the user to connect to a remtoe server (through SSH) and monitor the HPC jobs that are currently running and queued. If you are tired of typing "squeue" every other minute to check the status of your analysis, just run OpoSqueue through your Command Line and enjoy a window that will update every 5 seconds with the nodes status!

This tool is expected to get soon other updates, mostly regarding its appearance, but if you have any suggestions regarding additional functionalities that could be useful for your every-day work, feel free to contact me.

## 0. Set-Up
GUI support is required on the user system, so it is recommended to install opoSqueue on your local computer, not on the cluster login node. Your computer will also need Python >=3.11, so make sure to have the correct version (run `python --version`) or [download it](https://www.python.org/downloads/). To install this package simply clone the repository running this command through the Terminal:

```bash
pip install git+https://github.com/flavialeotta/opoSqueue.git
```

The installation will automatically take care of the dependencies, but it is also possible to manually install them by running the command:

```bash
pip install requirements.txt
```

## 1. How to run
To run opoSqueue simply type:

```bash
oposqueue
```

and you're good to go!

### Save your connection details

### Access saved connections

### Main window

## 2. Components
Package asyncio:

1. Synchronous functions
If you define a function using def async function(), the function becomes a 'coroutine', which means it is allowed to pause and wait for things. It will need 'await' which is like a pause button. 

Once this function is defined, you need asyncio.run() to run it: this type of function starts the event loop, puts the function inside it and ,manages all pauses and starts of it until you close the program.

In my main application there are two loops:
1. UI: waits for the user to click buttons. Controlled by QEventLoop(app)
2. Async: needs to check if SSH data has arrived. Controlled by asyncio.set_event_loop(loop)


Components of opoSqueue:
1. main.py
- function async main():
    a. creates the application using app = Qapplication(sys.argv);
    b. puts the app into a loop using loop = Qeventloop(app);
    c. starts a window calling TitleScreen();
    d. loops the app forever with loop.run_forever().

2. ui/window/titlescreen.py
- class TitleScreen():

## 3. Possible problems
### WARNING: The script oposqueue.exe is installed in '...' which is not on PATH.
This is usually a local configuration problem, which can be easily solved. Locate the path that is provided by the warning message (usually something along the line of 'C:\Users\name of the user\intermediate folders\Python\pythoncore-version\Scripts')

Run this PowerShell command:

```PowerShell
[Environment]::SetEnvironmentVariable("Path", $env:Path + "; path given by the error message", "User")
```

Do not change "User" for your user name. Then, restart your Terminal window.

## 4. Contacts

