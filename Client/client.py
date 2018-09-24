#!/usr/bin/python3

import socket
import errno
import time
import sys
import os

from IPy import IP

class Client():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = self.create_socket()

    def create_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

    def get_file(self, filename):
        print('Connecting to server: ', self.host, self.port)
        print('\nSending filename:   ', filename)

        self.send_filename(filename)
        with open(filename, 'wb') as f:
            print('Checking for response...')

            #makes the client eventually close when there is no data
            self.sock.setblocking(0)
            begin = time.time()
            timeout = 2
            expected = 0

            while True:
                # wait if you have no data
                if time.time() - begin > timeout:
                    break
                #recieve something
                try:
                    packet = self.sock.recv(1024)
                    if packet: 
                        num, data = self.extract(packet)
                        print("Got packet ", num)

                        # Send acknlowedgement to the sender
                        if num == expected:
                            print("Sending acknlowedgement ", expected)
                            self.send_filename(str(expected))
                            expected += 1
                            f.write(data)
                        else:
                            print("Sending acknlowedgement ", (expected - 1))
                            self.send_filename(str(expected - 1))
                        
                        begin = time.time()
                    
                    else: 
                        time.sleep(0.01)

                except socket.error as err:
                    pass

        # Quick fix for writing file that doesn't exist
        if os.stat(filename).st_size == 0:
            print("File doesn't exist on server.")
            os.remove(filename)
        else:
            print("Recieved data.")

        self.end_connection()

    def send_filename(self, filename):
        return self.sock.sendto(filename.encode(), (self.host, self.port))

    def end_connection(self):
        self.sock.close()

    def make_packet(self, acknum, data=b''):
        ackbytes = acknum.to_bytes(4, byteorder='little', signed=True)
        return ackbytes + data

    def extract(self, packet):
        num = int.from_bytes(packet[0:4], byteorder = 'little', signed = True)
        return num, packet[4:]

if __name__ == '__main__':

    host = input('Which host would you like the client to connect to?\n')
    
    try: # IP address error checking.
        IP(host)
    except Exception as e:
        print(host, "is not a valid IP address.\nShutting Down.")
        sys.exit()

    port = input('Which port would you like the client to connect to?\n')

    # Port number error checking.
    if not port.isdigit() and not 1 <= int(port) <= 65535:
        print(port, 'is not a valid port number.\nShutting Down.')
        sys.exit()

    filename = input('What file would you like to get from the server?\n')
    client = Client(host, int(port))
    client.get_file(filename)

