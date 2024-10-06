import asyncio
from meross_iot.manager import MerossManager
from meross_iot.http_api import MerossHttpClient
from meross_iot.model.enums import OnlineStatus
import logging

# Aktivieren der ausführlichen Protokollierung (optional)
logging.basicConfig(level=logging.INFO)

EMAIL = 'Ihre_Email@example.com'
PASSWORD = 'Ihr_Meross_Passwort'

async def main():
    # API-Basis-URL direkt angeben (anpassen, falls nötig)
    api_base_url = 'https://iot.meross.com'  # Oder 'https://iot-eu.meross.com' für Europa

    # Erstellen eines HTTP-Clients mit Ihren Zugangsdaten und der API-URL
    http_client = await MerossHttpClient.async_from_user_password(
        email=EMAIL,
        password=PASSWORD,
        api_base_url=api_base_url
    )

    # Initialisieren des Managers mit dem HTTP-Client
    manager = MerossManager(http_client=http_client)
    await manager.async_init()

    # Geräte entdecken
    await manager.async_device_discovery()
    devices = manager.find_devices()

    if not devices:
        print("Keine Geräte gefunden.")
        manager.close()
        await http_client.async_logout()
        return

    try:
        while True:
            # Iterieren über alle gefundenen Geräte
            for device in devices:
                # Versuchen, das Gerätemodell abzurufen
                try:
                    model = device.type
                except AttributeError:
                    model = "Unbekannt"

                if model == 'mss315':
                    # print(f"\nGerät: '{device.name}', Modell: {model}")

                    # Überprüfen, ob das Gerät online ist
                    if device.online_status == OnlineStatus.ONLINE:
                        # Aktualisieren des Gerätezustands
                        await device.async_update()
                        # Überprüfen, ob das Gerät den Stromverbrauch messen kann
                        if hasattr(device, 'async_get_instant_metrics'):
                            try:
                                electricity = await device.async_get_instant_metrics()
                                power = int(electricity.power / 1000)  # Umwandlung von mW in W
                                voltage = int(electricity.voltage / 1000)  # Umwandlung von mV in V
                                current = int(electricity.current / 1000)  # Umwandlung von mA in A
                                print(f"Aktueller Stromverbrauch von '{device.name}':")
                                print(f"  Leistung: {power} W")
                                print(f"  Spannung: {voltage} V")
                                print(f"  Stromstärke: {current} A")
                            except Exception as e:
                                print(f"Fehler beim Abrufen des Stromverbrauchs von '{device.name}': {e}")
                        #else:
                            # print(f"Das Gerät '{device.name}' unterstützt keine Messung des Stromverbrauchs.")
                    else:
                        print(f"Das Gerät '{device.name}' ist offline.")

            # Warten Sie 10 Sekunden, bevor Sie erneut abfragen
            await asyncio.sleep(60)
    except KeyboardInterrupt:
        print("\nProgramm beendet durch Benutzer.")

    # Aufräumen
    manager.close()
    await http_client.async_logout()

if __name__ == '__main__':
    asyncio.run(main())
