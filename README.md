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
- Reduce the load on the host WiFi if devices only need to communicate with each other.
- Allow adding multiple devices if only one is authorized to connect to WiFi
- Can run in a docker container

_Requirements:_
 - The chip must support AP+STA operation (i.e. can connect to a wifi network and create its own AP simultaneously).
 - Runs on Linux (balenaOS)
 - balena cli

_Supported devices:_
- Intel AC 8265

### Deploying

#### Balena device:

*NB*: The device needs to be in [local mode](https://www.balena.io/docs/learn/develop/local-mode/) for these commands to work:

```bash
$ balena push <deviceID>.local
```

#### Any linux-based device:
```
$ scp mesh.sh <yourdeviceip>:
$ ssh <yourdeviceip>
# sh mesh.sh
```
---

### TODO
- [x] can create wifi 
- [x] can connect to wifi
- [x] access internet through wifi
- [x] create wifi after reboot
- [x] add lan interface from within a container
- [x] activate existing wifi from within a container
- [x] deactivate wifi from within a container
- [x] create new wifi connection from within a container
- [x] list available connections from container
- [x] connect to master wifi automatically
- [x] can become master
- [x] can become slave
- [x] remove/re-add virtual wlan1 interface if it's unavailable
- [x] can turn on physical wifi device, if it's off
- [x] use ENV vars for configuration
- [ ] tests
- [ ] create different configurations: 
    - [x] star
    - [ ] mesh
    - [ ] chain
    - [ ] clusters
    - [ ] ring
