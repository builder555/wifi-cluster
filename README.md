# WiFi Cluster

### Connect multiple wifi-enabled devices to each other and to external WiFi using a single connection.

<br>
Can create star configuration:

<pre>
 Master device --> WiFi
 ^     ^     ^
 |     |     |
dev1  dev2  dev3
</pre>

_Why?_
- Reduce the load on WiFi if devices only need to communicate with each other.
- Allow adding multiple devices if only one is authorized to connect to WiFi

_Requirements:_
 - The chip must support AP+STA operation (i.e. can connect to a wifi network and create its own AP simultaneously).
 - Runs on Linux (balenaOS)
 - balena cli

_Supported devices:_
- Intel AC 8265

### Deploying

```bash
$ balena push <deviceID>.local
```

### Run it

```
$ balena ssh <deviceID>.local wifimod
# python mgr.py
```

___OR___
```
$ scp mgr.py <yourdeviceip>:
$ ssh <yourdeviceip>
$ python mgr.py
```
---

### Known Issues
- have to manually take down wlan1 and re-add it after reboot

### TODO
- handle "wifi device is off" case
- create different configurations (mesh, chain, star, clusters, ring)
- tests