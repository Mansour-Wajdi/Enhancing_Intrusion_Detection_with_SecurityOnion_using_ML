import paramiko
import scp
import dpkt
import io
import pandas as pd
from scapy.all import *
from datetime import datetime
from datetime import timedelta
import re
from scapy.all import *
from datetime import datetime
import re

# extract/calculate the desired values 
### extarct and calculate them from pcap file :

#### notes : 
#Calculating sloss and dloss typically involves analyzing sequences of packets to identify retransmissions or dropped packets. This can get quite complex. In the provided code, I've added placeholders for these values.

#The code assumes that all packets have an IP layer and may have a TCP layer. If this is not the case for your pcap file, you might need to add additional checks.

#Services have been identified only based on the protocol. Advanced identification based on port numbers and packet patterns might provide more accurate results.





def calculate_values(log_id,pcap_file, connection_srcip, connection_dstip, connection_src_port, connection_dst_port):
    packets = rdpcap(pcap_file)
    #initializations 
    states = []
    protocols = set()
    sbytes = 0
    dbytes = 0
    timestamps = []
    Spkts = 0
    Dpkts = 0
    services = ["http", "ftp", "smtp", "ssh", "dns", "ftp-data", "irc"]
    service = "-"
    dtcpb = 0
    spacket_sizes = []
    dpacket_sizes = []
    trans_depth = 0
    res_bdy_len = 0
    previous_stime = None
    sjits = []
    djits = []
    previous_dtime = None
    djits = []
    syn_time = None
    syn_ack_time = None
    ack_time = None
    recent_packets = deque(maxlen=100)
    ct_flw_http_mthd = is_ftp_login = ct_ftp_cmd = ct_srv_src = ct_srv_dst = ct_dst_ltm = ct_src_ltm = ct_src_dport_ltm = ct_dst_sport_ltm = ct_dst_src_ltm = 0
    # Queue to store timestamps of all packets
    all_timestamps = deque()

    
    seq_numbers_src = set()
    seq_numbers_dst = set()
    retransmissions_src = 0
    retransmissions_dst = 0

    
    
    for packet in packets:
        # Extracting state
        state = packet.get('state', b'-').decode() if 'state' in packet else '-'
        states.append(state)

        # Extracting protocol
        if packet.haslayer(IP) and packet['IP'].src == connection_srcip and packet['IP'].dst == connection_dstip:
            proto_number = packet['IP'].proto
            protocol_name = packet['IP'].get_field('proto').i2s[proto_number]
            protocols.add(protocol_name)
            
            # Extracting service
            if packet.haslayer(TCP) and protocol_name in services:
                service = protocol_name

            # Extracting bytes and packets count
            if packet['IP'].src == connection_srcip:
                sbytes += len(packet)
                Spkts += 1
                timestamps.append(packet.time)
            if packet['IP'].dst == connection_srcip:
                dbytes += len(packet)
                Dpkts += 1
        # Extracting packet sizes
        if packet['IP'].src == connection_srcip:
            spacket_sizes.append(len(packet))
        if packet['IP'].dst == connection_srcip:
            dpacket_sizes.append(len(packet))

        # For calculating jitter
        current_time = packet.time
        if previous_stime:
            if packet['IP'].src == connection_srcip:
                sjits.append(current_time - previous_stime)
            else:
                djits.append(current_time - previous_stime)
        previous_stime = current_time

        # HTTP depth and body length
        if packet.haslayer(Raw):
            raw_data = packet[Raw].load.decode(errors='ignore') # Decoding to make it a string, and ignoring any decoding errors
            if "HTTP" in raw_data:  # A simple check to see if it might be HTTP data
                trans_depth += 1
                # Extracting Content-Length
                content_length_headers = re.findall(r"Content-Length: (\d+)", raw_data)
                for header in content_length_headers:
                    res_bdy_len += int(header)
        
        # Destination TCP sequence number
        if packet.haslayer(TCP) and packet['IP'].dst == connection_dstip:
            dtcpb = packet['TCP'].seq

            
        # For calculating destination jitter
        current_time = packet.time
        if packet['IP'].dst == connection_dstip:
            if previous_dtime:
                djits.append(current_time - previous_dtime)
            previous_dtime = current_time

        # For calculating TCP round trip time
        if packet.haslayer(TCP):
            if "S" in packet['TCP'].flags and not "A" in packet['TCP'].flags:  # SYN flag
                syn_time = packet.time
            elif "S" in packet['TCP'].flags and "A" in packet['TCP'].flags:  # SYN-ACK flag
                syn_ack_time = packet.time
            elif not "S" in packet['TCP'].flags and "A" in packet['TCP'].flags:  # ACK flag
                ack_time = packet.time

        # HTTP methods count
        if packet.haslayer(Raw) and ("GET" in str(packet[Raw]) or "POST" in str(packet[Raw])):
            ct_flw_http_mthd += 1

        # FTP check (basic)
        if packet.haslayer(Raw) and ("USER" in str(packet[Raw]) or "PASS" in str(packet[Raw])):
            is_ftp_login = 1
        if packet.haslayer(Raw) and "FTP" in str(packet[Raw]):
            ct_ftp_cmd += 1

            
            
        # Note: Calculating sloss and dloss might require advanced packet analysis and is not done here.
        # instead we will only calculate the number of retransmitted packets.
        if not 'TCP' in packet:
            continue
        src_ip = packet["IP"].src
        dst_ip = packet["IP"].dst
        seq_number = int(packet['TCP'].seq)
        
        # Check for retransmission in source IP
        if src_ip == connection_srcip:
            if seq_number in seq_numbers_src:
                retransmissions_src += 1
            else:
                seq_numbers_src.add(seq_number)
        
        # Check for retransmission in destination IP
        if src_ip == connection_dstip:
            if seq_number in seq_numbers_dst:
                retransmissions_dst += 1
            else:
                seq_numbers_dst.add(seq_number)

            

        recent_packets.append(packet)

        # Check if the oldest packet (if any) from the recent_packets needs to be removed from any counter
        if len(recent_packets) == 100:
            oldest_packet = recent_packets[0]

            if oldest_packet['IP'].src == connection_srcip and 'Sload' in oldest_packet:
                ct_srv_src -= 1
            if oldest_packet['IP'].dst == connection_dstip and 'Sload' in oldest_packet:
                ct_srv_dst -= 1
            if oldest_packet['IP'].dst == connection_dstip:
                ct_dst_ltm -= 1
            if oldest_packet['IP'].src == connection_srcip:
                ct_src_ltm -= 1
            if oldest_packet.haslayer(TCP) and oldest_packet['IP'].src == connection_srcip and oldest_packet['TCP'].dport == connection_dst_port:
                ct_src_dport_ltm -= 1
            if  oldest_packet.haslayer(TCP) and oldest_packet['IP'].dst == connection_dstip and oldest_packet['TCP'].sport == connection_src_port:
                ct_dst_sport_ltm -= 1
            if oldest_packet['IP'].src == connection_srcip and oldest_packet['IP'].dst == connection_dstip:
                ct_dst_src_ltm -= 1

        # Count the new packet for the counters if criteria are met
        if packet['IP'].src == connection_srcip and 'Sload' in packet:
            ct_srv_src += 1
        if packet['IP'].dst == connection_dstip and 'Sload' in packet:
            ct_srv_dst += 1
        if packet['IP'].dst == connection_dstip:
            ct_dst_ltm += 1
        if packet['IP'].src == connection_srcip:
            ct_src_ltm += 1
        if packet.haslayer(TCP) and packet['IP'].src == connection_srcip and packet['TCP'].dport == connection_dst_port:
            ct_src_dport_ltm += 1
        if packet.haslayer(TCP) and packet['IP'].dst == connection_dstip and packet['TCP'].sport == connection_src_port:
            ct_dst_sport_ltm += 1
        if packet['IP'].src == connection_srcip and packet['IP'].dst == connection_dstip:
            ct_dst_src_ltm += 1

            
            
        # If the packet is from source to destination
        if packet['IP'].src == connection_srcip and packet['IP'].dst == connection_dstip:
            current_timestamp = packet.time
            all_timestamps.append(current_timestamp)
            
            
#################
####### rate
#################
    # consider only packets that fall within the last two seconds of the connection
    last_timestamp = all_timestamps[-1] if all_timestamps else None
    packets_in_last_2_seconds = [ts for ts in all_timestamps if last_timestamp - ts <= 2]

    # Calculate the rate based on the packets in the last 2 seconds
    rate = len(packets_in_last_2_seconds) / 2.0  # Since the window is 2 seconds
#################
                
    
    
    
    duration = datetime.fromtimestamp(float(max(timestamps))) - datetime.fromtimestamp(float(min(timestamps))) if timestamps else timedelta(seconds=0)
    Sload = (sbytes * 8) / duration.total_seconds() if duration else 0
    Dload = (dbytes * 8) / duration.total_seconds() if duration else 0
    swin = packet['TCP'].window if packet.haslayer(TCP) and packet['IP'].src == connection_srcip else 0
    dwin = packet['TCP'].window if packet.haslayer(TCP) and packet['IP'].dst == connection_srcip else 0
    stcpb = packet['TCP'].seq if packet.haslayer(TCP) and packet['IP'].src == connection_srcip else 0
    sttl = packet['IP'].ttl if packet['IP'].src == connection_srcip else 0
    dttl = packet['IP'].ttl if packet['IP'].dst == connection_srcip else 0
    smean = sum(spacket_sizes) / len(spacket_sizes) if spacket_sizes else 0
    dmean = sum(dpacket_sizes) / len(dpacket_sizes) if dpacket_sizes else 0
    sjit = max(sjits) - min(sjits) if sjits else 0
    djit = max(djits) - min(djits) if djits else 0

    synack = syn_ack_time - syn_time if syn_time and syn_ack_time else 0
    ackdat = ack_time - syn_ack_time if syn_ack_time and ack_time else 0
    tcprtt = synack + ackdat

    dintpkt = sum(djits) / len(djits) if djits else 0
    is_sm_ips_ports = 1 if connection_srcip == connection_dstip and connection_src_port == connection_dst_port else 0
    
    ############################################
    ############### ct_state_ttl ###############
    ############################################
    #ct_state_ttl = calculate_ct_state_ttl(list(set(states))[0], sttl, dttl)
    
    
    
    
    results = {
        'id': log_id,
        'dur': duration.total_seconds(),
        'proto': list(protocols)[0] if protocols else "Unknown",
        'service': service,
        'state': list(set(states))[0],
        'spkts': Spkts,
        'dpkts': Dpkts,
        'sbytes': sbytes,
        'dbytes': dbytes,
        'rate': rate,
        'sttl': sttl,
        'dttl': dttl,
        'sload': Sload,
        'dload': Dload,
        'sloss': int(retransmissions_src),
        'dloss': int(retransmissions_dst),
        'sinpkt': sjit / len(sjits) if sjits else 0,
        'dinpkt': dintpkt,
        'sjit': sjit,
        'djit': djit,
        'swin': swin,
        'stcpb': stcpb,
        'dtcpb': dtcpb,
        'dwin': dwin,
        'tcprtt': tcprtt,
        'synack': synack,
        'ackdat': ackdat,
        'smean': smean,
        'dmean': dmean,
        'trans_depth': trans_depth,
        'response_body_len': res_bdy_len,
        'ct_srv_src': ct_srv_src,
        'ct_state_ttl': 3,  # Placeholder
        'ct_dst_ltm': ct_dst_ltm,
        'ct_src_dport_ltm': ct_src_dport_ltm,
        'ct_dst_sport_ltm': ct_dst_sport_ltm,
        'ct_dst_src_ltm': ct_dst_src_ltm,
        'is_ftp_login': is_ftp_login,
        'ct_ftp_cmd': ct_ftp_cmd,
        'ct_flw_http_mthd': ct_flw_http_mthd,
        'ct_src_ltm': ct_src_ltm,
        'ct_srv_dst': ct_srv_dst,
        'is_sm_ips_ports': is_sm_ips_ports
        }
    
    return results






def analyze_pcap_files(dir_path, file_path, output_file='./csv_files/featrues_df.csv'):
    featrues_df = pd.DataFrame(columns=['id', 'dur', 'proto', 'service', 'state', 'spkts', 'dpkts', 'sbytes',
                 'dbytes', 'rate', 'sttl', 'dttl', 'sload', 'dload', 'sloss', 'dloss',
                 'sinpkt', 'dinpkt', 'sjit', 'djit', 'swin', 'stcpb', 'dtcpb', 'dwin',
                 'tcprtt', 'synack', 'ackdat', 'smean', 'dmean', 'trans_depth',
                 'response_body_len', 'ct_srv_src', 'ct_state_ttl', 'ct_dst_ltm',
                 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm',
                 'is_ftp_login', 'ct_ftp_cmd', 'ct_flw_http_mthd', 'ct_src_ltm',
                 'ct_srv_dst', 'is_sm_ips_ports'])
    flow_info = pd.read_csv(file_path)
    for index, row in flow_info.iterrows():
        log_id=str(row["log.id.uid"])    
        connection_srcip,connection_dstip,src_port,dst_port, proto = row['source.ip'],row['destination.ip'],row['source.port'],row['destination.port'],row['network.transport']
        pcap_file = f'{dir_path}/filtred_pcap_{log_id}.pcap'
        results = calculate_values(log_id,pcap_file, connection_srcip, connection_dstip, src_port, dst_port)
        featrues_df = featrues_df._append(results, ignore_index=True)
    featrues_df.to_csv(output_file, index=False)




if __name__ == "__main__":
    featrues_df = pd.DataFrame(columns=['id', 'dur', 'proto', 'service', 'state', 'spkts', 'dpkts', 'sbytes',
                    'dbytes', 'rate', 'sttl', 'dttl', 'sload', 'dload', 'sloss', 'dloss',
                    'sinpkt', 'dinpkt', 'sjit', 'djit', 'swin', 'stcpb', 'dtcpb', 'dwin',
                    'tcprtt', 'synack', 'ackdat', 'smean', 'dmean', 'trans_depth',
                    'response_body_len', 'ct_srv_src', 'ct_state_ttl', 'ct_dst_ltm',
                    'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm',
                    'is_ftp_login', 'ct_ftp_cmd', 'ct_flw_http_mthd', 'ct_src_ltm',
                    'ct_srv_dst', 'is_sm_ips_ports'])

    dir_path = './pcap_files'
    file_path = './csv_files/flow_info.csv'
    flow_info = pd.read_csv(file_path)
    for index, row in flow_info.iterrows():
        log_id=str(row["log.id.uid"])    
        connection_srcip,connection_dstip,src_port,dst_port, proto = row['source.ip'],row['destination.ip'],row['source.port'],row['destination.port'],row['network.transport']
        pcap_file = f'{dir_path}/filtred_pcap_{log_id}.pcap'
        results = calculate_values(log_id,pcap_file, connection_srcip, connection_dstip, src_port, dst_port)
        featrues_df = featrues_df._append(results, ignore_index=True)
    
    featrues_df.to_csv('featrues_df.csv', index=False)

