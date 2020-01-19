"""
NordVPN Server Finder
github/trishmapow, 2020

v3.0.0
- use recommendations API (faster, but no more mbps data)
- use logging module
- refactoring
"""

import argparse
import logging
from operator import itemgetter
import platform
import subprocess

import requests
from tabulate import tabulate

NORD_API_BASE = "https://api.nordvpn.com/v1"
DEFAULT_MAX_LOAD = 30


def get_country_id(country_code: str):
    url = NORD_API_BASE + "/servers/countries"

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


def get_servers(country_code: str, city: str = None, max_load: int = DEFAULT_MAX_LOAD):
    # trial and error, undocumented API
    fields = [
        "fields[servers.name]",
        "fields[servers.locations.country.code]",
        "fields[servers.locations.country.city.name]",
        "fields[station]",
        "fields[load]",
        "fields[servers.groups.title]",
    ]

    country_id = get_country_id(country_code)
    if country_id is None:
        raise ValueError("Country id not found. Check that country code is correct.")
    country_filter = f"filters[country_id]={country_id}"
    url = (
        NORD_API_BASE
        + "/servers/recommendations?limit=16384&"
        + "&".join(fields)
        + f"&{country_filter}"
    )

    servers = requests.request("GET", url)
    filtered = [srv for srv in servers.json() if srv["load"] <= max_load]

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
    parser.add_argument(
        "--fping",
        action="store_true",
        help="show avg ping (ms) for servers, requires 'fping'",
    )
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    # control debug (urllib shows requests by default)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.disable()

    # check system is linux and fping exists
    if args.fping:
        if platform.system().lower() == "linux":
            f = subprocess.run(["which", "fping"], stdout=subprocess.DEVNULL)
            if f.returncode != 0:
                parser.error("fping not found")
        else:
            parser.error("fping only supported on Linux")

    # parse loc
    loc = [x.strip() for x in args.location.split(",")]
    if len(loc) == 2:
        city = loc[0]
        country = loc[1]
    elif len(loc) == 1:
        city = None
        country = loc[0]
    else:
        parser.error("'city, country_code' or 'country_code' expected")

    # parse load
    if args.load is not None:
        if args.load >= 1 and args.load <= 99:
            servers = get_servers(country, city, args.load)
        else:
            parser.error("load should be between 1 and 99 percent")
    else:
        servers = get_servers(country, city)
    logging.debug(f"city={city} country={country} load={args.load or DEFAULT_MAX_LOAD}")

    # construct table of servers sorted by ascending load
    headers = ["Name", "Load %", "IP", "Groups"]
    x = [
        [
            s["name"],
            s["load"],
            s["station"],
            (", ".join([g["title"] for g in s["groups"]][:-1])),
        ]
        for s in sorted(servers, key=itemgetter("load"))
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
            f"{len(servers)} servers online in {city or ''} {country} with <{args.load or DEFAULT_MAX_LOAD}% load"
        )
