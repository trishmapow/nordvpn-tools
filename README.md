# nordvpn-tools

## nordvpn_best.py v2
Outputs a table of servers in the specified city and country that have a load % below MAX_LOAD (default 30). 

Requirements: `pip3 install requests tabulate`.

v2 uses new NordVPN endpoint /v1/servers which has much more server info, reverse_geocode no longer needed.

```
usage: nordvpn_best.py [-h] [--load LOAD] [--debug] LOC

Shows low load NordVPN servers in a given city and/or country.

positional arguments:
  LOC          'city, country_code' or 'country_code' e.g. US, GB

optional arguments:
  -h, --help   show this help message and exit
  --load LOAD  set maximum load (1-99)
  --debug
```

Sample output:
```
$ python3 nordvpn_best.py 'Sydney, AU' --load 20
Name              Load %    Mbps  IP              Groups
--------------  --------  ------  --------------  -------------------------
Australia #200        19     150  104.222.131.45  Standard VPN servers, P2P
Australia #202        13     150  104.222.131.47  Standard VPN servers, P2P
2 servers online in Sydney AU with <20% load
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
