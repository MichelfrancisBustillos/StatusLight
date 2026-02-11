# StatusLight

A Python application that automatically synchronizes your Microsoft Teams status with an RGB light device. This tool monitors your Teams activity and adjusts the light's color to reflect your current status in real-time.

## Features

- **Automatic Status Detection**: Continuously monitors your Microsoft Teams status from activity logs
- **RGB Light Control**: Updates an RGB light device based on your Teams status
- **Manual Override**: Temporarily override automatic status detection and manually set your status
- **GUI Interface**: User-friendly Tkinter interface for managing settings and status
- **Customizable Colors**: Choose custom RGB colors for each status (Available, Busy, Away, Do Not Disturb)
- **Tray Minimization**: Option to minimize the application to the system tray
- **Configuration Management**: Easy-to-use settings tab for light IP address and color configuration

## Status Colors

The application supports the following status mappings:

- **Available**: Green (0, 255, 0) - Default
- **Busy**: Red (255, 0, 0) - Default
- **Away**: Yellow (255, 255, 0) - Default
- **Do Not Disturb**: Red (255, 0, 0) - Default
- **Off**: Light turns off when status is unknown

All colors are customizable through the GUI settings.

## Requirements

- Python 3.6+
- Microsoft Teams (with log file access)
- RGB light device compatible with JSON API control (e.g., Nanoleaf, WLED, or similar)
- Required Python packages:
  - `requests`
  - `pillow`
  - `pystray`
  - `tkinter` (usually included with Python)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MichelfrancisBustillos/StatusLight.git
   cd StatusLight
   ```

2. Install required dependencies:
   ```bash
   pip install requests pillow pystray
   ```

3. Run the application:
   ```bash
   python src/main.py
   ```

   Optionally, pass the light's IP address as an argument:
   ```bash
   python src/main.py 192.168.4.220
   ```

## Configuration

### Initial Setup

When you first run the application, a `config.ini` file will be automatically created with default settings. The configuration file is located in the `src/` directory.

### Configuration Options

The `config.ini` file contains the following settings:

```ini
[Settings]
light_ip = 192.168.4.220           # IP address of your RGB light device
busy = (255, 0, 0)                 # RGB color for Busy status
away = (255, 255, 0)               # RGB color for Away status
available = (0, 255, 0)            # RGB color for Available status
teams_log_path = ...               # Path to Teams log directory (auto-detected)
tray_minimize = True               # Minimize to system tray when closing
manual_override = False            # Enable/disable manual status override
```

## Usage

### Status Tab

Displays your current Microsoft Teams status and the connection status of your RGB light device.

- **Current Status**: Shows your Teams status (Available, Busy, Away, Do Not Disturb, or Unknown)
- **Light Status**: Shows whether the light is Connected or if there's an Error

### Control Tab

Allows you to manually set your status and control the light.

- **Manual Status Override**: Enable to temporarily disable automatic status detection
- **Status Buttons**: Set Busy, Away, Available, or Off status manually
- When enabled, automatic updates stop and the light follows your manual selections

### Settings Tab

Configure your light device and customize status colors.

- **Light IP Address**: Enter the IP address of your RGB light device
- **Color Buttons**: Click to choose custom colors for each status using a color picker
- **Reset to Default**: Restore default color settings
- **Minimize to Tray**: Enable to minimize the window to the system tray instead of closing

## Light Device Requirements

Your RGB light device must:

1. Be accessible via HTTP
2. Support JSON POST requests to control its state
3. Accept commands in the following format:

   ```json
   {
     "on": true,
     "seg": [{"id": 0, "col": [[R, G, B]]}],
     "bri": 254
   }
   ```

The endpoint should be at: `http://<light_ip>/json/state`

Common compatible devices:
- Nanoleaf devices (with local API enabled)
- WLED-compatible devices
- Custom RGB light controllers with JSON API support

## Troubleshooting

### Light Connection Error
- Ensure your RGB light device is powered on and connected to your network
- Verify the light's IP address in the Settings tab
- Check that the device is accessible from your computer (try pinging the IP)

### Status Not Updating
- Ensure Microsoft Teams is running and actively logging activity
- Check that the Teams log path is correct in Settings
- Verify you have read access to the Teams log directory

### Application Not Starting
- Ensure all required Python packages are installed: `pip install requests pillow pystray`
- Check the `debug.log` file for detailed error messages

## Project Structure

```
StatusLight/
├── ReadMe.md              # This file
├── ToDo                   # Future enhancement list
├── src/
│   ├── main.py           # Application entry point
│   ├── gui.py            # GUI implementation
│   ├── light_handler.py  # Light device communication
│   ├── teams_handler.py  # Teams status extraction
│   ├── config_handler.py # Configuration management
│   ├── config.ini        # Application configuration
│   └── icons/            # Application icon assets
```

## Planned Features

- Change icon color based on status
- Turn off light on application exit

## Author

Michelfrancis Bustillos

## License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE.md](LICENSE) file for
details.

## Support

For issues or feature requests, please open an issue on the GitHub repository.
