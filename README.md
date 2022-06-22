## WANDOWN

Uses paramiko to log into my home IOS router and do basic stuff that I can automate if needed

#### Usage
As always, however you want to, need to ensure variables cpe_ip, cpe_un, and cpe_pw are populated correctly

To run a simple direct command-
```
wandown.py direct "sh ip int br"
```
To run indirect programmed commands-
```
wandown.py reset gi0
wandown.py default_route
```

### Use case- 
- If my nbn services goes down, have clearly lost WAN connectivity.
- I would normally log into the router, reset (shut/no shut) the interface the nbn NTD connects to, turn on DHCP logging, and see if the interface picks up a new IPv4 address from my ISP
- If nbn's layer 2 is down, I'll typically get something like this come via the DHCP log
```
DHCP: QScan: Timed out Selecting state%Unknown DHCP problem.. No allocation possible
```

### Things to add-
- Want to implement a flow to turn on DHCP logging and wait for output that matches the above DHCP error or subsequent corresponding DHCP allocation
- Some flags to change some of the built in SSH settings

### Helpful links
- https://docs.paramiko.org/en/stable/api/client.html
- https://docs.paramiko.org/en/stable/api/channel.html
