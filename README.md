# nordvpn-tools

## nordvpn_best.py
Outputs a table of servers in the specified city and country that have a load % below MAX_LOAD (default 30).

Requirements: `pip3 install requests reverse_geocode tabulate`. Uses the reverse_geocode library to (very roughly) convert coordinates to cities (offline), try larger cities if not working.

Sample output:
```
~/P/nordvpn-helper $ python3 nordvpn_best.py                            22:39:23
Enter [CITY] [COUNTRY (optional)]: Sydney Australia
Name            IP                 Categories  Load %
--------------  ---------------  ------------  -------------------------
Australia #197  104.222.131.42             26  Standard VPN servers, P2P
Australia #201  104.222.131.46             29  Standard VPN servers, P2P
Australia #202  104.222.131.47             16  Standard VPN servers, P2P

... etc ...

Australia #203  104.222.131.48             18  Standard VPN servers, P2P
Australia #207  45.121.210.199             27  Standard VPN servers, P2P
Australia #446  103.107.196.187            19  Standard VPN servers, P2P
154 servers online in Sydney, Australia (approximate)
55 of which have <30% load
```
