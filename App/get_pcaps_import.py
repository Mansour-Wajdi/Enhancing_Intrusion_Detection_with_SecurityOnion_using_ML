import paramiko
import scp
import pandas as pd
from functions.filter_pcap_script import filter_pcap
import logging
    
def retrieve_pcap_file(host, username, password, remote_path, logger, local_filename='temp.pcap'):
    """
    Connect via SSH and retrieve a pcap file from the remote server.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=username, password=password)
        #logger.info("Connected via SSH")
        with scp.SCPClient(ssh.get_transport()) as scp_client:
            scp_client.get(remote_path, local_filename)
            logger.info("PCAP file retrieved")
            logger.info(f"PCAP file saved to {local_filename}")
            return local_filename
    except (paramiko.AuthenticationException, paramiko.SSHException) as error:
        logger.error(f"Error: {str(error)}")
    finally:
        ssh.close()


def download_pcaps_from_info(pcap_info, remote_host, remote_username, remote_password, logger):
    """
    Download pcap files based on information in the dataframe.
    """
    for _, row in pcap_info.iterrows():
        import_id = row['import.id']
        log_id = row['log.id.uid']
        local_filename = f"./pcap_files/full_pcap_{log_id}.pcap"
        remote_pcap_path = f"/nsm/import/{import_id}/pcap/data.pcap"
        retrieve_pcap_file(remote_host, remote_username, remote_password, remote_pcap_path, logger,  local_filename)



def filter_pcaps(flow_info,logger):
    """
    Filter pcap files based on the information provided in the dataframe.
    """
    for _, row in flow_info.iterrows():
        connection_srcip, connection_dstip, src_port, dst_port, proto = row['source.ip'], row['destination.ip'], row['source.port'], row['destination.port'], row['network.transport']
        log_id = row["log.id.uid"]
        proto = proto.lower()
        filter_condition = (
            f"(ip.src == {connection_srcip} && {proto}.srcport == {src_port} && "
            f"ip.dst == {connection_dstip} && {proto}.dstport == {dst_port}) || "
            f"(ip.src == {connection_dstip} && {proto}.srcport == {dst_port} && "
            f"ip.dst == {connection_srcip} && {proto}.dstport == {src_port})"
        )
        input_path = f'./pcap_files/full_pcap_{log_id}.pcap'
        output_path = f'./pcap_files/filtred_pcap_{log_id}.pcap'
        filter_pcap(input_path, output_path, filter_condition)
        logger.info("PCAP file filtred succefuly")
        logger.info(f"filtred PCAP file saved to {output_path}")




def process_pcap_requests(remote_host,remote_username,remote_password,csv_path,logger):
    
    # Load pcap info and start downloading the pcaps
    pcap_info = pd.read_csv('./csv_files/flow_info.csv')
    download_pcaps_from_info(pcap_info, remote_host, remote_username, remote_password, logger)

    # Load flow info and start filtering the pcaps
    flow_info = pd.read_csv(csv_path)
    filter_pcaps(flow_info,logger)


if __name__ == "__main__":
    remote_host = "192.168.43.10"
    remote_username = "wajdi"
    remote_password = "0000"
    csv_path='./csv_files/flow_info.csv'
    logger = logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    process_pcap_requests(remote_host,remote_username,remote_password,csv_path, logger)
