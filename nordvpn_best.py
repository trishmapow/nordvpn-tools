import requests
import json
import reverse_geocode
from tabulate import tabulate
import sys
import argparse

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
    parser = argparse.ArgumentParser(description="Shows low load NordVPN servers in a given city and/or country.")
    parser.add_argument('--city', help="find servers in '[city] [country]'")
    parser.add_argument('--country', help="find servers in [country] (full name)")
    parser.add_argument('--load', type=int, help="set maximum load (1-99)")
    args = parser.parse_args()

    if not (args.city or args.country):
        parser.error("No action requested, choose --city or --country")
    elif args.city:
        loc = args.city.split(" ")
        if len(loc) != 2:
            parser.error("Expected [city] [country]")
        city = loc[0]
        country = loc[1]
    else:
        city = None
        country = args.country

    if args.load is not None and args.load >= 1 and args.load <= 99:
        MAX_LOAD = args.load

    servers = get_servers(country, city)

    x = [[s['name'], s['ip_address'], s['load'], (', '.join([cat['name'] for cat in s['categories']]))] for s in servers if int(s['load']) < MAX_LOAD]
    print(tabulate(x, headers=["Name", "IP", "Load %", "Categories"]))
    print(f"{len(servers)} servers online in {city} {country} (approximate)")
    print(f"{len(x)} of which have <{MAX_LOAD}% load")
