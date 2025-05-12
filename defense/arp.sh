
if [ -z "$1" ]; then
    echo "Usage: $0 <GATEWAY_IP>"
    exit 1
fi

GATEWAY_IP="$1"
arptables -F


ping -c1 $GATEWAY_IP > /dev/null

GATEWAY_MAC=$(arp -n | awk -v ip=$GATEWAY_IP '$1 == ip {print $3}')

arptables -A INPUT --source-ip $GATEWAY_IP ! --source-mac $GATEWAY_MAC -j DROP

echo "ARP protection enabled on ws3 — only accepting from $GATEWAY_IP ($GATEWAY_MAC)"

