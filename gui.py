"""
GUI for displaying current status and light status, and allowing users to change settings.
Author: Michelfrancis Bustillos
"""
import tkinter as tk
from tkinter import ttk, colorchooser
from config_handler import save_config

def color_picker(status: str):
    """
    Docstring for color_picker
    Parameters:
    status (str): The status for which the color is being picked ("busy", "away", or "available").
    Returns:
    None
    """
    color = colorchooser.askcolor(title="Choose Color")
    save_config(None,status, color[0])

def generate_status_tab(tabControl: ttk.Notebook) -> tuple:
    """
    Docstring for generate_status_tab
    Parameters:
    tabControl (ttk.Notebook): The notebook widget to which the status tab will be added.
    Returns:
    tuple: A tuple containing the updated notebook widget, the status label, and the light status label.
    """ 
    status_tab = tk.Frame(tabControl)
    status_label = tk.Label(status_tab, text="Current Status: Unknown", font=("Arial", 16))
    status_label.pack(pady=20)
    light_status_label = tk.Label(status_tab, text="Light Status: Unknown", font=("Arial", 16))
    light_status_label.pack(pady=20)
    tabControl.add(status_tab, text="Status")
    return tabControl, status_label, light_status_label

def generate_settings_tab(tabControl: ttk.Notebook, light_url: str) -> ttk.Notebook:
    """
    Docstring for generate_settings_tab
    
    :param tabControl: Description
    :type tabControl: ttk.Notebook
    :param light_url: Description
    :type light_url: str
    :return: Description
    :rtype: Notebook
    """
    settings_tab = tk.Frame(tabControl)
    light_ip_input_label = tk.Label(settings_tab, text="Light IP Address:", font=("Arial", 12))
    light_ip_input_label.pack(pady=10)
    light_ip_input = tk.Entry(settings_tab, width=20)
    light_ip_input.insert(0, light_url.split("/")[2].split(":")[0])
    light_ip_input.pack(pady=20)
    busy_color_button = tk.Button(settings_tab, text="Choose Busy Color", command=lambda: color_picker("busy"))
    busy_color_button.pack(pady=10)
    away_color_button = tk.Button(settings_tab, text="Choose Away Color", command=lambda: color_picker("away"))
    away_color_button.pack(pady=10)
    available_color_button = tk.Button(settings_tab, text="Choose Available Color", command=lambda: color_picker("available"))
    available_color_button.pack(pady=10)
    submit_button = tk.Button(settings_tab, text="Save", command=lambda: save_config(light_ip_input.get()))
    submit_button.pack(pady=10)
    tabControl.add(settings_tab, text="Settings")
    return tabControl
