# Meross Power Consumption Reading Script

This Python script allows you to read the current power consumption of Meross devices of the model mss315. It outputs the values for power (Watts), voltage (Volts), and current (Amperes) as integers and updates the information every 10 seconds.

## Prerequisites

*	Python 3.6 or higher: Ensure that Python 3 is installed on your system.
*	meross_iot library: A Python library for communication with Meross devices.

## Installation

### Install Python

If Python is not installed, download it from the official website:

*	Python [Download](https://www.python.org/downloads/)

Verify the installation with:
```
python3 --version
```


### Install meross_iot Library

Install the required library via pip:
```
pip3 install meross_iot --upgrade
```


# Configuration

Download the Script

## Insert Credentials

Replace the placeholders in the script with your actual Meross credentials:
```
EMAIL = 'your_email@example.com'
PASSWORD = 'your_meross_password'
```
## Adjust API URL (if necessary)

If you are located in Europe, change the api_base_url to:
```
api_base_url = 'https://iot-eu.meross.com'
```


## Usage

Run the script in the terminal:
```
python3 meross_power_mss315.py
```


The program will now output the current values of your Meross device of model mss315 every 10 seconds.

### Example Output:
```
INFO:root:Initializing Meross Manager...
INFO:root:Discovering Meross devices...

Device: 'Solar 1600', Model: mss315
Current power consumption of 'Solar 1600':
  Power: 46 W
  Voltage: 230 V
  Current: 0 A

To stop the program, press Ctrl+C.
```
## Customization

Change Query Interval

To change the interval between queries, adjust the time in seconds in the asyncio.sleep() function:

# Wait 60 seconds before querying again
```
await asyncio.sleep(60)
```


## Output as Floating-Point Numbers

If you need the values with decimal places, remove the int() conversion:
```
  power = electricity.power / 1000    # Power in Watts as float
  voltage = electricity.voltage / 1000  # Voltage in Volts as float
  current = electricity.current / 1000  # Current in Amperes as float
```
## Consider Multiple Models

If you want to include other models, adjust the condition:
```
  if model not in ['mss315', 'mss310']:
    continue  # Skip devices not in the list
```


## Notes

*	Supported Devices: This script is designed for the model mss315. Ensure that your device is this model and supports power consumption measurement.
*	Network Connection: Your computer and Meross devices must be connected to the internet.
*	Error Messages: If problems occur, check your credentials, internet connection, and whether the meross_iot library is correctly installed.
*	Responsible Use: Since the Meross API is not officially documented, you should minimize the number of requests to avoid possible rate limits and not overload the service.

## Disclaimer

Use of this script is at your own risk. Ensure that you comply with Meross’s terms of use. The author assumes no liability for any damages or violations of Meross’s terms of use.

## License

This project is licensed under the MIT License.
