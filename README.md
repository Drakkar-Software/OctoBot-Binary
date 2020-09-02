# OctoBot-Binary [0.4.0-alpha23](https://github.com/Drakkar-Software/OctoBot/tree/dev/docs/CHANGELOG.md)
[![Release](https://img.shields.io/github/downloads/Drakkar-Software/OctoBot-Binary/total.svg)](https://github.com/Drakkar-Software/OctoBot-Binary/releases)
[![Build Status](https://travis-ci.com/Drakkar-Software/OctoBot-Binary.svg?branch=master)](https://travis-ci.com/Drakkar-Software/OctoBot-Binary) 
[![Build Status](https://dev.azure.com/drakkarsoftware/OctoBot-Binary/_apis/build/status/Drakkar-Software.OctoBot-Binary?branchName=0.4.0)](https://dev.azure.com/drakkarsoftware/OctoBot-Binary/_build/latest?definitionId=13&branchName=0.4.0)

OctoBot binaries is dedicated to create and upload binaries for Windows, Linux and MacOS each [OctoBot project](https://github.com/Drakkar-Software/OctoBot) release.

## Usage
Download and move your platform binary into a folder with the an [OctoBot-Launcher](https://github.com/Drakkar-Software/OctoBot-Launcher) binary and start the launcher

### On Windows
- Just double-click on *OctoBot_windows.exe*

### On Linux and MacOS
- Open a terminal a type the following commands :
```
$ chmod +x OctoBot_linux
$ ./OctoBot_linux
```

**Replace `OctoBot_linux` by `OctoBot_osx` on MacOS**

## Binary production steps:
1. Clone OctoBot (0.4.0 branch) into octobot folder
2. Install OctoBot requirements  `python -m pip install -r octobot/requirements.txt`
3. Install pyinstaller 4.0 pip install  `https://github.com/pyinstaller/pyinstaller/archive/develop.zip`
4. List OctoBot modules files for pyinstaller discovery  `python scripts/python_file_lister.py "bin/octobot_packages_files.txt" <octobot repo folder>`
5. Add pyinstaller required imports  `python scripts/insert_imports.py octobot/octobot/cli.py`
6. Copy bin folder into the octobot folder
7. Go into the octobot folder
8. Compile the OctoBot project `python setup.py build_ext --inplace`
9. Call pyinstaller  `pyinstaller bin\start.spec`
10. Binary should be available in the dist folder

More informations on [OctoBot wiki page](https://github.com/Drakkar-Software/OctoBot/wiki/Installation).
