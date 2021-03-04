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

import pytest
import requests
import time

from tests import get_binary_file_path, clear_octobot_previous_folders, get_log_file_content, is_on_windows

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

BINARY_DISABLE_WEB_OPTION = "-nw"
LOG_CHECKS_MAX_ATTEMPTS = 300


@pytest.fixture
def start_binary():
    clear_octobot_previous_folders()
    with TemporaryFile() as output, TemporaryFile() as err:
        binary_process = start_binary_process("", output, err)
        try:
            yield
        except Exception:
            pass
        finally:
            terminate_binary(binary_process, output, err)


@pytest.fixture
def start_binary_without_web_app():
    clear_octobot_previous_folders()
    with TemporaryFile() as output, TemporaryFile() as err:
        binary_process = start_binary_process(BINARY_DISABLE_WEB_OPTION, output, err)
        logger.debug(err.read())
        try:
            yield
        except Exception:
            pass
        finally:
            terminate_binary(binary_process, output, err)


def start_binary_process(binary_options, output_file, err_file):
    logger.debug("Starting binary process...")
    return subprocess.Popen(f"{get_binary_file_path()} {binary_options}",
                            shell=True,
                            stdout=output_file,
                            stderr=err_file,
                            preexec_fn=os.setsid if not is_on_windows() else None)


def terminate_binary(binary_process, output_file, err_file):
    logger.info(output_file.read())
    errors = err_file.read()
    if errors:
        logger.error(errors)
        raise ValueError(f"Error happened during process execution : {errors}")
    logger.debug("Killing binary process...")
    if is_on_windows():
        os.kill(binary_process.pid, signal.CTRL_C_EVENT)
    else:
        try:
            os.killpg(os.getpgid(binary_process.pid), signal.SIGTERM)  # Send the signal to all the process groups
        except ProcessLookupError:
            binary_process.kill()


def multiple_checks(check_method, sleep_time=1, max_attempts=10, **kwargs):
    attempt = 1
    while max_attempts >= attempt > 0:
        try:
            result = check_method(**kwargs)
            if result:  # success
                return
        except Exception as e:
            logger.warning(f"Check ({attempt}/{max_attempts}) failed : {e}")
        finally:
            attempt += 1
            try:
                time.sleep(sleep_time)
            except KeyboardInterrupt:
                # Fails when windows is stopping binary
                pass
    assert False  # fail


def check_endpoint(endpoint_url, expected_code):
    try:
        result = requests.get(endpoint_url)
        return result.status_code == expected_code
    except requests.exceptions.ConnectionError:
        logger.warning(f"Failed to get {endpoint_url}")
        return False


def check_logs_content(expected_content: str, should_appear: bool = True):
    log_content = get_log_file_content()
    logger.debug(log_content)
    if should_appear:
        return expected_content in log_content
    return expected_content not in log_content


def test_terms_endpoint(start_binary):
    multiple_checks(check_endpoint,
                    max_attempts=100,
                    endpoint_url="http://localhost:5001/terms",
                    expected_code=200)


def test_evaluation_state_created(start_binary_without_web_app):
    multiple_checks(check_logs_content,
                    max_attempts=LOG_CHECKS_MAX_ATTEMPTS,
                    expected_content="new state:")


def test_logs_content_has_no_errors(start_binary_without_web_app):
    multiple_checks(check_logs_content,
                    max_attempts=LOG_CHECKS_MAX_ATTEMPTS,
                    expected_content="ERROR",
                    should_appear=False)


def test_balance_profitability_updated(start_binary_without_web_app):
    multiple_checks(check_logs_content,
                    max_attempts=LOG_CHECKS_MAX_ATTEMPTS,
                    expected_content="BALANCE PROFITABILITY :")
