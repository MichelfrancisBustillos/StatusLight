"""
This module handles all interactions with the Teams log files,
including extracting the current status from the latest log file
and determining the file path of the latest log file.
Author: Michelfrancis Bustillos
"""
# pylint: disable=line-too-long
import glob
import mmap
from datetime import datetime
import os
import logging
import config_handler

def get_teams_path() -> str:
    """
    Return file path of latest Teams Log file.
    :param None
    :return: str: The file path of the latest Teams log file.
    """
    teams_path = str(os.getenv('LOCALAPPDATA')) + "\\Packages\\MSTeams_*\\LocalCache\\Microsoft\\MSTeams\\Logs"
    teams_path = glob.glob(teams_path)[-1]
    logging.info("Teams log file path: %s", teams_path)
    return teams_path

def extract_status() -> str:
    """
    Extract the status from the log file.
    :param None
    :return: str: The extracted status ("Available", "Busy", "Away", or "Unknown").
    """
    teams_log_path = config_handler.LOADED_CONFIG["teams_log_path"]
    teams_log_path = teams_log_path + "\\MSTeams_" + datetime.now().strftime("%Y-%m-%d") + "*.log"
    logfile = glob.glob(teams_log_path)[-1]

    new_status = "Unknown"
    statuses = ["Available", "Away", "Busy", "Do not disturb"]
    if os.path.getsize(logfile) != 0:
        with open(logfile, "r", encoding="utf-8") as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as file:
                line_number = file.rfind('status'.encode("utf-8"))
                if line_number != -1:
                    file.seek(line_number)
                    line = file.readline().decode("utf-8")
                    if any(status in line for status in statuses):
                        temp_status = line.split("status ")[1].strip()
                        if temp_status != new_status:
                            new_status = temp_status
    return new_status
