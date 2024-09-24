import paramiko
import socket

def test_ssh_connection(host, username, password, logger):
    """
    Connect via SSH and retrieve a pcap file from the remote server.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=username, password=password)
        logger.info("Connected via SSH")
    except (paramiko.AuthenticationException, paramiko.SSHException) as error:
        logger.error(f"Error: {str(error)}")
    except (socket.timeout, socket.error) as e:
        logger.error(f"Network error while trying to connect to host {host}: \n      {str(e)}")
    finally:
        ssh.close()
