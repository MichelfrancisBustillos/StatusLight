"""
GUI for displaying current status and light status, and allowing users to change settings.
Author: Michelfrancis Bustillos
"""
import tkinter as tk
from tkinter import ttk, colorchooser
import pystray
from PIL import Image
from config_handler import save_config, generate_default_config
from light_handler import update_status

class GUI():
    def __init__(self, root: tk.Tk, loaded_config: dict):
        self.root = root
        self.root.title("Teams Status Light")
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.widthdraw_window())
        self.root.title("Teams Status Light")
        self.image = Image.open("icon.png")
        self.menu = (pystray.MenuItem("Open", self.show_window), pystray.MenuItem("Exit", self.close_window))
        self.tabControl = ttk.Notebook(self.root)
        self.generate_status_tab()
        update_status(self.root, loaded_config, self.status_label, self.light_status_label)
        self.generate_settings_tab(loaded_config["light_url"])
        self.tabControl.pack(expand=1, fill="both")

    def color_picker(self, status: str):
        color = colorchooser.askcolor(title="Choose Color")
        save_config(None,status, color[0])

    def generate_status_tab(self):
        status_tab = tk.Frame(self.tabControl)
        self.status_label = tk.Label(status_tab, text="Current Status: Unknown", font=("Arial", 16))
        self.status_label.pack(pady=20)
        self.light_status_label = tk.Label(status_tab, text="Light Status: Unknown", font=("Arial", 16))
        self.light_status_label.pack(pady=20)
        self.tabControl.add(status_tab, text="Status")

    def generate_settings_tab(self, light_url: str):

        settings_tab = tk.Frame(self.tabControl)
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
        self.tabControl.add(settings_tab, text="Settings")

    def widthdraw_window(self):
        self.root.withdraw()
        self.icon = pystray.Icon("name", self.image, "Teams Status Light", self.menu)
        self.icon.run()

    def show_window(self):
        self.icon.stop()
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.widthdraw_window())
        self.root.after(0, self.root.deiconify)

    def close_window(self):
        self.icon.stop()
        self.root.destroy()
