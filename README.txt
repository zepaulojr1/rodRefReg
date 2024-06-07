# Repository for the Rodent Refreshement Regulator Automated Watering System in development by Jamie Sanson and Jackson Cone
# Rodent Refreshment Regulator

Rodent Refreshment Regulator is a Python application designed to manage and monitor an automatic water dispenser system for feeding mice. The system is controlled by a Raspberry Pi and operates within a user-selected time window. It uses a relay hat to control a 12V water pump and a Slack bot to send notifications if the pump stops working.

## Features

- **Automatic Water Dispensing:** The system dispenses water at regular intervals during a specified time window.
- **User-Friendly GUI:** The GUI allows users to configure settings, monitor system status, and receive recommendations.
- **Slack Notifications:** Sends alerts to a Slack channel if the water pump stops working.
- **Email Notifications:** Sends email notifications upon successful pump triggers.
- **Terminal Output:** Displays system messages and settings updates in a GUI-integrated terminal.

## Requirements

- **Hardware:**
  - Raspberry Pi (with Python installed)
  - 12V Water Pump
  - Relay Hat (for controlling the pump)
  - Necessary wiring and connectors

- **Software:**
  - Python 3
  - Required Python packages:
    - RPi.GPIO
    - tkinter
    - Pillow (PIL)
    - requests
    - slack_sdk (if using Slack notifications)
    - smtplib
    - json
    - math

## Setup Instructions

### 1. Hardware Setup

- Connect the 12V water pump to the Raspberry Pi via a relay module.
- Use GPIO pins to control the relay and monitor the pump's status.

### 2. Install Required Packages

```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
pip3 install RPi.GPIO tkinter Pillow requests slack_sdk smtplib json math
