nft add table netdev filter
nft add chain netdev filter arp_filter { type filter hook ingress device eth0 priority 0 \; }

nft add rule netdev filter arp_filter arp op request accept
nft add rule netdev filter arp_filter arp op reply accept

nft add rule netdev filter arp_filter drop

