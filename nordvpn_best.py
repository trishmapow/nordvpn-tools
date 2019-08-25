import requests
import json
import reverse_geocode
from tabulate import tabulate

NORD_API_BASE = "https://api.nordvpn.com"
MAX_LOAD = 30

def get_servers(country: str, city: str = None):
    servers = requests.request("GET", NORD_API_BASE + "/server")
    filtered = [srv for srv in servers.json() if srv['country'].lower() == country.lower()]
    for srv in filtered:
        srv["city"] = reverse_geocode.search([(float(srv["location"]["lat"]), float(srv["location"]["long"]))])[0]["city"]
        if city is not None and srv["city"] != city:
            filtered.remove(srv)
    return filtered

if __name__ == '__main__':
    loc = input("Enter [CITY] [COUNTRY (optional)]: ").split()
    city = loc[0]
    country = loc[1] if len(loc) == 2 else "Australia"
    servers = get_servers(country, city)
    x = [[s['name'], s['ip_address'], s['load'], (', '.join([cat['name'] for cat in s['categories']]))] for s in servers if int(s['load']) < MAX_LOAD]
    print(tabulate(x, headers=["Name", "IP", "Categories", "Load %"]))
    print(f"{len(servers)} servers online in {city}, {country} (approximate)")
    print(f"{len(x)} of which have <{MAX_LOAD}% load")