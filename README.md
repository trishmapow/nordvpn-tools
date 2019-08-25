# nordvpn-tools

## nordvpn_best.py
Outputs a table of servers in the specified city and country that have a load % below MAX_LOAD (default 30).

Requirements: `pip3 install requests reverse_geocode tabulate`. Uses the reverse_geocode library to (very roughly) convert coordinates to cities (offline), try larger cities if not working.

Sample output:
```
~/P/nordvpn-helper $ python3 nordvpn_best.py                            22:43:57
Enter [CITY] [COUNTRY (optional)]: Sydney Australia
Name            IP                 Load %  Categories
--------------  ---------------  --------  -------------------------
Australia #195  104.222.131.40         29  Standard VPN servers, P2P
Australia #197  104.222.131.42         20  Standard VPN servers, P2P
Australia #202  104.222.131.47         25  Standard VPN servers, P2P
... etc ...
Australia #430  103.212.227.181        29  Standard VPN servers, P2P
Australia #444  103.107.196.171        26  Standard VPN servers, P2P
Australia #446  103.107.196.187        19  Standard VPN servers, P2P
154 servers online in Sydney, Australia (approximate)
55 of which have <30% load

```
