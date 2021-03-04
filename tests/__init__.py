#  Drakkar-Software OctoBot-Binary
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import os
import platform
import shutil


def is_on_windows():
    return platform.system() == "Windows"


def get_binary_file_path() -> str:
    if is_on_windows():
        return "OctoBot_windows_x64.exe/OctoBot_windows.exe"
    elif platform.system() == "Darwin":
        return "./OctoBot_macos_x64/OctoBot_macos-latest_x64"
    else:
        return "./OctoBot_linux_x64/OctoBot_ubuntu-latest_x64"


def delete_folder_if_exists(folder_path):
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        shutil.rmtree(folder_path)


def clear_octobot_previous_folders():
    try:
        for folder_path in [
            "logs",
            "tentacles",
            "user"
        ]:
            delete_folder_if_exists(folder_path)
    except PermissionError:
        # Windows file conflict
        pass


def get_log_file_content(log_file_path="logs/OctoBot.log"):
    with open(log_file_path, "r") as log_file:
        return log_file.read()
