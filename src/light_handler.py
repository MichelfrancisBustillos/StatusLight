"""
This module handles all interactions with the light,
including updating the light status based on the extracted status from the Teams log
and checking the communication with the light.
Author: Michelfrancis Bustillos
"""
# pylint: disable=line-too-long
import tkinter as tk
from tkinter import messagebox
import logging
import requests
from teams_handler import extract_status
from config_handler import load_config

manual_override = False

def update_status(root: tk.Tk, loaded_config: dict, status_label: tk.Label, light_status_label: tk.Label, status = None):
    """
    Update the status and light status labels in the GUI.
    :param root: The root Tkinter window.
    :type root: tk.Tk
    :param loaded_config: The loaded configuration containing the light URL and color mappings.
    :type loaded_config: dict
    :param status_label: The Tkinter Label widget to update with the current status.
    :type status_label: tk.Label
    :param light_status_label: The Tkinter Label widget to update with the current light status.
    :type light_status_label: tk.Label
    :param status: The current status to set the light to (optional, if not provided it will be extracted from the Teams log).
    :type status: str or None 
    :return: None
    """

    if status is not None:
        new_status = status
    else:
        new_status = extract_status(loaded_config["teams_log_path"])
    if new_status != status_label.cget("text").split(": ")[1]:
        logging.info("Status change detected: %s", new_status)
        update_light(loaded_config, new_status)
        status_label.config(text=f"Current Status: {new_status}")
        light_status_label.config(text=f"Light Status: {light_communications_check(loaded_config)}")
    if loaded_config["manual_override"] is False:
        root.after(10000, update_status, root, loaded_config, status_label, light_status_label)


def light_communications_check(loaded_config: dict) -> str:
    """
    Check if the light is reachable and update the configuration accordingly.
    :param loaded_config: The loaded configuration containing the light URL and color mappings.
    :type loaded_config: dict
    :return: str: The status of the light communication ("Connected" or "Error").
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
    :param loaded_config: The loaded configuration containing the light URL and color mappings.
    :type loaded_config: dict
    :param status: The current status to set the light to ("Available", "Busy", "Away", or "Unknown").
    :type status: str
    :return: None
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
    :param loaded_config: The loaded configuration containing the light URL and color mappings.
    :type loaded_config: dict
    :return: str: The current status of the light ("Available", "Busy", "Away", or "Unknown").
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
