ws3 ping r1 -c 1
ws3 arp -n
ws2 python3 attack/arp.py 10.1.0.3 10.1.0.1
ws3 arp -n
