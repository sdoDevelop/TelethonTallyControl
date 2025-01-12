import socket

# Define the server (Arduino) IP and port
server_ip = "10.75.140.5"
server_port = 5005

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send a message to the Arduino
message = b'Hello Arduino'  # The content doesn't matter, any packet will trigger the strips
sock.sendto(message, (server_ip, server_port))

# Close the socket
sock.close()
