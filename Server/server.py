import socket
import os.path
import time

class Server():
    def __init__(self, port):
        self.host = '127.0.0.1'
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket. SOCK_DGRAM)
        self.server = (self.host, self.port)
        self.sock.bind(self.server)
        self.window_size = 5
        # timer properties
        self.start_time = -1
        self.duration = 0.5

    def listen(self):
        print('Listening on: ' + self.host + ':' + str(self.port))
        print('\n------------------------------------------------\n')   
        while True:
            # Get data 
            payload, client_host = self.sock.recvfrom(1024)
            filename = payload.decode()

            # Open file
            if self.file_exists(filename):
                f = open(filename,'rb')
            else:
                print('File does not exist.')

            # Add all packets and number them
            packets = []
            num = 0
            file_contents = f.read(1020)
            while file_contents:
                packets.append(self.make_packet(num, file_contents))
                num += 1
                file_contents = f.read(1020)
            f.close()

            num_packets = len(packets)
            print('Number packets: ', num_packets)
            next_frame = 0
            base = 0
            window = self.set_window(num_packets, base)

            # Send the packet
            while base < num_packets:
                # Send all packets within the window
                while next_frame < base + window and next_frame < num_packets:
                    print('Sending packet ', next_frame)
                    self.send_data_to_socket(packets[next_frame], client_host)
                    next_frame += 1
                # Wait till time is up or acknowledgement
                self.start_timer()
                while self.timer_running() and not self.timer_timeout():
                    data = self.sock.recvfrom(1024)
                    if data:
                        ack = data[0].decode()
                        print('Got acknowledgement ', ack)
                        if int(ack) >= base:
                            base = int(ack) + 1
                            self.stop_timer()

                if self.timer_timeout():
                    self.stop_timer()
                    next_frame = base
                else:
                    print('Shifting window.')
                    window_size = self.set_window(num_packets, base)
            #self.sock.recvfrom(1024)
            time.sleep(1)
            print('Listening on: ' + self.host + ':' + str(self.port))
            print('\n------------------------------------------------\n')   

    def send_data_to_socket(self, payload, host):
        self.sock.sendto(payload, host)

    def file_exists(self, filename):
        return os.path.isfile(filename)

    def set_window(self, num_packets, base):
        return min(self.window_size, num_packets - base)

    def make_packet(self, acknum, data=b''):
        ackbytes = acknum.to_bytes(4, byteorder='little', signed=True)
        return ackbytes + data

    def start_timer(self):
        if self.start_time == -1:
            self.start_time = time.time()

    def stop_timer(self):
        if self.start_time != -1:
            self.start_time = -1

    def timer_running(self):
        return self.start_time != -1

    def timer_timeout(self):
        if not self.timer_running():
            return False
        else:
            return time.time() - self.start_time >= self.duration

port = int(input('Which port would you like the server to listen on?\n'))
server = Server(port)
server.listen()

        