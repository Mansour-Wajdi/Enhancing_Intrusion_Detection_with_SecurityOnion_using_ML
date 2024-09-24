import paramiko
import scp
import pandas as pd


def create_requests(pcap_info):
    """Create a list of pcap requests based on given info."""
    requests = [
        f'\"(host {row["source.ip"]}) and (port {row["source.port"]}) and (host {row["destination.ip"]}) and (port {row["destination.port"]})\"'
        for _, row in pcap_info.iterrows()
    ]
    pcap_info['request'] = requests
    return pcap_info

def request_pcap_file(host, username, password, row,logger):
    """Send a request for a pcap file to the remote machine."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, username=username, password=password)
        command = f"sudo so-pcap-export {row['request']} {row['log.id.uid']}"
        _, stdout, _ = ssh.exec_command(command)
        logger.info(stdout.read().decode())
        logger.debug(command)
    except (paramiko.AuthenticationException, paramiko.SSHException) as error:
        logger.error("Error: %s", str(error))
    finally:
        ssh.close()

def retrieve_pcap_file(host, username, password, remote_path,logger, local_filename):
    """Retrieve a pcap file from a remote machine."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=username, password=password)
        with scp.SCPClient(ssh.get_transport()) as scp_client:
            scp_client.get(remote_path, local_filename)
            logger.info("PCAP file retrieved")
    except (paramiko.AuthenticationException, paramiko.SSHException) as error:
        logger.error("Error: %s", str(error))
    finally:
        ssh.close()

def process_pcap_requests(remote_host, remote_username, remote_password, csv_path, logger):
    """Function to process pcap files."""

    # Create pcap requests
    pcap_info = pd.read_csv(csv_path)
    pcap_info = create_requests(pcap_info)
    # Send requests and retrieve pcap files
    for _, row in pcap_info.iterrows():
        request_pcap_file(remote_host, remote_username, remote_password, row, logger)
        log_id = row['log.id.uid']
        local_filename = f"./pcap_files/filtred_pcap_{log_id}.pcap"
        remote_pcap_path = f"/nsm/pcapout/{log_id}.pcap"
        retrieve_pcap_file(remote_host, remote_username, remote_password, remote_pcap_path,logger, local_filename)

if __name__ == "__main__":
    process_pcap_requests()
