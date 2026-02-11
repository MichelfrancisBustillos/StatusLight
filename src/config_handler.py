"""
Configuration handler for managing application settings,
including light IP, color mappings, and Teams log path.
Author: Michelfrancis Bustillos
"""
# pylint: disable=line-too-long
import logging
import configparser
from teams_handler import get_teams_path
from light_handler import update_light

CONFIG_FILE = "config.ini"

def generate_default_config():
    """
    Generate a default configuration file if it does not exist.
    :param None
    :return: None
    """
    config = configparser.ConfigParser()
    config["Settings"] = {'light_ip': "0.0.0.0", 'busy': "(255, 0, 0)", 'away': "(255, 255, 0)", 'available': "(0, 255, 0)"}
    config.set("Settings", "teams_log_path", get_teams_path())
    config.set("Settings", "tray_minimize", "False")
    logging.info("Default configuration generated.")
    with open(CONFIG_FILE, "w", encoding="utf-8") as configfile:
        config.write(configfile)

def load_config() -> dict:
    """
    Load the configuration from the specified file.
    :param None
    :return: dict: A dictionary containing the loaded configuration values, including light URL, color mappings, and Teams log path.
    """
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    logging.info("Configuration loaded from file: %s", CONFIG_FILE)
    return {
        "light_ip": config.get("Settings", "light_ip"),
        "light_url": f"http://{config.get('Settings', 'light_ip')}/json/state",
        "busy_color": config.get("Settings", "busy"),
        "away_color": config.get("Settings", "away"),
        "available_color": config.get("Settings", "available"),
        "teams_log_path": config.get("Settings", "teams_log_path"),
        "tray_minimize": config.getboolean("Settings", "tray_minimize", fallback=False)
    }

def save_config(light_ip=None, status=None, color=None, tray_minimize=None):
    """
    Save the configuration to the specified file.
    :param light_ip: The IP address of the light to save in the configuration (optional).
    :type light_ip: str or None
    :param status: The status for which the color is being saved ("busy", "away", or "available") (optional).
    :type status: str or None
    :param color: The color to save for the specified status in the configuration (optional).
    :type color: tuple or None
    :param tray_minimize: The boolean value indicating whether to minimize to tray (optional).
    :type tray_minimize: bool or None
    :return: None
    """
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if light_ip:
        config.set("Settings", "light_ip", light_ip)
        print(f"Light IP updated to: {light_ip}")
        update_light(load_config(), "Available")
    if status and color:
        config.set("Settings", status, str(color))
    if tray_minimize is not None:
        config.set("Settings", "tray_minimize", str(tray_minimize))
    with open(CONFIG_FILE, "w", encoding="utf-8") as configfile:
        config.write(configfile)
    logging.info("Configuration saved to file: %s", CONFIG_FILE)
