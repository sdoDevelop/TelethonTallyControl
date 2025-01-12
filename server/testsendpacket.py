import socket

tallyClientIP = "10.74.140.5"
tallyClientPort = 5005

def send_udp_packet(ip, port, message):
    """Send a UDP packet to the specified IP and port."""
    try:
        # Create a UDP socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Encode the message to bytes
        message_bytes = message.encode('utf-8')

        # Send the packet
        udp_socket.sendto(message_bytes, (ip, port))

        print(f"Packet sent to {ip}:{port} with message: {message}")
    except Exception as e:
        print(f"Error sending UDP packet: {e}")
    finally:
        # Close the socket
        udp_socket.close()

# Configuration
ip_address = "10.75.140.5"
port = 5005
message = "Hello, UDP!"  # Replace with your desired message

# Send the packet
send_udp_packet(ip_address, port, message)
