#!/bin/bash

# Get your own IP and MAC
MY_IP="10.1.0.1"
MY_MAC="1e:4d:df:0d:09:14"
echo "[*] My IP: $MY_IP"
echo "[*] My MAC: $MY_MAC"

nft list table inet filter > /dev/null 2>&1 || nft add table inet filter
nft list chain inet filter forward > /dev/null 2>&1 || \
  nft add chain inet filter forward { type filter hook forward priority 0\; policy accept\; }
# Send to r1 a rule to drop forwarded traffic with your MAC unless it comes from your IP
nft insert rule inet filter forward ether saddr != $MY_MAC ip saddr $MY_IP  drop

echo "[✓] Rule added on r1: block anyone cloning my MAC."

