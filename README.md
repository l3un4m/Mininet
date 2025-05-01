# comp-sec2
## Firewalls
For this report it's asked of us to implement firewalls corresponding to what a normal enterprise network would look like so we added *nft rules* for [**R1**](https://github.com/l3un4m/comp-sec2/blob/main/firewall/r1.nft) and for [**R2**](https://github.com/l3un4m/comp-sec2/blob/main/firewall/r2.nft) with a **drop policy** that resulted in the following *pingall*
![a](/screenshots/pingall.png)

## DNS Reflection
For this attack we start by scanning the ports that are open in the work station(for example) and send a DNS request in the name of the WorkStations so that they get the reply which is bigger than the request sent by the attacker resulting in a DOS if multiplied

## Arp Poisoning
For this attack we use a simple scapy command to perform the arp poisoning.
´´´
sendp(Ether(dst='TARGET-MAC')/ARP(op="who-has", psrc='DEF\_GATEWAY-IP', pdst='TARGET-IP'),
inter=0.2, loop=1)
´´´
This command will tell our target to change the MAC Address of it's default gateway to our own MAC address, this way all the traffic coming from our target will reach us and then be forwarded to it's original destination.
