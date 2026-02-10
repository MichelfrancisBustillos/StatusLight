"""
Update Light color based on status and display current status in a GUI.
Author: Michelfrancis Bustillos
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import logging
import requests
from gui import generate_status_tab, generate_settings_tab
from config_handler import load_config, save_config, generate_default_config
from teams_handler import extract_status

logging.basicConfig(filename="debug.log",
                    format='%(asctime)s %(levelname)s: %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def light_communications_check(loaded_config: dict):
    """
    Check if the light is reachable and update the configuration accordingly.
    Parameters:
    loaded_config (dict): The loaded configuration containing the light URL and color mappings.
    Returns:
    None
    """
    url = loaded_config["light_url"]
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return "Connected"
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Light Communication Error", "Error communicating with the light. Please check the light IP address in the settings.")
        logging.error("Error communicating with light: %s", e)
        return "Error"

def update_light(loaded_config: dict, status: str):
    """
    Update Light color based on status.
    Parameters:
    loaded_config (dict): The loaded configuration containing the light URL and color mappings.
    status (str): The current status to update the light with ("Available", "Busy", "Away", or "Unknown").
    Returns:
    None
    """
    url = loaded_config["light_url"]
    available_r = int(loaded_config["available_color"].strip("()").split(",")[0])
    available_g = int(loaded_config["available_color"].strip("()").split(",")[1])
    available_b = int(loaded_config["available_color"].strip("()").split(",")[2])
    busy_r = int(loaded_config["busy_color"].strip("()").split(",")[0])
    busy_g = int(loaded_config["busy_color"].strip("()").split(",")[1])
    busy_b = int(loaded_config["busy_color"].strip("()").split(",")[2])
    away_r = int(loaded_config["away_color"].strip("()").split(",")[0])
    away_g = int(loaded_config["away_color"].strip("()").split(",")[1])
    away_b = int(loaded_config["away_color"].strip("()").split(",")[2])
    color_map = {
        "Available": {"on": True, "seg": [{"id": 0, "col": [[available_r,available_g,available_b]]}], "bri": 254},
        "Busy": {"on": True, "seg": [{"id": 0, "col": [[busy_r,busy_g,busy_b]]}], "bri": 254},
        "Do not disturb": {"on": True, "seg": [{"id": 0, "col": [[busy_r,busy_g,busy_b]]}], "bri": 254},
        "Away": {"on": True, "seg": [{"id": 0, "col": [[away_r,away_g,away_b]]}], "bri": 254},
        "Unknown": {"on": False}
    }
    payload = color_map.get(status, color_map["Unknown"])
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        logging.info("Updated light status to %s", status)
    except requests.exceptions.RequestException as e:
        logging.error("Error updating light status: %s", e)

def get_light_status(loaded_config: dict) -> str:
    """
    Get the current status of the light.
    Parameters:
    loaded_config (dict): The loaded configuration containing the light URL and color mappings.
    Returns:
    str: The current status of the light ("Available", "Busy", "Away", or "Unknown").
    """
    url = loaded_config["light_url"]
    available_r = int(loaded_config["available_color"].strip("()").split(",")[0])
    available_g = int(loaded_config["available_color"].strip("()").split(",")[1])
    available_b = int(loaded_config["available_color"].strip("()").split(",")[2])
    busy_r = int(loaded_config["busy_color"].strip("()").split(",")[0])
    busy_g = int(loaded_config["busy_color"].strip("()").split(",")[1])
    busy_b = int(loaded_config["busy_color"].strip("()").split(",")[2])
    away_r = int(loaded_config["away_color"].strip("()").split(",")[0])
    away_g = int(loaded_config["away_color"].strip("()").split(",")[1])
    away_b = int(loaded_config["away_color"].strip("()").split(",")[2])
    try:
        response = requests.get(url,timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("on"):
                col = data.get("seg", [{}])[0].get("col")[0]
                if col == [available_r,available_g,available_b]:
                    return "Available"
                elif col == [busy_r,busy_g,busy_b]:
                    return "Busy"
                elif col == [away_r,away_g,away_b]:
                    return "Away"
    except requests.exceptions.RequestException as e:
        logging.error("Error getting light status: %s", e)
    return "Unknown"

def update_status(root: tk.Tk, loaded_config: dict, status_label: tk.Label, light_status_label: tk.Label):
    """
    Update the status and light status labels in the GUI.
    Parameters:
    root (tk.Tk): The root Tkinter window.
    loaded_config (dict): The loaded configuration containing the light URL and color mappings.
    status_label (tk.Label): The label widget for displaying the current status.
    light_status_label (tk.Label): The label widget for displaying the light status.
    Returns:
    None
    """
    new_status = extract_status(loaded_config["teams_log_path"])
    if new_status != status_label.cget("text").split(": ")[1]:
        logging.info("Status change detected: %s", new_status)
        update_light(loaded_config, new_status)
        status_label.config(text=f"Current Status: {new_status}")
        light_status_label.config(text=f"Light Status: {light_communications_check(loaded_config)}")
    root.after(5000, update_status, root, loaded_config, status_label, light_status_label)


def create_gui(loaded_config: dict) -> tk.Tk:
    """
    Create the GUI for displaying the current status and light status.
    Parameters:
    loaded_config (dict): The loaded configuration containing the light URL and color mappings.
    Returns:
    tk.Tk: The root Tkinter window with the GUI.
    """
    root = tk.Tk()
    root.title("Teams Status Light")
    tabControl = ttk.Notebook(root)
    tabControl, status_label, light_status_label = generate_status_tab(tabControl)
    update_status(root, loaded_config, status_label, light_status_label)
    tabControl = generate_settings_tab(tabControl, loaded_config["light_url"])
    tabControl.pack(expand=1, fill="both")
    return root

if __name__ == "__main__":
    logging.info("Starting application.")
    if not os.path.exists("config.ini"):
        logging.info("Config file not found. Generating default config.")
        generate_default_config()

    if len(sys.argv) > 1:
        if sys.argv[1]:
            LIGHT_IP = sys.argv[1]
            save_config(LIGHT_IP, None, None)
            logging.info("Light IP address updated from command line argument: %s", LIGHT_IP)
    loaded_config = load_config()

    root = create_gui(loaded_config)
    root.mainloop()
