### Check if your device supports AP mode

`iw phy | grep -i "supported interface" -A10`


### Commands to add a virtual wifi device as AP and activate a connection:

```bash
# take down the physical device just in case
ifconfig wlan0 down
# add the virtual device
iw dev wlan0 interface add wlan1 type __ap
# add connection details
nmcli con add type wifi ifname wlan1 mode ap con-name MYAP1 ssid MyCoolAP
nmcli con modify MYAP1 wifi.band bg
nmcli con modify MYAP1 wifi.channel 1
nmcli con modify MYAP1 wifi-security.key-mgmt wpa-psk
nmcli con modify MYAP1 wifi-security.proto rsn
nmcli con modify MYAP1 wifi-security.group ccmp
nmcli con modify MYAP1 wifi-security.pairwise ccmp
nmcli con modify MYAP1 wifi-security.psk 11223344
nmcli con modify MYAP1 ipv4.method shared
# bring up the virtual and physical devices
ifconfig wlan1 up
ifconfig wlan0 up
```

### Other commands

```bash
# nmcli con up MYAP1
# inside a docker container:
ip link set wlan1 up
ip link set wlan0 up

# to delete wlan1:
iw dev wlan1 del
```