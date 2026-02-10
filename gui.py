"""
GUI for displaying current status and light status, and allowing users to change settings.
Author: Michelfrancis Bustillos
"""
# pylint: disable=line-too-long
import tkinter as tk
from tkinter import ttk, colorchooser
import pystray
from PIL import Image
from config_handler import save_config, generate_default_config
from light_handler import update_status

class GUI():
    """
    GUI class for displaying current status and light status, and allowing users to change settings.
    :param self
    :param root: The root Tkinter window.
    :type root: tk.Tk
    :param loaded_config: The loaded configuration containing the light URL and color mappings.
    :type loaded_config: dict
    :return: None
    """
    def __init__(self, root: tk.Tk, loaded_config: dict):
        self.root = root
        self.root.title("Teams Status Light")
        self.tray_minimize = tk.BooleanVar()
        self.tray_minimize.set(loaded_config.get("tray_minimize", False))
        self.check_tray_minimize()
        self.root.title("Teams Status Light")
        self.image = Image.open("icon.png")
        self.menu = (pystray.MenuItem("Open", self.show_window), pystray.MenuItem("Exit", self.close_window))
        self.tab_control = ttk.Notebook(self.root)
        self.generate_status_tab()
        update_status(self.root, loaded_config, self.status_label, self.light_status_label)
        self.generate_settings_tab(loaded_config["light_url"])
        self.tab_control.pack(expand=1, fill="both")

    def color_picker(self, status: str):
        """
        Show a color picker dialog and save the selected color for the specified status in the configuration.
        
        :param self
        :param status: The status for which the color is being picked ("busy", "away", or "available").
        :type status: str
        :return: None
        """
        color = colorchooser.askcolor(title="Choose Color")
        save_config(None,status, color[0])

    def generate_status_tab(self):
        """
        Generate the status tab for the GUI, displaying the current status and light status.
        
        :param self
        :return: None
        """
        status_tab = tk.Frame(self.tab_control)
        self.status_label = tk.Label(status_tab, text="Current Status: Unknown", font=("Arial", 16))
        self.status_label.pack(pady=20)
        self.light_status_label = tk.Label(status_tab, text="Light Status: Unknown", font=("Arial", 16))
        self.light_status_label.pack(pady=20)
        self.tab_control.add(status_tab, text="Status")

    def generate_settings_tab(self, light_url: str):
        """
        Generate the settings tab for the GUI, allowing users to change the light IP address and color mappings.
        
        :param self
        :param light_url: URL of the light to display in the settings tab.
        :type light_url: str
        :return: None
        """
        settings_tab = tk.Frame(self.tab_control)
        light_ip_input_label = tk.Label(settings_tab, text="Light IP Address:", font=("Arial", 12))
        light_ip_input_label.grid(row=0, column=0, padx=10, pady=10)
        light_ip_input = tk.Entry(settings_tab, width=20)
        light_ip_input.grid(row=0, column=1, padx=10, pady=10)
        light_ip_input.insert(0, light_url.split("/")[2].split(":")[0])
        submit_button = tk.Button(settings_tab, text="Save", command=lambda: save_config(light_ip_input.get()))
        submit_button.grid(row=0, column=2, columnspan=2, pady=10)
        busy_color_button = tk.Button(settings_tab, text="Choose Busy Color", command=lambda: self.color_picker("busy"))
        busy_color_button.grid(row=1, column=0, columnspan=1, pady=10, padx=10, sticky="e")
        away_color_button = tk.Button(settings_tab, text="Choose Away Color", command=lambda: self.color_picker("away"))
        away_color_button.grid(row=1, column=1, columnspan=1, pady=10, padx=10)
        available_color_button = tk.Button(settings_tab, text="Choose Available Color", command=lambda: self.color_picker("available"))
        available_color_button.grid(row=1, column=2, columnspan=1, pady=10, padx=10, sticky="w")
        reset_button = tk.Button(settings_tab, text="Reset to Default", command=lambda: generate_default_config())
        reset_button.grid(row=2, column=0, pady=10)
        minimize_button = tk.Checkbutton(settings_tab, text="Minimize to Tray", variable=self.tray_minimize, onvalue=True, offvalue=False, command=lambda: self.check_tray_minimize())
        minimize_button.grid(row=2, column=1, pady=10)
        self.tab_control.add(settings_tab, text="Settings")

    def widthdraw_window(self):
        """
        Callback for withdrawing the window to the system tray.
        
        :param self
        :return: None
        """
        self.root.withdraw()
        self.icon = pystray.Icon("name", self.image, "Teams Status Light", self.menu)
        self.icon.run()

    def show_window(self):
        """
        Callback for showing the window from the system tray menu.
        
        :param self
        :return: None
        """
        self.icon.stop()
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.widthdraw_window())
        self.root.after(0, self.root.deiconify)

    def close_window(self):
        """
        Callback for closing the application from the system tray menu.
        
        :param self
        :return: None
        """
        self.icon.stop()
        self.root.destroy()

    def check_tray_minimize(self):
        """
        Check the tray minimize setting and set the window close protocol accordingly.
        
        :param self
        :return: None
        """
        if self.tray_minimize.get():
            self.root.protocol("WM_DELETE_WINDOW", lambda: self.widthdraw_window())
        else:
            self.root.protocol("WM_DELETE_WINDOW", lambda: self.close_window())
        save_config(None, None, None, self.tray_minimize.get())
