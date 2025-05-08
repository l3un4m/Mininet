nft add rule ip filter forward tcp flags syn limit rate 20/second accept
nft add rule ip filter forward tcp flags syn drop
