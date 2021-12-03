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
- Can run in a docker container

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
- [x] can create wifi 
- [x] can connect to wifi
- [x] access internet through wifi
- [x] * create wifi after reboot --> _yes, but need to re-add wlan1 interface_
- [x] add lan interface from within a container
- [x] activate existing wifi from within a container
- [x] deactivate wifi from within a container
- [x] create new wifi connection from within a container
- [x] list available connections from container
- [x] connect to master wifi automatically
- [x] can become master
- [x] can become slave
- [ ] <font color="red">remove/re-add virtual wlan1 interface if it's unavailable</font>
- [ ] can turn on physical wifi device, if it's off
- [ ] tests
- [ ] create different configurations: 
    - [x] star
    - [ ] mesh
    - [ ] chain
    - [ ] clusters
    - [ ] ring
