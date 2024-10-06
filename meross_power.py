import asyncio
from meross_iot.manager import MerossManager
from meross_iot.http_api import MerossHttpClient
from meross_iot.model.enums import OnlineStatus
import logging

# Enable verbose logging (optional)
logging.basicConfig(level=logging.INFO)

EMAIL = 'your_email@example.com'
PASSWORD = 'your_meross_password'

async def main():
    # Specify the API base URL directly (adjust if necessary)
    api_base_url = 'https://iot.meross.com'  # Or 'https://iot-eu.meross.com' for Europe

    # Create an HTTP client with your credentials and API URL
    http_client = await MerossHttpClient.async_from_user_password(
        email=EMAIL,
        password=PASSWORD,
        api_base_url=api_base_url
    )

    # Initialize the manager with the HTTP client
    manager = MerossManager(http_client=http_client)
    await manager.async_init()

    # Discover devices
    await manager.async_device_discovery()
    devices = manager.find_devices()

    if not devices:
        print("No devices found.")
        manager.close()
        await http_client.async_logout()
        return

    try:
        while True:
            # Iterate over all found devices
            for device in devices:
                # Attempt to retrieve the device model
                try:
                    model = device.type
                except AttributeError:
                    model = "Unknown"

                # Check if the model is 'mss315'
                if model != 'mss315':
                    continue  # Skip this device if it's not the desired model

                print(f"\nDevice: '{device.name}', Model: {model}")

                # Check if the device is online
                if device.online_status == OnlineStatus.ONLINE:
                    # Update the device state
                    await device.async_update()
                    # Check if the device supports power consumption measurement
                    if hasattr(device, 'async_get_instant_metrics'):
                        try:
                            electricity = await device.async_get_instant_metrics()
                            # Convert and round to integers
                            power = int(electricity.power / 1000)    # Power in Watts as integer
                            voltage = int(electricity.voltage / 1000)  # Voltage in Volts as integer
                            current = int(electricity.current / 1000)  # Current in Amperes as integer
                            print(f"Current power consumption of '{device.name}':")
                            print(f"  Power: {power} W")
                            print(f"  Voltage: {voltage} V")
                            print(f"  Current: {current} A")
                        except Exception as e:
                            print(f"Error retrieving power consumption from '{device.name}': {e}")
                    else:
                        print(f"The device '{device.name}' does not support power consumption measurement.")
                else:
                    print(f"The device '{device.name}' is offline.")

            # Wait 10 seconds before querying again
            await asyncio.sleep(10)
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")

    # Cleanup
    manager.close()
    await http_client.async_logout()

if __name__ == '__main__':
    asyncio.run(main())
