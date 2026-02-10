"""
Configuration handler for managing application settings, including light IP, color mappings, and Teams log path.
Author: Michelfrancis Bustillos
"""
import configparser
from teams_handler import get_teams_path

config_file = "config.ini"

def generate_default_config():
    """
    Generate a default configuration file if it does not exist.
    Parameters:
    None
    Returns:
    None
    """
    config = configparser.ConfigParser()
    config["Settings"] = {'light_ip': "0.0.0.0", 'busy': "(255, 0, 0)", 'away': "(255, 255, 0)", 'available': "(0, 255, 0)"}
    config.set("Settings", "teams_log_path", get_teams_path())
    print(config["Settings"])
    with open(config_file, "w") as configfile:
        config.write(configfile)

def load_config():
    """
    Load the configuration from the specified file.
    Parameters:
    None
    Returns:
    None
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    return {
        "light_ip": config.get("Settings", "light_ip"),
        "light_url": f"http://{config.get('Settings', 'light_ip')}/json/state",
        "busy_color": config.get("Settings", "busy"),
        "away_color": config.get("Settings", "away"),
        "available_color": config.get("Settings", "available"),
        "teams_log_path": config.get("Settings", "teams_log_path")
    }

def save_config(light_ip=None, status=None, color=None, teams_log_path=None):
    """
    Save the configuration to the specified file.
    Parameters:
    light_ip (str): The URL of the light to save in the configuration.
    status (str): The status for which the color is being saved ("busy", "away", or "available").
    color (tuple): The RGB color tuple to save for the specified status.
    teams_log_path (str): The file path of the Teams log to save in the configuration.
    Returns:
    None
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    if light_ip:
        config.set("Settings", "light_ip", light_ip)
    if status and color:
        config.set("Settings", status, str(color))
    if teams_log_path:
        teams_log_path = get_teams_path()
        config.set("Settings", "teams_log_path", teams_log_path)
    with open(config_file, "w") as configfile:
        config.write(configfile)
