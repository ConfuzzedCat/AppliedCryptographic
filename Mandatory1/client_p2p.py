#!/usr/bin/env python3

import socket
import threading
import os
import sys
from OTP import encrypt, decrypt


# Load encryption key from file
def load_key():
    try:
        with open("key.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print("Error: key.txt file not found.")
        sys.exit(1)


# Function to handle receiving messages (server)
def listen(ip, port, key):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)
    print(f"Listening on {ip}:{port}...")

    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr} established.")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        decrypted_message = decrypt(data.decode(), key)
        print(f"Received (decrypted): {decrypted_message}")

    client_socket.close()


# Function to handle sending messages (client)
def send(ip, port, key):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))

    while True:
        message = input("Enter message to send: ")
        if message.lower() == 'exit':
            break
        encrypted_message = encrypt(message, key)
        client_socket.send(encrypted_message.encode())
        print(f"Sent (encrypted): {encrypted_message}")

    client_socket.close()


# Main function to initialize threads
def main():
    # Get the listening IP and port
    ip_a = input("Enter this instance's listening IP (e.g. 127.0.0.1): ").strip()
    port = int(input("Enter the port to listen on: ").strip())

    # Load the encryption key
    key = load_key()

    # Create the server and client threads
    server_thread = threading.Thread(target=listen, args=(ip_a, port, key))
    server_thread.start()
    ip_b = input("Enter the other instance's listening IP (e.g. 127.0.0.2): ").strip()
    client_thread = threading.Thread(target=send, args=(ip_b, port, key))

    # Start the threads
    client_thread.start()

    # Wait for threads to complete
    server_thread.join()
    client_thread.join()


if __name__ == "__main__":
    main()