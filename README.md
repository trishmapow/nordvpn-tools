# nordvpn-tools

## nordvpn_best.py v2.1
Outputs a table of servers in the specified city and country that have a load % below MAX_LOAD (default 30). 

Requirements: `pip3 install requests tabulate`. 

v2.1 optional requirement `fping` to show ping times to servers.

v2 uses new NordVPN endpoint /v1/servers which has much more server info, reverse_geocode no longer needed.

```
usage: nordvpn_best.py [-h] [--load LOAD] [--debug] [--fping] LOC

Shows low load NordVPN servers in a given city and/or country.

positional arguments:
  LOC          'city, country_code' or 'country_code' e.g. US, GB

optional arguments:
  -h, --help   show this help message and exit
  --load LOAD  set maximum load (1-99)
  --debug
  --fping      show avg ping (ms) for servers, requires 'fping'
```

Sample output:
```
$ python3 nordvpn_best.py 'Sydney, AU' --load 10 --fping                                                                                    04:40:03
Name              Load %    Mbps  IP               Groups                       Ping (ms)
--------------  --------  ------  ---------------  -------------------------  -----------
Australia #197         7     150  104.222.131.42   Standard VPN servers, P2P         6.07
Australia #205         7     150  45.121.210.197   Standard VPN servers, P2P         5.9
Australia #207         5     150  45.121.210.199   Standard VPN servers, P2P         5.84
Australia #208         8     150  45.121.210.200   Standard VPN servers, P2P         5.72
Australia #214         8     130  43.245.163.165   Standard VPN servers, P2P         5.99
Australia #219         7     130  43.245.163.171   Standard VPN servers, P2P         5.29
Australia #227         8     130  43.245.163.181   Standard VPN servers, P2P         5.84
Australia #263         7     190  144.48.36.3      Standard VPN servers, P2P         5.73
Australia #264         9     190  144.48.36.5      Standard VPN servers, P2P         5.84
Australia #296         8     800  144.48.36.27     Standard VPN servers, P2P         5.82
Australia #390         7     300  103.212.227.149  Standard VPN servers, P2P         5.8
Australia #391         9     300  103.212.227.115  Standard VPN servers, P2P         5.88
Australia #421         6     350  144.48.36.83     Standard VPN servers, P2P         5.82
14 servers online in Sydney AU with <10% load
```

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
- v2.0: https://github.com/trishmapow/nordvpn-tools/releases/tag/v2.0
- v1.0: https://github.com/trishmapow/nordvpn-tools/releases/tag/v1.0