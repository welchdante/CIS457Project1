import socket
import os.path

class Server():
	def __init__(self, port):
		self.host = '127.0.0.1'
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket. SOCK_DGRAM)
		self.server = (self.host, self.port)
		self.sock.bind(self.server)

	def listen(self):
		print('Listening on: ' + self.host + ':' + str(self.port))
		print('\n------------------------------------------------\n')	
		while True:
			payload, client_host = self.sock.recvfrom(1024)
			filename = payload.decode()
			if self.file_exists(filename):
				f = open(filename,'rb')
				file_contents = f.read(1024)
				while file_contents:
					self.send_data_to_socket(file_contents, client_host)
					file_contents = f.read(1024)
				f.close()
			else:
				print('File does not exist.')

	def send_data_to_socket(self, payload, host):
		self.sock.sendto(payload, host)

	def file_exists(self, filename):
         return os.path.isfile(filename)

port = int(input('Which port would you like the server to listen on?\n'))
server = Server(port)
server.listen()

		