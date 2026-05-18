# OpoSqueue v0.1.0

## Introduction
OpoSqueue (or OpoSQ for short), is a Python-based CLI tool that allows the user to connect to a remote server (through SSH) and monitor the HPC jobs that are currently queued and running. If you are tired of typing "squeue" every other minute to check the status of your analysis, just run OpoSqueue through your Command Line and enjoy a window that will update every 5 seconds with the nodes status!

This tool is expected to get soon other updates, mostly regarding its appearance, but if you have any suggestions about additional functionalities that could be useful for your every-day work, feel free to contact me.

## 0. Set-Up
GUI support is required on the user system, so it is recommended to install opoSqueue on your local computer, not on the cluster login node. Your computer will also need Python >=3.11, so make sure to have the correct version (run `python --version`) or [download it](https://www.python.org/downloads/). 

Once you have the correct version of Python, install this package by simply cloneing the repository running this command through the Terminal:

```bash
pip install git+https://github.com/flavialeotta/opoSqueue.git
```

The installation will automatically take care of the dependencies, but it is also possible to manually install them by cloning the repository and then running the command:

```bash
pip install requirements.txt
```

## 1. How to run
To run opoSqueue simply type:

```bash
oposqueue
```

and you're good to go! It will open the following window:
<img src="src/oposqueue/storage/static/main_window.png" alt="main page" width="200"/>

### Save your connection details
To start a new connection, click on "New Connection. This button will redirect you to the following window:
<img src="src/oposqueue/storage/static/new_connection.png" alt="new connection" width="200"/>

and you can fill in the required fields:

- *'Save Slot Name'*: an optional field that lets you rename a connection to a name easy to remember, like "University" or "Work";
- *'Host'*: the SSH address;
- *'Username'*: the user name at which you're registered in the server;
- *'Password'*: the server's account Password. **Important: opoSqueue NEVER stores your passwords!**.

### Main window
Once the connection is established you will be redirected to the cluster view of your HPC nodes.

<img src="src/oposqueue/storage/static/cluster_view.png" alt="cluster" width="200"/>

This window not only shows an overview of all the nodes available in the HPC cluster and their statuses, but also a list of queued jobs (on the right). Each node also displays the number of CPUs available and allocated, as well as the name of the user currently running analyses on that node and a color-coded 'window' depending on its status:

- green: available and free;
- yellow: partially occupied;
- red: completely allocated;
- grey: down (lost connection to the node).

An interesting feature of opoSqueue is the possibility of searching for a specific Username (on the top bar) which will promptly highlight any node currentl used by that same user. This gives a quick access on the status of your analyses: once no node is highlighted, all your analyses will have finished!

### Access saved connections

If you have ticked "Save connection" when providing connection's data, the next time you will open opoSqueue, a new button will appear: continue.

<img src="src/oposqueue/storage/static/continue.png" alt="continue" width="200"/>

Once you click on that button, you will be redirected to a list of all the connections previously saved. To connect again, select "Connect" and provide your password in the pop-up window:

<img src="src/oposqueue/storage/static/continue_credentials.png" alt="credentials" width="200"/>

## 2. Components
Folder structure:
opoSqueue
│   .gitignore
│   pyproject.toml
│   README.md
│   requirements.txt
│
└───src
    └───oposqueue
        │   main.py
        │   __init__.py
        │   __main__.py
        │
        ├───core
        │       asset_path.py
        │       polling_service.py
        │       profile_manager.py
        │       slurm_parser.py
        │       ssh_manager.py
        │       state_store.py
        │       __init__.py
        │
        ├───models
        │       job.py
        │       node.py
        │       ssh_profile.py
        │       __init__.py
        │
        ├───storage
        │   ├───profiles
        │   │       .gitkeep
        │   │
        │   └───static
        │           png files for documentation
        │
        └───ui
            │   logo.png
            │   __init__.py
            │
            ├───fonts
            │       custom fonts ttf files
            │
            ├───piskels
            │       raw files for sprites
            │
            ├───sprites
            │       gif files for sprites
            │
            ├───widgets
            │       fonts.py
            │       job_queue_panel.py
            │       node_tile.py
            │       save_slot_widget.py
            │       __init__.py
            │
            └───windows
                    cluster_view.py
                    connection_dialogue.py
                    save_select_screen.py
                    title_screen.py
                    __init__.py

Components of opoSqueue:
1. **core scripts**
2. **models scripts**
3. **ui/widgets scripts**
4. **ui/windows scripts**

## 3. Possible problems
### WARNING: The script oposqueue.exe is installed in '...' which is not on PATH.
This is usually a local configuration problem, which can be easily solved. Locate the path that is provided by the warning message (usually something along the line of 'C:\Users\name of the user\intermediate folders\Python\pythoncore-version\Scripts')

Run this PowerShell command:

```PowerShell
[Environment]::SetEnvironmentVariable("Path", $env:Path + "; path given by the error message", "User")
```

Do not change "User" for your user name. Then, restart your Terminal window.

## 4. Contacts
For any type of inquiries or to drop and say hi, please contact me either at my personal e-mail address (flavia.leotta@hotmail.com) or my institutional one (fleotta@cent.uw.edu.pl).