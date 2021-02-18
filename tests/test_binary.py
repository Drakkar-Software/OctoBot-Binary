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
import logging
import os
import signal
import subprocess
from tempfile import TemporaryFile

import platform
import requests
import time

import pytest

from tests import get_binary_file_path, clear_octobot_previous_folders, get_log_file_content, is_on_windows

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@pytest.fixture
def start_binary():
    clear_octobot_previous_folders()
    with TemporaryFile() as output, TemporaryFile() as err:
        binary_process = subprocess.Popen(get_binary_file_path(),
                                          shell=True,
                                          stdout=output,
                                          stderr=err,
                                          preexec_fn=os.setsid if not is_on_windows() else None)
        logger.debug("Starting binary process...")
        yield
        logger.info(output.read())
        errors = err.read()
        if errors:
            logger.error(errors)
            raise ValueError(f"Error happened during process execution : {errors}")
        logger.debug("Killing binary process...")
        if is_on_windows():
            binary_process.kill()
        else:
            try:
                os.killpg(os.getpgid(binary_process.pid), signal.SIGTERM)  # Send the signal to all the process groups
            except ProcessLookupError:
                binary_process.kill()


def test_version_endpoint(start_binary):
    max_attempts = 10
    attempt = 1
    while max_attempts >= attempt > 0:
        try:
            requests.get('http://localhost:5001/version')
            attempt = -1  # success
        except requests.exceptions.ConnectionError:
            logger.warning(f"Failed to get http://localhost/version, retrying ({attempt}/{max_attempts})...")
            attempt += 1
            time.sleep(1)
    assert attempt <= max_attempts


def test_evaluation_state_created(start_binary):
    time.sleep(10)
    log_content = get_log_file_content()
    logger.debug(log_content)
    assert "new state:" in log_content


def test_logs_content_has_no_errors(start_binary):
    time.sleep(10)
    log_content = get_log_file_content()
    logger.debug(log_content)
    assert "ERROR" not in log_content
