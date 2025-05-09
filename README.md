# Mininet
## Firewalls
For this report it's asked of us to implement firewalls corresponding to what a normal enterprise network would look like so we added *nft rules* for [**R1**](https://github.com/l3un4m/comp-sec2/blob/main/firewall/r1.nft) and for [**R2**](https://github.com/l3un4m/comp-sec2/blob/main/firewall/r2.nft) with a **drop policy** that resulted in the following *pingall*
![a](/screenshots/pingall.png)

## DNS Reflection
### Attack
For this [attack](https://github.com/l3un4m/Mininet/blob/main/attack/dns.py) we know that the DNS port is **5353** so we send a DNS request in the name of the WorkStations so that they get the reply (in the open port 5353) which is bigger than the request sent by the attacker resulting in a DOS if multiplied.
```
[Attacker] python3 attack/dns.py [Victim's IP] [DNS IP] [Open Port in Victim]
```
![dns](/screenshots/dns1.jpg)
As we can see, a DNS request is being sent with a spoofed IP of WS2(when in reality it comes from internet) and the response is bigger than the request meaning that it's profitable bandwithwise.
### Defense

## ARP Poisoning
### Attack
For this [attack](https://github.com/l3un4m/Mininet/blob/main/attack/arp.py) we use a simple scapy script to perform the arp poisoning, to run it inside our mininet we simply have to do the following command:
```
[Attacker] python3 attack/arp.py [Victim's IP] [Victim's Default-Gateway]
```
Since the victim and the attacker need to be on the same subnetwork we assume that they have the same default-gateway something that can be easily found by the attacker with the command *arp -a [Victim's IP]*
![arp1](/screenshots/arp1.jpg)
We start by finding the MAC Address of our victim **WS3** and using it in our scapy script along with it's IP and **R1**'s(DefaultGateway) IP Address. We can see a before and after *Arp Table* of **WS3** and confirm that our attack was successful. Furthermore, if we analyse the following capture we can see that a ping from **WS3** to **DNS** passes by **WS2**.
![arp2](/screenshots/arp2.jpg)
**NOTE:** We use *inter=0.2, loop=1* to tell scapy to keep sending these packets every 0.2 seconds because if **R1** sends traffic to **WS3** the DefaultGateway MAC address will be corrected. Also after 60 seconds (in this system) the *Arp Table*'s cache is cleared and if that happens then our attack stops working.
### Defense

## Network Scan
### Attack
For this [attack](https://github.com/l3un4m/Mininet/blob/main/attack/scan.py) we start by sending *ICMP Echo Requests* to every address in the given subnet and saving the ones that reply so that after we send TCP packets with the SYN flag to every port in the addresses that replied and we wait for a TCP response packet with the SYN-ACK flag in order to find open ports in the addresses that we found.
![scan](/screenshots/scan1.jpg)

### Defense
For this [mitigation](https://github.com/l3un4m/Mininet/blob/main/defense/r2_scan.nft) we simply insert four rules in the *filter* table to limit the rate of accepted **SYN** packets to **10 per second** and **icmp** to **2 per second** preventing both types of scanning.
As we can see, when we run the same attack this time it can't see any of our hosts:
![scan](/screenshots/scan_def.jpg)

## SYN Flooding
### Attack
For this [attack](https://github.com/l3un4m/Mininet/blob/main/attack/flood.py) we simply flood a victim with SYN packets coming from spoofed IP's preventing new connections to be established to the victim.
![scan](/screenshots/flood1.jpg)
Here we can see all the spoofed SYN's and SYN-ACK's being sent.
![scan](/screenshots/flood2.jpg)
Here we see the amount of SYN\_RECV's on the **http** server.

<<<<<<< HEAD
=======
### Defense
For this [mitigation](https://github.com/l3un4m/Mininet/blob/main/defense/flood.sh) we simply insert two rules in the *filter* table to limit the rate of accepted **SYN** packets to 15 per second.
>>>>>>> 977b115 (Attacks: Complete SSH)

