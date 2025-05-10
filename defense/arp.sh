arptables -F

ping -c1 10.1.0.1 > /dev/null

GATEWAY_IP="10.1.0.1"
GATEWAY_MAC=$(arp -n | awk -v ip=$GATEWAY_IP '$1 == ip {print $3}')

arptables -A INPUT --source-ip $GATEWAY_IP ! --source-mac $GATEWAY_MAC -j DROP

echo "ARP protection enabled on ws3 — only accepting from $GATEWAY_IP ($GATEWAY_MAC)"

