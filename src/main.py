"""
Update Light color based on status and display current status in a GUI.
Author: Michelfrancis Bustillos
"""
import os
import sys
import tkinter as tk
import logging
from gui import GUI
from config_handler import load_config, save_config, generate_default_config

logging.basicConfig(filename="debug.log",
                    format='%(asctime)s %(levelname)s: %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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

    root = tk.Tk()
    GUI(root, loaded_config)
    root.mainloop()
