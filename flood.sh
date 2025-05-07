internet python3 attack/flood.py http 80 10.2.0.0/24 # Perform Attack
http netstat -nat | grep SYN_REC |awk '{print$6}' | sort | uniq -c | sort -r #Check for SYN_RECV Connections



