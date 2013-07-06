import thread, threading, time, random, hashlib

"Solution for classic readers-writers problem."

def generateData():
	data = hashlib.sha1()
	data.update(str(random.random()))
	return data.hexdigest()

class Library():

	def __init__(self):
		self.event = threading.Event()
		self.event.set()
		self.c = threading.BoundedSemaphore()
		self.w = threading.BoundedSemaphore()
		self.r = threading.BoundedSemaphore()
		self.clients = 0
		self.resource = generateData()

	def read(self, name):
		with self.w:
			self.event.clear()
			with self.c:
				self.clients += 1
		with self.r:
			print "Reader %s is reading resource: %s" % (name, self.resource)
		with self.c:
			self.clients -= 1
			if self.clients == 0:
				self.event.set()

	def write(self, name):
		with self.w:
			self.event.wait()
			self.resource = generateData()
			print "Writer %s changed data to %s" % (name, self.resource)
			self.event.clear()

def reader(name, library):
	while True:
		delay = random.randrange(1, 5)
		time.sleep(delay)
		library.read(name)

def writer(name, library):
	while True:
		delay = random.randrange(1, 5)
		time.sleep(delay)
		library.write(name)

try:
	library = Library()
	for i in range(1, 10):
		thread.start_new_thread(reader, (i,library))
	for i in range(1, 2):
		thread.start_new_thread(writer, (i,library))
except:
	print "Error: Unable to start thread"

while True:
	pass
