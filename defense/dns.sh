dns nft add table ip filter
dns nft add chain ip filter input { type filter hook input priority 0 \; }

dns nft add rule ip filter input udp dport 53 limit rate 10/second accept
dns nft add rule ip filter input udp dport 53 drop


