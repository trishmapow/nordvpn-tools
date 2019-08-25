import requests
import json
import reverse_geocode
from tabulate import tabulate
import sys

NORD_API_BASE = "https://api.nordvpn.com"
MAX_LOAD = 30

def get_servers(country: str, city: str = None):
    servers = requests.request("GET", NORD_API_BASE + "/server")
    filtered = [srv for srv in servers.json() if srv['country'].lower() == country.lower()]
    if city is None:
        return filtered
    else:
        return list(filter(lambda srv: reverse_geocode.search([(float(srv["location"]["lat"]), float(srv["location"]["long"]))])[0]["city"].lower() == city.lower(), filtered))

if __name__ == '__main__':
    if len(sys.argv[1:]) == 1:
        try:
            arg1 = int(sys.argv[1])
            if arg1 < 1 or arg1 > 99:
                print("Load arg between 1-99")
                exit(1)
            else:
                MAX_LOAD = arg1
        except ValueError:
            print("Args: MAX_LOAD (integer 1-99)")
            exit(1)

    loc = input("Enter [CITY] [COUNTRY]: ").split()
    if len(loc) != 2:
        print("Need two arguments")
        exit(1)
    city = loc[0]
    country = loc[1]
    servers = get_servers(country, city)

    x = [[s['name'], s['ip_address'], s['load'], (', '.join([cat['name'] for cat in s['categories']]))] for s in servers if int(s['load']) < MAX_LOAD]
    print(tabulate(x, headers=["Name", "IP", "Load %", "Categories"]))
    print(f"{len(servers)} servers online in {city}, {country} (approximate)")
    print(f"{len(x)} of which have <{MAX_LOAD}% load")
