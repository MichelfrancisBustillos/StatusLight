from datetime import datetime
import glob
import os
import time
import mmap
import requests
import sys

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
    teams_path = teams_path + "\\MSTeams_" + datetime.now().strftime("%Y-%m-%d") + "*.log"
    teams_path = glob.glob(teams_path)[-1]
    return teams_path

def extract_status(logfile) -> str:
    """
    Extract the status from the log file.
    Parameters:
    logfile (str): The file path of the log file.
    Returns:
    str: The extracted status from the log file.
    """

    new_status = "Unknown"
    with open(logfile, "r", encoding="utf-8") as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as file:
            line_number = file.rfind('status'.encode("utf-8"))
            if line_number != -1:
                file.seek(line_number)
                line = file.readline().decode("utf-8")
                temp_status = line.split("status ")[1].strip()
                if temp_status in ["Available", "Away", "Busy", "Do not disturb"]:
                    new_status = temp_status
    return new_status

def update_light(url: str, status: str):
    """
    Update Light color based on status.
    Parameters:
    url (str): The URL of the light to be updated.
    status (str): The status to determine the light color.
    Returns:
    None
    """
    color_map = {
        "Available": {"on": True, "seg": [{"id": 0, "col": [[0,255,0]]}], "bri": 254},
        "Busy": {"on": True, "seg": [{"id": 0, "col": [[255,0,0]]}], "bri": 254},
        "Do not disturb": {"on": True, "seg": [{"id": 0, "col": [[255,0,0]]}], "bri": 254},
        "Away": {"on": True, "seg": [{"id": 0, "col": [[255,255,0]]}], "bri": 254},
        "Unknown": {"on": False}
    }
    payload = color_map.get(status, color_map["Unknown"])
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error updating light: {e}")

def get_light_status(url) -> str:
    """
    Get the current status of the light.
    Parameters:
    url (str): The URL of the light to get the status from.
    Returns:
    str: The current status of the light ("Available", "Busy", or "Unknown").
    """
    response = requests.get(url,timeout=5)
    if response.status_code == 200:
        data = response.json()
        if data.get("on"):
            col = data.get("seg", [{}])[0].get("col")[0]
            if col == [0, 255, 0]:
                return "Available"
            elif col == [255, 0, 0]:
                return "Busy"
            elif col == [255, 255, 0]:
                return "Away"
    return "Unknown"

if __name__ == "__main__":
    LIGHT_IP = "192.168.4.220"
    light_url = f"http://{LIGHT_IP}/json/state"
    logfile = get_teams_path()
    print(f"Reading log file: {logfile}")
    print(f"Current light status: {get_light_status(light_url)}")
    while True:
        status = extract_status(logfile)
        print(f"Current status: {status}")
        update_light(light_url, status)
        time.sleep(5)
