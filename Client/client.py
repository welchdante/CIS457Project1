import socket

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
		with open("test.jpg", 'wb') as f:
		    print('File opened')
		    print('Receiving data...')
		    while True:
		        data = self.sock.recv(1)
		        if not data:
		            break
		        f.write(data)
		f.close()
		self.end_connection()

	def send_filename(self, filename):
		return self.sock.sendto(filename.encode(), (self.host, self.port))

	def end_connection(self):
		self.sock.close()

host = input('Which host would you like the client to connect to?\n')
port = int(input('Which port would you like the client to connect to?\n'))
filename = input('What file would you like to get from the server?\n')
client = Client(host, port)
client.get_file(filename)