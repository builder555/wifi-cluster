#/bin/sh

MASTER_SSID=${SSID:-MyInternalWifi}
MASTER_PSK=${PSK:-0suPersEcurepSk0}
SAVED_WIFI_CONFIG_NAME=${SAVED_WIFI_CONFIG:-balena-wifi-01}
WIFI_DEVICE=${WIFI_DEVICE_NAME:-wlan0}
MASTER_AP_CONFIG_NAME=MasterAP

function is_master_present {
    echo "Checking for master wifi..."
    iw dev $WIFI_DEVICE scan | grep "SSID: $MASTER_SSID" > /dev/null
}

function is_connected_device {
    echo "Is connected on $1?"
    nmcli con show --active | sed 1d | awk -F"  "+ '{print $4}' | grep $1 > /dev/null
}

function is_connected_ssid {
    echo "Is connected to '$1'?"
    iw dev $WIFI_DEVICE link | grep SSID | grep $1 > /dev/null
}

function am_master {
    # the only way this device is master is if it's connected on virtual device wlan1
    is_connected_device wlan1
}

function connect_to_client_wifi {
    nmcli con up $SAVED_WIFI_CONFIG_NAME
}

function connect_to_master_wifi {
    echo "Connecting to master wifi"
    nmcli dev wifi connect $MASTER_SSID password $MASTER_PSK
}

function add_master_ap_connection {
    echo "Adding master AP connection"
    nmcli con add type wifi ifname wlan1 mode ap con-name $MASTER_AP_CONFIG_NAME ssid $MASTER_SSID
    nmcli con modify $MASTER_AP_CONFIG_NAME wifi.band bg
    # nmcli con modify $MASTER_AP_CONFIG_NAME wifi.channel 1
    nmcli con modify $MASTER_AP_CONFIG_NAME 802-11-wireless-security.key-mgmt wpa-psk
    nmcli con modify $MASTER_AP_CONFIG_NAME 802-11-wireless-security.proto rsn
    nmcli con modify $MASTER_AP_CONFIG_NAME 802-11-wireless-security.group ccmp
    nmcli con modify $MASTER_AP_CONFIG_NAME 802-11-wireless-security.pairwise ccmp
    nmcli con modify $MASTER_AP_CONFIG_NAME 802-11-wireless-security.psk $MASTER_PSK
    nmcli con modify $MASTER_AP_CONFIG_NAME ipv4.method shared
}

function is_connection_configured {
    nmcli con show | sed 1d | awk -F"  "+ '{print $1}' | grep $1 > /dev/null
}

function become_master {
    echo "becoming master"
    ip link set wlan1 down >/dev/null 2>&1
    # delete the wlan1 interface since it can return 'busy' sometimes, when activating it
    iw dev wlan1 del >/dev/null 2>&1
    echo "taking down wifi"
    ip link set $WIFI_DEVICE down >/dev/null 2>&1
    echo "adding interface"
    iw dev $WIFI_DEVICE interface add wlan1 type __ap
    if ! is_connection_configured $MASTER_AP_CONFIG_NAME; then
        echo "MastAP not configured"
        add_master_ap_connection
    else
        echo "MasterAP already configured!"
    fi
    ip link set $WIFI_DEVICE up >/dev/null 2>&1
    ip link set wlan1 up >/dev/null 2>&1
    echo "became master!"
}

function stop_being_master {
    echo "Stopping master AP (if on)"
    ip link set wlan1 down >/dev/null 2>&1
}

function is_down {
    cat /sys/class/net/$1/operstate | grep down > /dev/null
}

echo "Start!"

while true; do
    echo "waiting for the next run..."
    sleep 30

    if is_down $WIFI_DEVICE; then
        ip link set $WIFI_DEVICE up
    fi

    if is_connected_ssid "$MASTER_SSID"; then
        echo "Connected to master!"
        continue
    fi

    echo "Not conected to master wifi"
    if is_master_present; then
        echo "A master is present!"
        stop_being_master
        connect_to_master_wifi
        continue
    fi

    echo "No master present!"
    if ! am_master; then
        echo "I am no master!"
        become_master
    else
        echo "already master"
    fi
    if ! is_connected_device $WIFI_DEVICE; then
        echo "Not connected to wifi"
        connect_to_client_wifi
    else
        echo "already connected"
    fi
done

echo "Done!"
