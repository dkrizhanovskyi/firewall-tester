# This file is part of the Automated Firewall Rule Tester.
# 
# Automated Firewall Rule Tester is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Automated Firewall Rule Tester is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Automated Firewall Rule Tester. If not, see <https://www.gnu.org/licenses/>.
import logging
import os

def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    """
    Set up a logger with a specific name and log file.
    :param name: Name of the logger.
    :param log_file: Path to the log file.
    :param level: Logging level.
    :return: Configured logger instance.
    """
    # Ensure the directory for the log file exists
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
