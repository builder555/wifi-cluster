# import wifi
import subprocess
import dbus.mainloop.glib
import NetworkManager
import uuid
import logging

MASTER_SSID = "EtcherProAP"
MASTER_PSK = "super-secure-pass"


def add_internal_ap_connection(ssid: str, psk: str) -> None:
    logging.debug("adding EP_AP_1 master...")
    example_connection = {
        "connection": {
            "id": "EP_AP_1",
            "type": "802-11-wireless",
            "uuid": str(uuid.uuid4()),
            "interface-name": "wlan1",
        },
        "802-11-wireless": {
            "band": "bg",
            "mode": "ap",
            "security": "802-11-wireless-security",
            "ssid": ssid,
        },
        "802-11-wireless-security": {
            "key-mgmt": "wpa-psk",
            "psk": psk,
        },
        "ipv4": {"method": "shared"},
        "ipv6": {"method": "auto"},
    }
    NetworkManager.Settings.AddConnection(example_connection)
    logging.debug("added EP_AP_1 master")


def add_internal_client_connection(ssid: str, psk: str) -> None:
    logging.debug("adding EP_WIFI_1 client...")
    example_connection = {
        "connection": {
            "id": f"EP_WIFI_1",
            "type": "802-11-wireless",
        },
        "802-11-wireless": {
            "hidden": True,
            "mode": "infrastructure",
            "ssid": ssid,
        },
        "802-11-wireless-security": {
            "auth-alg": "open",
            "key-mgmt": "wpa-psk",
            "psk": psk,
        },
        "ipv4": {"method": "auto"},
        "ipv6": {"method": "auto"},
    }
    NetworkManager.Settings.AddConnection(example_connection)
    logging.debug("added EP_WIFI_1 client")


def get_internal_client_connection(ssid: str) -> NetworkManager.Connection:
    logging.debug("getting EP_WIFI_1 connection")
    connections = NetworkManager.Settings.ListConnections()
    for c in connections:
        settings = c.GetSettings()
        wifi_settings = settings.get("wifi") or settings.get("802-11-wireless", {})
        if (
            wifi_settings.get("mode") == "infrastructure"
            and wifi_settings.get("ssid", "") == ssid
        ):
            logging.debug("found EP_WIFI_1")
            return c
    logging.debug("did not find EP_WIFI_1")
    return None


def get_internal_ap_connection(ssid: str) -> NetworkManager.Connection:
    logging.debug("getting EP_AP_1")
    connections = NetworkManager.Settings.ListConnections()
    for c in connections:
        settings = c.GetSettings()
        wifi_settings = settings.get("wifi") or settings.get("802-11-wireless", {})
        if wifi_settings.get("mode") == "ap" and wifi_settings.get("ssid", "") == ssid:
            logging.debug("found EP_AP_1")
            return c
    logging.debug("did not find EP_AP_1")
    return None


def get_external_client_connection() -> NetworkManager.Connection:
    logging.debug("getting balena-wifi")
    connections = NetworkManager.Settings.ListConnections()
    for conn in connections:
        settings = conn.GetSettings()
        if settings.get("connection", {}).get("id") == "balena-wifi-01":
            logging.debug("found balena-wifi")
            return conn
    logging.debug("did not find balena-wifi")
    return None


def get_wifi_device(interface: str) -> NetworkManager.Wireless:
    logging.debug(f"getting wifi device {interface}")
    devices = NetworkManager.NetworkManager.GetDevices()
    for dev in devices:
        if dev.Interface == interface:
            logging.debug(f"got wifi device {interface}")
            return dev
    logging.debug(f"did not find {interface} device")
    return None


def connect_to_client_wifi() -> None:
    logging.debug("connecting to client wifi")
    connection = get_external_client_connection()
    assert connection, "WiFi connection credentials are not specified"
    device = get_wifi_device("wlan0")
    NetworkManager.NetworkManager.ActivateConnection(connection, device, "/")
    logging.debug("should be connected to client wifi")


def connect_to_master_wifi() -> None:
    logging.debug("connecting to master wifi")
    connection = get_internal_client_connection(MASTER_SSID)
    if not connection:
        add_internal_client_connection(MASTER_SSID, MASTER_PSK)
        connection = get_internal_client_connection(MASTER_SSID)
    device = get_wifi_device("wlan0")
    NetworkManager.NetworkManager.ActivateConnection(connection, device, "/")
    logging.debug("should be connected to master wifi")


def is_master_present() -> bool:
    logging.debug("is master present?")
    error_code = subprocess.run(
        f"iw dev wlan0 scan | grep {MASTER_SSID}", shell=True
    ).returncode
    is_master_present = error_code == 0
    if is_master_present:
        logging.debug("master IS present")
    else:
        logging.debug("master is not present")
    return is_master_present


def become_master() -> None:
    logging.debug("becoming master")
    subprocess.run("iw dev wlan1 del >/dev/null 2>&1", shell=True)
    subprocess.run("ip link set wlan0 down >/dev/null 2>&1", shell=True)
    device = get_wifi_device("wlan1")
    if not device:
        logging.debug("adding wlan1 interface")
        subprocess.run("iw dev wlan0 interface add wlan1 type __ap", shell=True)
        device = get_wifi_device("wlan1")
    connection = get_internal_ap_connection(MASTER_SSID)
    if not connection:
        add_internal_ap_connection(MASTER_SSID, MASTER_PSK)
        connection = get_internal_ap_connection(MASTER_SSID)
    subprocess.run("ip link set wlan1 up >/dev/null 2>&1", shell=True)
    subprocess.run("ip link set wlan0 up >/dev/null 2>&1", shell=True)
    NetworkManager.NetworkManager.ActivateConnection(connection, device, "/")
    logging.debug("became master")


def is_connected_to_wifi(ssid: str = "") -> bool:
    logging.debug(f"is connected to {ssid or 'wifi'}?")
    active_connections = NetworkManager.NetworkManager.ActiveConnections
    for conn in active_connections:
        if conn.Type == "802-11-wireless" and (
            ssid == ""
            or ssid == conn.Connection.GetSettings().get("802-11-wireless", {}).get("ssid")
        ):
            logging.debug("IS connected!")
            return True
    logging.debug(f"is not connected to {ssid or 'wifi'}")
    return False

def is_master() -> bool:
    logging.debug("am i master?")
    active_connections = NetworkManager.NetworkManager.ActiveConnections
    for conn in active_connections:
        if conn.Devices[0].Interface == 'wlan1':
            logging.debug("i am the master")
            return True
    logging.debug("i am no master")
    return False

def stop_being_master() -> None:
    logging.debug("stopping being a master")
    active_connections = NetworkManager.NetworkManager.ActiveConnections
    for conn in active_connections:
        if conn.Devices[0].Interface == 'wlan1':
            NetworkManager.NetworkManager.DeactivateConnection(conn)
            break
    logging.debug("i am master no more")

def dbus_setup() -> None:
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    logging.debug("starting app")
    dbus_setup()
    if is_master_present():
        if not is_connected_to_wifi(MASTER_SSID):
            connect_to_master_wifi()
        if is_master():
            stop_being_master()
    else:
        if not is_connected_to_wifi():
            connect_to_client_wifi()
        if not is_master():
            become_master()
    logging.debug("done!")
