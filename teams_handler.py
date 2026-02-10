import glob
import mmap
from datetime import datetime
import os
import logging

def get_teams_path() -> str:
    """
    Return file path of latest Teams Log file.
    Parameters:
    None
    Returns:
    str: The file path of the latest Teams log file.
    """
    teams_path = str(os.getenv('LOCALAPPDATA')) + "\\Packages\\MSTeams_*\\LocalCache\\Microsoft\\MSTeams\\Logs"
    teams_path = glob.glob(teams_path)[-1]
    logging.info("Teams log file path: %s", teams_path)
    return teams_path

def extract_status(teams_log_path: str) -> str:
    """
    Extract the status from the log file.
    Parameters:
    logfile (str): The file path of the log file.
    Returns:
    str: The extracted status from the log file.
    """

    teams_log_path = teams_log_path + "\\MSTeams_" + datetime.now().strftime("%Y-%m-%d") + "*.log"
    logfile = glob.glob(teams_log_path)[-1]

    new_status = "Unknown"
    with open(logfile, "r", encoding="utf-8") as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as file:
            line_number = file.rfind('status'.encode("utf-8"))
            if line_number != -1:
                file.seek(line_number)
                line = file.readline().decode("utf-8")
                temp_status = line.split("status ")[1].strip()
                if temp_status in ["Available", "Away", "Busy", "Do not disturb"] and temp_status != new_status:
                    new_status = temp_status
    return new_status
