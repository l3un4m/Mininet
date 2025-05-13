# Mininet
**Note:** For an easier reading of the report it's advised to access https://github.com/l3un4m/Mininet. No code is shown in the report, only it's explanation and results. Every section and subsection has an hyperlink to the files in question.
Additionally there are provided scripts that mimick an attempt of each attack implemented, these can be used to compare what happens before and after implementing the defenses. To run them simply do:
```
source examples/[desired_attack].sh
```
## Firewalls
For this report it's asked of us to implement firewalls corresponding to what a normal enterprise network would look like so I added *nft rules* for [**R1**](https://github.com/l3un4m/Mininet/blob/main/firewall/r1.nft) and for [**R2**](https://github.com/l3un4m/Mininet/blob/main/firewall/r2.nft) with a **drop policy** for **R1** and an **accept policy** for **R2** that resulted in the following *pingall*:

![a](/screenshots/pingall.jpg)

**Note:** These rules are applied automatically when the topology is launched, for that I simply had to update the topo.py to apply them at "boot".
## Network Scan
### Attack
**Note:** For this attack to be shown we need to have **R1** in our ARP Table so for that simpli ping **WS3** from **R1**
```
r1 ping ws3
```
For this [attack](https://github.com/l3un4m/Mininet/blob/main/attack/scan.py) we start by sending *ICMP Echo Requests* to every address in the given subnet and saving the ones that reply so that after we send TCP packets with the SYN flag to every port in the addresses that replied and we wait for a TCP response packet with the SYN-ACK flag in order to find open ports in the addresses that we found.
```
[Attacker] python3 attack/scan.py [Victim Subdomain]
```

![scan](/screenshots/scan1.jpg)

### Defense
**Note:**To visualize this mitigation it's needed to send a ping from **R1** to **WS3** to reset it's ARP Table correctly.
```
r1 ping ws3
```
For this [mitigation](https://github.com/l3un4m/Mininet/blob/main/defense/r2_scan.nft) we simply insert four rules in the *filter* table of **R2** to limit the rate of accepted **SYN** packets to **2 per second** and **icmp** to **2 per second** preventing both types of scanning.
```
r2 nft flush ruleset
r2 nft -f defense/r2_scan.nft
```
As we can see, when we run the same attack this time it can't see any of our hosts:

![scan2](/screenshots/scan_def.jpg)
**Note:** This attack is very useful since for the next attacks we need to know about what IP's are being used and their open ports!
## DNS Reflection
### Attack
For this [attack](https://github.com/l3un4m/Mininet/blob/main/attack/dns.py) we know that the DNS port is **5353** so we send a DNS request in the name of the WorkStations so that they get the reply (in the open port 5353) which is bigger than the request sent by the attacker resulting in a DOS if multiplied.
```
[Attacker] python3 attack/dns.py [Victim's IP] [DNS IP] [Open Port in Victim]
```
![dns](/screenshots/dns.jpg)
As we can see, a DNS request is being sent with a spoofed IP of WS2(when in reality it comes from internet) and the response is bigger than the request meaning that it's profitable bandwithwise.
### Defense
For this [mitigation](https://github.com/l3un4m/Mininet/blob/main/defense/r2_dns.nft) I updated **R2**'s Firewall rules to block any traffic incoming from the internet pretending to be from DMZ or the Workstations:
```
r2 nft flush ruleset
r2 nft -f defense/r2_dns.nft
```
Since this rule only applies to traffic coming from outside the network I also added a [rule](https://github.com/l3un4m/Mininet/blob/main/defense/r1_dns.nft) that limits the rate of received dns packets to 5 per second so that if hosts inside DMZ are compromised they can't be used to perform a DNS Reflection that would cause DOS.
```
r1 nft flush ruleset
r1 nft -f defense/r1_dns.nft
```

![dns\_def](/screenshots/dns_def.jpg)

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
For this [mitigation](https://github.com/l3un4m/Mininet/blob/main/defense/arp.sh) we simply use *arptables* to create a rule that will drop any arp packets that come from an IP source that doesn't match it's MAC Address, in this example **WS2** was pretending to be **R1** but the MAC Address was still **WS2's** so it's blocked.
```
[Victim] source defense/arp.sh [Default Gateway's IP]
```
As we can see the arp table of the victim remais unchanged.

![arp3](/screenshots/arp_def.jpg)

## SYN Flooding
### Attack
For this [attack](https://github.com/l3un4m/Mininet/blob/main/attack/flood.py) we simply flood a victim with SYN packets coming from spoofed IP's preventing new connections to be established to the victim.

Here we can see all the spoofed SYN's and SYN-ACK's being sent:

![flood](/screenshots/flood1.jpg)
Here we see the amount of SYN\_RECV's on the **http** server:

![flood2](/screenshots/flood2.jpg)

### Defense
For this [mitigation](https://github.com/l3un4m/Mininet/blob/main/defense/r2_flood.nft) we simply insert two rules in the *filter* table to limit the rate of accepted **SYN** packets to 5 per second.
```
r2 nft flush ruleset
r2 nft -f defense/r2_flood.nft
```

![flood3](/screenshots/flood_def.jpg)
We can see in the previous figure that we still have **45** SYN\_REC but when looking at the amount of dropped packets we see a number of **400** packets that were dropped by our new firewall rule meaning that it doesn't erase the issue but impossibilitates it from filling our SYN\_RECV entry table. As an addition I changed the default wait time of ~60 seconds
to free up SYN\_RECV entries to ~6-10 seconds with the command:
```
[Victim Host] sysctl -w net.ipv4.tcp_synack_retries=2
```
This means that clients with a slower connection might failt to start a tcp connection but it's what I consider to be the best solution in the presence of an attack like this.
## SSH Brute-Force
**Note:** For this attack we need to download a wordlist but Inginious didn't accept a zip with it because it'd be too big so for simplicity reasons just clone and unzip the following repo: https://github.com/dw0rsec/rockyou.txt.git and add it to the home folder of mininet.
### Attack
For this [attack](https://github.com/l3un4m/Mininet/blob/main/attack/brute.py) I created a simple python for loop that will try every password from a given password list (rockyou.txt in this case) until it finds the correct credentials.

![brute](/screenshots/brute.jpg)

Due to performance issues I couldn't achieve the correct answer but the script seems to be working as it should.

### Defense
For this [mitigation](https://github.com/l3un4m/Mininet/blob/main/defense/r2_brute.nft) we simply redo **R2**'s firewall rules to include a threshold of 5 New SSH packets per second slowing down our opponent drastically enough to make the attack unfeasable.
```
r2 nft flush ruleset
r2 nft -f defense/r2_brute.nft
```
