# comp-sec2
## Firewalls
For this report it's asked of us to implement firewalls corresponding to what a normal enterprise network would look like so we added *nft rules* for [**R1**](https://github.com/l3un4m/comp-sec2/blob/main/firewall/r1.nft) and for [**R2**](https://github.com/l3un4m/comp-sec2/blob/main/firewall/r2.nft) with a **drop policy** that resulted in the following *pingall*
![a](/screenshots/pingall.png)

## DNS Reflection
### Attack
For this attack we start by scanning the ports that are open in the work station(for example) and send a DNS request in the name of the WorkStations so that they get the reply which is bigger than the request sent by the attacker resulting in a DOS if multiplied
![dns](/screenshots/dns.jpg)
As we can see, a DNS request is being sent with a spoofed IP of WS2(when in reality it comes from internet) and the response is bigger than the request meaning that it's profitable bandwithwise.
### Defense

## ARP Poisoning
### Attack
For this attack we use a simple scapy command to perform the arp poisoning.
```
sendp(Ether(dst='TARGET-MAC')/ARP(op="who-has", psrc='DEF\_GATEWAY-IP', pdst='TARGET-IP'), inter=0.2, loop=1)
```
This command will tell our target to change the MAC Address of it's default gateway to our own MAC address, this way all the traffic coming from our target will reach us and then be forwarded to it's original destination.
### Defense
