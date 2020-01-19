# nordvpn-tools

## Downloads (standalone)
Windows: [nordvpn_best.exe](dist/nordvpn_best.exe)

Linux: [nordvpn_best](dist/nordvpn_best)

## nordvpn_best.py v3
Outputs a table of servers in the specified city and country that have a load % below MAX_LOAD (default 30). 

Python requirements: `pip3 install -r requirements.txt`

```
$ python3 nordvpn_best.py -h
usage: nordvpn_best.py [-h] [--load LOAD] [--fping] [--debug] LOC

Shows low load NordVPN servers in a given city and/or country.

positional arguments:
  LOC          'city, country_code' or 'country_code' e.g. US, GB

optional arguments:
  -h, --help   show this help message and exit
  --load LOAD  set maximum load (1-99)
  --fping      show avg ping (ms) for servers, requires 'fping'
  --debug
```

Sample output:
```
$ python3 nordvpn_best.py 'Brisbane, AU' --load 20 --fping
Name              Load %  IP              Groups                       Ping (ms)
--------------  --------  --------------  -------------------------  -----------
Australia #462        13  103.137.12.211  Standard VPN servers, P2P         31.6
Australia #413        15  103.137.12.147  Standard VPN servers, P2P         31.2
Australia #436        16  103.137.12.197  Standard VPN servers, P2P         39
Australia #464        16  103.137.12.227  Standard VPN servers, P2P         38.2
Australia #320        17  144.48.39.43    Standard VPN servers, P2P         40.1
Australia #410        17  103.137.12.133  Standard VPN servers, P2P         41.2
Australia #411        18  103.137.12.139  Standard VPN servers, P2P         40.3
Australia #316        18  45.248.77.139   Standard VPN servers, P2P         39.1
Australia #388        18  45.248.77.133   Standard VPN servers, P2P         36.9
Australia #355        18  45.248.77.171   Standard VPN servers, P2P         35.5
Australia #466        19  103.137.12.243  Standard VPN servers, P2P         35.4
Australia #465        19  103.137.12.235  Standard VPN servers, P2P         36.8
Australia #306        19  45.248.77.187   Standard VPN servers, P2P         35.1
Australia #318        20  144.48.39.27    Standard VPN servers, P2P         33
Australia #387        20  45.248.77.131   Standard VPN servers, P2P         32.8
Australia #302        20  45.248.77.75    Standard VPN servers, P2P         32.3
17 servers online in Brisbane AU with <20% load
```

### Changelog
- v3.0 no longer shows mbps info for each server, unfortunately NordVPN has removed this from the specifications field. 

- v2.1 optional system requirement: `fping` to show ping times to servers

- v2.0 uses new NordVPN endpoint /v1/servers which has much more server info, reverse_geocode no longer needed.

### Run With Docker

Build locally:
```shell
docker build . -t trishmapow/nordvpn-tools
```
Or Pull from Dockerhub:
```shell
docker pull trishmapow/nordvpn-tools
```
Then run with
```shell
docker run -it trishmapow/nordvpn-tools <Parameters>
```

### Older versions
Check the [releases page](https://github.com/trishmapow/nordvpn-tools/releases).
