from scapy.all import *

#Port Scanning with spoofed IP of ws3
res, unans = sr( IP(src="10.1.0.3", dst="10.1.0.2")/TCP(flags="S", dport=(1,1024)))
#View Summary
res.nsummary()

#Send a DNS request in the name of WS2 so that WS2 gets a DNS response in port 8 that was previously checked to be open
send(IP(src="10.1.0.2",
dst="10.12.0.20")/UDP(dport=8)/DNS(rd=1,qd=DNSQR(qname="example.com")))
