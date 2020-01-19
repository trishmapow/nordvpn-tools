"""
NordVPN Server Finder
github/trishmapow, 2019

v2.1 fping support on Linux
"""

import requests
from tabulate import tabulate
import argparse
import subprocess
import platform

NORD_API_BASE = "https://api.nordvpn.com/v1"
MAX_LOAD_DEFAULT = 30
VERBOSE = False

def get_country_id(country_code: str):
    url = NORD_API_BASE + "/servers/countries"
    if VERBOSE:
        print(url)

    servers = requests.request("GET", url)
    country_id = [
        srv["id"]
        for srv in servers.json()
        if srv["code"].lower() == country_code.lower()
    ]

    if len(country_id) == 1 and type(country_id[0]) == int:
        return country_id[0]
    else:
        return None

def get_servers(country_code: str, city: str = None, max_load: int = MAX_LOAD_DEFAULT, legacy: bool = False):
    # trial and error, undocumented API
    fields = [
        "fields[servers.name]",
        "fields[servers.locations.country.code]",
        "fields[servers.locations.country.city.name]",
    ]
    fields.extend(
        [
            "fields[station]",
            "fields[load]",
            "fields[specifications]",
            "fields[servers.groups.title]",
        ]
    )

    if legacy:
        load_filter = f"filters[servers.load][$lt]={max_load}"
        url = NORD_API_BASE + "/servers?limit=16384&" + "&".join(fields) + f"&{load_filter}"

        servers = requests.request("GET", url)
        filtered = [
            srv
            for srv in servers.json()
            if srv["locations"][0]["country"]["code"].lower() == country_code.lower()
        ]
    else:
        country_id = get_country_id(country_code)
        if country_id is None:
            raise ValueError("Country id not found. Check that country code is correct.")
        country_filter = f"filters[country_id]={country_id}"
        url = NORD_API_BASE + "/servers/recommendations?limit=16384&" + "&".join(fields) + f"&{country_filter}"

        servers = requests.request("GET", url)
        filtered = [
            srv
            for srv in servers.json()
            if srv["load"] <= max_load
        ]
    
    if VERBOSE:
        print(url)
    
    if city is None:
        return filtered
    else:
        return [
            srv
            for srv in filtered
            if srv["locations"][0]["country"]["city"]["name"].lower() == city.lower()
        ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Shows low load NordVPN servers in a given city and/or country."
    )
    parser.add_argument(
        "location",
        metavar="LOC",
        type=str,
        help="'city, country_code' or 'country_code' e.g. US, GB",
    )
    parser.add_argument("--load", type=int, help="set maximum load (1-99)")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument(
        "--fping",
        action="store_true",
        help="show avg ping (ms) for servers, requires 'fping'",
    )
    parser.add_argument(
        "--show-mbps",
        action="store_true",
        help="show server mbps, uses legacy API, slower & uses more data"
    )
    args = parser.parse_args()

    if args.debug:
        VERBOSE = True
    show_mbps = args.show_mbps

    # check system is linux and fping exists
    if args.fping:
        if platform.system().lower() == "linux":
            f = subprocess.run(["which", "fping"], stdout=subprocess.DEVNULL)
            if f.returncode != 0:
                parser.error("fping not found")
        else:
            parser.error("fping only supported on Linux")

    # parse loc
    loc = list(map(lambda x: x.strip(), args.location.split(",")))
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

    # parse load
    if args.load is not None and args.load >= 1 and args.load <= 99:
        servers = get_servers(country, city, args.load, legacy=show_mbps)
    else:
        servers = get_servers(country, city, legacy=show_mbps)

    # construct table of servers sorted by ascending load
    if show_mbps:
        headers = ["Name", "Load %", "Mbps", "IP", "Groups"]
        x = [
            [
                s["name"],
                s["load"],
                [
                    x["values"][0]["value"]
                    for x in s["specifications"]
                    if x["identifier"] == "network_mbps"
                ][0],
                s["station"],
                (", ".join([g["title"] for g in s["groups"]][:-1])),
            ]
            for s in sorted(servers, key=lambda server: server['load'])
        ]
    else:
        headers = ["Name", "Load %", "IP", "Groups"]
        x = [
            [
                s["name"],
                s["load"],
                s["station"],
                (", ".join([g["title"] for g in s["groups"]][:-1])),
            ]
            for s in sorted(servers, key=lambda server: server["load"])
        ]

    if len(servers) == 0:
        print(
            f"No servers found with given location and load. Check location and/or increase load parameter."
        )
    else:
        if args.fping:
            ips = [s["station"] for s in servers]
            fping_args = ["fping", "-q", "-i 1", "-c 3"]
            fping_args.extend(ips)
            f = subprocess.run(
                fping_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            avgs = [
                (l.split("/")[7] if len(l.split("/")) == 9 else "-1")
                for l in f.stderr.decode().splitlines()
            ]
            headers.append("Ping (ms)")
            x = [x[row] + [avgs[row]] for row in range(0, len(x) - 1)]

        # output
        print(tabulate(x, headers=headers))
        print(
            f"{len(servers)} servers online in {city or ''} {country} with <{args.load or MAX_LOAD_DEFAULT}% load"
        )