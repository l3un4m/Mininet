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
For this attack we use a simple scapy command to perform the arp poisoning
![arp1](/screenshots/arp1.jpg)
As we can see we use the **WS3**'s IP and MAC Addresses and **R1**'s(DefaultGateway) IP Address. We can see a before and after *Arp Table* of **WS3** and confirm that our attack was successful. Furthermore, if we analyse the following capture we can see that a ping from **WS3** to **DNS** passes by **WS2**.
![arp2](/screenshots/arp2.jpg)
**NOTE:** We use *inter=0.2, loop=1* to tell scapy to keep sending these packets every 0.2 seconds because if **R1** sends traffic to **WS3** the DefaultGateway MAC address will be corrected. Also after 60 seconds (in this system) the *Arp Table*'s cache is cleared and if that happens then our attack stops working.
### Defense
