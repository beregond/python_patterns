import socket, threading

PORT = 1245

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', PORT))
s.listen(4)
clients = []
lock = threading.Lock()

class Server(threading.Thread):
	def __init__(self, (socket,address)):
		threading.Thread.__init__(self)
		self.socket = socket
		self.address = address

	def run(self):
		with lock:
			clients.append(self)
			print '%s:%s connected.' % self.address

		while True:
			data = self.socket.recv(1024)
			if not data:
				break
			print self.socket
			for c in clients:
				if c != self:
					c.socket.send(data)
		self.socket.close()
		with lock:
			print '%s:%s disconnected.' % self.address
			clients.remove(self)

while True:
	Server(s.accept()).start()
