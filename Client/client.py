import socket
import errno
import time
import re

class Client():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = self.create_socket()

    def create_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

    def get_file(self, filename):
        print('Connecting to server: ', self.host, self.port)
        print('\n------------------------------------------------\n')
        print('Sending filename:   ', filename)
        print('\n------------------------------------------------\n')

        self.send_filename(filename)

        print('Receiving data...')

        #makes the client eventually close when there is no data
        self.sock.setblocking(0)
        begin = time.time()
        timeout = 2
        expected = 0
        packets = []

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
                        packets.append((num, data))
                            
                    else:
                        print("Sending acknlowedgement ", (expected - 1))
                        self.send_filename(str(expected - 1))
                        
                    begin = time.time()
                    
                else: 
                    time.sleep(0.01)

            except socket.error as err:
                pass

        # sort packets, handle reordering
        sorted(packets, key=lambda x: x[0])

        packets = self.handle_duplicates(packets)

        # write file
        with open(filename, 'wb') as f:
            print('File opened')
            for p in packets:
                data = p[1]
                f.write(data)

        f.close()
        self.end_connection()

    def handle_duplicates(self, packets):
        i = 0
        while i < len(packets) - 1:
            if packets[i][0] == packets[i+1][0]:
                del packets[i+1]
            else:
                i += 1
        return packets

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

# get host
host = input('Which host would you like the client to connect to?\n')
while True:
    if re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', host):
        break
    else:
        host = input('Which host would you like the client to connect to?\n')

# get port
port = input('Which port would you like the client to connect to?\n')
while True:
    if re.match('[0-9]{4}', port):
        break
    else:
        port = input('Which port would you like the client to connect to?\n')

# get filename and connect
filename = input('What file would you like to get from the server?\n')
client = Client(host, int(port))
client.get_file(filename)