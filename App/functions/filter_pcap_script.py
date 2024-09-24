import pyshark
import dpkt
import sys

def filter_pcap(input_path, output_path, packet_filter):
    cap = pyshark.FileCapture(input_path, display_filter=packet_filter, use_json=True, include_raw=True)
    packets = [pkt for pkt in cap]

    with open(output_path, 'wb') as f:
        writer = dpkt.pcap.Writer(f)
        for pkt in packets:
            raw_packet = pkt.get_raw_packet()
            timestamp = float(pkt.sniff_timestamp)
            writer.writepkt(raw_packet, timestamp)

    print(f"Filtered pcap saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python filter_pcap_script.py <input_path> <output_path> <packet_filter>")
        sys.exit(1)

    input_pcap_path = sys.argv[1]
    output_pcap_path = sys.argv[2]
    packet_filter_condition = sys.argv[3]

    filter_pcap(input_pcap_path, output_pcap_path, packet_filter_condition)
