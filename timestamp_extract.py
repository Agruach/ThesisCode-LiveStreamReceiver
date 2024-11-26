import subprocess
import datetime


# Start the FFmpeg process to read SRT packets
process = subprocess.Popen(
    [
        'ffmpeg',
        '-i', r'srt://IP:PORT?mode=listener',  # Replace with correct SRT stream URL
        '-f', 'mpegts',
        '-'
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

old_timestamp = 0

# Capture the first packet and correlate system time to SRT timestamp
first_packet = process.stdout.read(188)
first_udp_payload = first_packet[32:]
first_ts = int.from_bytes(first_udp_payload[8:12])
established_time = datetime.now()

while True:
    # Read the full packet (ensure size is sufficient for parsing)
    packet = process.stdout.read(188)  # Fix packet size assumed
    if len(packet) < 40:  # Minimal size for valid UDP + SRT header
        print("Incomplete packet")
        continue
    
    # Skip the null.family (4 bytes), IP header (20 bytes), and UDP header (8 bytes)
    udp_payload = packet[32:]  # 4 (null.family) + 20 (IP) + 8 (UDP) = 32

    # Extract the timestamp (bytes 40-43 in the UDP payload)
    timestamp = int.from_bytes(udp_payload[8:12])  # 8:12 in the UDP payload gives the timestamp

    print("Timestamp:", timestamp)