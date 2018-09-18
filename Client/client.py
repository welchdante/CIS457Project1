import socket

class Client():
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.sock = self.create_socket()

	def create_socket(self):
		return socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

	def get_file(self, message):
		print('Connecting to server: ', self.host, self.port)
		print('\n------------------------------------------------\n')
		print('Sending message:   ', message)
		print('\n------------------------------------------------\n')
		
		self.send_message(message)
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

	def send_message(self, message):
		return self.sock.sendto(message.encode(), (self.host, self.port))

	def end_connection(self):
		self.sock.close()

host = input('Which host would you like the client to connect to?\n')
port = int(input('Which port would you like the client to connect to?\n'))
message = input('What message would you like to send to the server?\n')
client = Client(host, port)
client.get_file(message)