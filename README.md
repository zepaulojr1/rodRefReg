
# Rodent Refreshment Regulator Version 15

**Last updated: 06/06/2024 by JS**

Welcome to the Rodent Refreshment Regulator, an automated water dispenser system designed to provide water to laboratory mice at specified intervals. This guide provides detailed instructions on setting up, configuring, and running the system using a Raspberry Pi.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Program](#running-the-program)
- [Advanced Settings](#advanced-settings)
- [Email Notifications](#email-notifications)
- [GUI Overview](#gui-overview)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Introduction
The Rodent Refreshment Regulator automates the process of providing water to laboratory mice using a relay hat connected to a Raspberry Pi. The system allows users to set specific time windows and intervals for dispensing water, ensuring the mice receive consistent hydration.

## Features
- User-friendly GUI for easy configuration
- Adjustable time windows and intervals for water dispensing
- Email notifications for successful water dispensing
- Advanced settings for fine-tuning system behavior
- Log messages displayed in a GUI-integrated terminal

## Requirements
- Raspberry Pi (tested on Raspberry Pi 4)
- Relay hat (e.g., sm_16relind relay hat)
- Python 3
- Required Python packages (see below)

## Installation
1. **Clone the Repository:**
   ```sh
   git clone https://github.com/yourusername/rodent-refreshment-regulator.git
   cd rodent-refreshment-regulator
   ```

2. **Install Required Packages:**
   ```sh
   pip install RPi.GPIO
   pip install pillow
   pip install requests
   ```

3. **Setup the Relay Hat:**
   Connect the relay hat to the Raspberry Pi GPIO pins according to the relay hat documentation.

## Configuration
Before running the program, you need to configure the water dispensing intervals and time windows.

1. **Define Relay Pairs:**
   The relay pairs are predefined as follows:
   ```python
   RELAY_PAIRS = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12), (13, 14), (15, 16)]
   ```

2. **Set Default Values:**
   Adjust the default values for interval, stagger, and time windows in the code:
   ```python
   INTERVAL = 3600  # Default interval: 1 hour
   STAGGER = 1  # Default stagger: 1 second
   WINDOW_START = 8  # Default window start time: 8 AM
   WINDOW_END = 20  # Default window end time: 8 PM
   ```

## Running the Program
1. **Launch the GUI:**
   ```sh
   python main.py
   ```

2. **Configure Settings via GUI:**
   - Answer the questions on the right side of the screen to configure water volume and intervals.
   - Click the "Suggest Settings" button to receive setting recommendations.
   - Click the "Push Settings" button to save these settings.
   - Click "Run Program" to start the water dispensing process.

3. **Stop the Program:**
   - Click "Stop Program" or close the GUI window to stop the program.

## Advanced Settings
Access advanced settings via the GUI to fine-tune system behavior:
- Enable or disable specific relay pairs
- Set the number of triggers for each relay pair
- Adjust interval and stagger times
- Define water window start and end times

## Email Notifications
The system can send email notifications upon successful water dispensing.

1. **Configure Email Settings:**
   Update the `send_email` function with your SMTP API key and recipient details:
   ```python
   api_key = "your-smtp-api-key"
   url = "https://api.your-smtp-service.com/v3/smtp/email"
   data = {
       "sender": {"name": "MouseMaster", "email": "your-email@example.com"},
       "to": [{"email": "recipient-email@example.com"}],
       "subject": subject,
       "htmlContent": content
   }
   ```

## GUI Overview
The GUI is divided into several sections:
- **Welcome Message:** Provides initial instructions and notes.
- **User Questions:** Collects input for water volume and intervals.
- **Buttons:** Allows users to suggest settings, push settings, run, and stop the program.
- **Advanced Settings:** Provides options to enable/disable relay pairs, set triggers, and update intervals and windows.
- **Terminal:** Displays log messages and system status.

## Troubleshooting
- Ensure the Raspberry Pi and relay hat are properly connected.
- Check GPIO pin configurations if relays are not triggering.
- Verify interval and time window settings are correctly configured.
- Review log messages in the GUI terminal for error details.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure your code follows the project's coding standards and includes appropriate documentation.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Enjoy using the Rodent Refreshment Regulator! If you have any questions or need further assistance, feel free to open an issue on GitHub or contact the project maintainers.
