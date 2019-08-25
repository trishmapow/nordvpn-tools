# nordvpn-tools

## nordvpn_best.py
Outputs a table of servers in the specified city and country that have a load % below MAX_LOAD (default 30). 

Requirements: `pip3 install requests reverse_geocode tabulate`. Uses the reverse_geocode library to (very roughly) convert coordinates to cities (offline), try larger cities if not working.

To run: `python3 nordvpn_best.py [OPTIONAL MAX_LOAD 1-99]`.

Sample output:
```
~/P/nordvpn-tools (master|✔) $ python3 nordvpn_best.py 20
Enter country (full name): Australia 
Enter city: Sydney
Name            IP                 Load %  Categories
--------------  ---------------  --------  -------------------------
Australia #215  43.245.163.166         19  Standard VPN servers, P2P
Australia #216  43.245.163.168         17  Standard VPN servers, P2P
Australia #219  43.245.163.171         17  Standard VPN servers, P2P
Australia #226  43.245.163.180         15  Standard VPN servers, P2P
Australia #264  144.48.36.5            15  Standard VPN servers, P2P
Australia #265  45.248.76.74           19  Standard VPN servers, P2P
Australia #295  144.48.36.35           15  Standard VPN servers, P2P
Australia #389  103.212.227.147        15  Standard VPN servers, P2P
Australia #390  103.212.227.149        19  Standard VPN servers, P2P
Australia #392  103.212.227.117        17  Standard VPN servers, P2P
Australia #421  144.48.36.83           14  Standard VPN servers, P2P
Australia #423  103.212.227.155        15  Standard VPN servers, P2P
Australia #425  103.212.227.163        19  Standard VPN servers, P2P
Australia #429  103.212.227.179        16  Standard VPN servers, P2P
Australia #430  103.212.227.181        15  Standard VPN servers, P2P
68 servers online in Sydney, Australia (approximate)
15 of which have <20% load

```
