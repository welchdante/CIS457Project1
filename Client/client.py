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
        # print('\n------------------------------------------------\n')
        print('\nSending filename:   ', filename)
        # print('\n------------------------------------------------\n')

        self.send_filename(filename)

        # Need to add check that file exists?
        with open(filename, 'wb') as f:
            print('File opened')
            print('Receiving data...')

            #makes the client eventually close when there is no data
            self.sock.setblocking(0)
            begin = time.time()
            timeout = 2

            while True:
                # wait if you have no data
                if time.time() - begin > timeout:
                    break
                #recieve something
                try:
                    data = self.sock.recv(1024)
                    if data: 
                        f.write(data)
                        begin = time.time()
                    else: 
                        time.sleep(0.01)

                except socket.error as err:
                    pass

        # Quick fix for writing file that doesn't exist
        if os.stat(filename).st_size == 0:
            os.remove(filename)

        self.end_connection()

    def send_filename(self, filename):
        return self.sock.sendto(filename.encode(), (self.host, self.port))

    def end_connection(self):
        self.sock.close()

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