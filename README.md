# nordvpn-tools

## nordvpn_best.py
Outputs a table of servers in the specified city and country that have a load % below MAX_LOAD (default 30). 

Requirements: `pip3 install requests reverse_geocode tabulate`. Uses the reverse_geocode library to (very roughly) convert coordinates to cities (offline), try larger cities if not working.

```
usage: nordvpn_best.py [-h] [--city CITY] [--country COUNTRY] [--load LOAD]

Shows low load NordVPN servers in a given city and/or country.

optional arguments:
  -h, --help         show this help message and exit
  --city CITY        find servers in '[city] [country]'
  --country COUNTRY  find servers in [country] (full name)
  --load LOAD        set maximum load (1-99)
```

Sample output:
```
$ python3 nordvpn_best.py --city 'Sydney, Australia' --load 20                                                                                    13:07:23
Name            IP                 Load %  Categories
--------------  ---------------  --------  -------------------------
Australia #197  104.222.131.42         19  Standard VPN servers, P2P
Australia #200  104.222.131.45         17  Standard VPN servers, P2P
Australia #205  45.121.210.197         16  Standard VPN servers, P2P
Australia #213  43.245.163.164         17  Standard VPN servers, P2P
Australia #295  144.48.36.35           19  Standard VPN servers, P2P
Australia #368  69.161.194.117         17  Standard VPN servers, P2P
Australia #390  103.212.227.149        19  Standard VPN servers, P2P
Australia #392  103.212.227.117        14  Standard VPN servers, P2P
Australia #423  103.212.227.155        17  Standard VPN servers, P2P
68 servers online in Sydney, Australia (approximate)
9 of which have <20% load

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
