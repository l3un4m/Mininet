from scapy.all import *
import ipaddress
import argparse

parser = argparse.ArgumentParser(description="Network Scanning with Scapy")
parser.add_argument("network", help="Target network prefix")
args = parser.parse_args()

network = args.network

# Generate all host IPs from CIDR
hosts = [str(ip) for ip in ipaddress.IPv4Network(network, strict=False).hosts()]

# Create ICMP Echo Request packets
packets = [IP(dst=ip)/ICMP() for ip in hosts]

# Send packets
ans, _ = sr(packets, timeout=2, verbose=0)

# Save the IP's
up_hosts = [recv.src for _, recv in ans]
print("Hosts that are UP:")
for ip in up_hosts:
    print(ip)

# TCP SYN scan each host that is UP(common ports 1–1024)
for ip in up_hosts:
    print(f"Scanning for open ports on {ip}")
    res, unans = sr(IP(dst=ip)/TCP(dport=(1,1024), flags='S'), timeout=1, verbose=0)

    for sent, received in res:
        if received.haslayer(TCP) and received[TCP].flags == 0x12:  # SYN-ACK
            print(f"    Port {sent[TCP].dport} open")
