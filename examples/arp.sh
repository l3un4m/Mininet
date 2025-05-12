ws3 arp -n                                  #Check VIctim's Arp Table
ws2 python3 attack/arp.py 10.1.0.3 10.1.0.1 #Perform Attack
ws3 arp -n                                  #Check VIctim's Arp Table
