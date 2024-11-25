from scapy.all import IP, TCP, send, sr1
import random

def fuzz_ssh_handshake(ip, port):
    # Define malformed packets for fuzzing
    packets = [
        IP(dst=ip) / TCP(dport=port, sport=random.randint(1024, 65535)) / b"\x00" * 100,  # Overly long data
        IP(dst=ip) / TCP(dport=port, sport=random.randint(1024, 65535)) / b"\xff" * 50,   # Invalid bytes
        IP(dst=ip) / TCP(dport=port, sport=random.randint(1024, 65535)) / b"SSH-2.0-FAKE-PROTOCOL",  # Invalid SSH banner
    ]

    for i, pkt in enumerate(packets):
        print(f"\nSending packet {i + 1}")
        try:
            # Send the packet and wait for a response
            response = sr1(pkt, timeout=2, verbose=0)
            if response:
                print(f"Received response for packet {i + 1}:")
                print(response.show())  # Display detailed response packet information
            else:
                print(f"No response for packet {i + 1}")
        except Exception as e:
            print(f"Error while sending packet {i + 1}: {e}")


if __name__ == "__main__":
    target_ip = "45.33.32.170"  # Replace with the target IP
    target_port = 22           # SSH port
    fuzz_ssh_handshake(target_ip, target_port)
