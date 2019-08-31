'''
NordVPN Server Finder
github/trishmapow, 2019

v2.0 using new Nord API
'''

import requests
from tabulate import tabulate
import argparse

NORD_API_BASE = "https://api.nordvpn.com/v1"
MAX_LOAD_DEFAULT = 30
VERBOSE = False

def get_servers(country_code: str, city: str = None, max_load: int = MAX_LOAD_DEFAULT):
    # trial and error, undocumented API
    fields = ["fields[servers.name]", "fields[servers.locations.country.code]", "fields[servers.locations.country.city.name]"]
    fields.extend(["fields[station]", "fields[load]", "fields[specifications]", "fields[servers.groups.title]"])

    # perhaps there's a country filter? would reduce network usage
    load_filter = f"filters[servers.load][$lt]={max_load}"
    url = NORD_API_BASE + "/servers?limit=16384&" + '&'.join(fields) + f"&{load_filter}"
    if (VERBOSE):
        print(url)

    servers = requests.request("GET", url)
    filtered = [srv for srv in servers.json() if srv['locations'][0]['country']['code'].lower() == country_code.lower()]
    if city is None:
        return filtered
    else:
        return [srv for srv in filtered if srv['locations'][0]['country']['city']['name'].lower() == city.lower()]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Shows low load NordVPN servers in a given city and/or country.")
    parser.add_argument('location', metavar='LOC', type=str, help="'city, country_code' or 'country_code' e.g. US, GB")
    parser.add_argument('--load', type=int, help="set maximum load (1-99)")
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    if args.debug:
        VERBOSE = True

    loc = list(map(lambda x: x.strip(), args.location.split(',')))
    if len(loc) == 2:
        city = loc[0]
        country = loc[1]
    elif len(loc) == 1:
        city = None
        country = loc[0]
    else:
        parser.error("'city, country_code' or 'country_code' expected")

    if VERBOSE:
        print(f"city={city} country={country}")

    if args.load is not None and args.load >= 1 and args.load <= 99:
        servers = get_servers(country, city, args.load)
    else:
        servers = get_servers(country, city)

    headers = ["Name", "Load %", "Mbps", "IP", "Groups"]
    x = [[s['name'], s['load'], [x['values'][0]['value'] for x in s['specifications'] if x['identifier'] == 'network_mbps'][0], s['station'], (', '.join([g['title'] for g in s['groups']][:-1]))] for s in servers]

    print(tabulate(x, headers=headers))
    print(f"{len(servers)} servers online in {city or ''} {country} with <{args.load or MAX_LOAD_DEFAULT}% load")
