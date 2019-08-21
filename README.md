# WOW CLASSIC LAUNCHER
Launches WoW Classic for you, and keeps it running.


### Requirements
- Windows
- Battlenet
  - Default install dir `C:\Program Files (x86)\Battle.net\Battle.net Launcher.exe`
    - Else, put a symlink in that dir to where you have it installed.
  - Logged in
  - Default page set to World of Warfcraft w/ Classic selected
  - Window on main-monitor
- Mouse cursor on main-monitor
- Wow on main-monitor
- Python 3.7?
  - Modules: pyautogui, opencv-python (w/ numpy -v 1.14.5), psutil

### Limitations
- There seems to be a hard time-out on the character screen, you get disconnected every 30 minutes idle or not. While this script will relaunch wow for you within 1~ minute, hitting another queue isn't ideal.

### Recommended Use
Make a windows **scheduled task** to run this script <30 minutes before server launch, or for following days, your expected return time. As for which run-method, python or exe, both work consistently well but the exe is probably the way to go.

### Running as Python
```bash
# Python Module Requirments
python -m pip install pyautogui
python -m pip install opencv-python
python -m pip install numpy==1.14.5
python -m pip install psutil

# Run Script
python \path\wow-launcher-script.py
```

### Running Build
Goto [releases](), download the latest, click `wow-auto-launcher.exe` inside folder.

### Building Process
```bash
# Without make
python -m nuitka --standalone --mingw64--plugin-enable=numpy --experimental=use_pefile --experimental=use_pefile_recurse --experimental=use_pefile_fullrecurse wow-launcher-script.py

# With make
make build
```

## KNOWN ISSUES
- Goes from LOADING_REALM(logging into realm) to CHARACTER_SCREEN on first launch, then restarts wow.


## TODO
- Fix char screen bug before click realm list on first run
- Load patterns into bytes on init; store patterns as b64 in module
