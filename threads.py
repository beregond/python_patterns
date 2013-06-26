import thread, threading, time, random, hashlib

"Solution for classic readers-writers problem."

# Semaphores
r = threading.BoundedSemaphore()
w = threading.BoundedSemaphore()
c = threading.BoundedSemaphore()
clients = 0
event = threading.Event()
event.set()

def generateData():
	data = hashlib.sha1()
	data.update(str(random.random()))
	return data.hexdigest()

resource = generateData()

def reader(name):
	global resource, clients, event
	while True:
		delay = random.randrange(1, 5)
		time.sleep(delay)
		with w:
			event.clear()
			with c:
				clients += 1
		with r:
			print "Reader %s is reading resource: %s" % (name, resource)
		with c:
			clients -= 1
			if clients == 0:
				event.set()

def writer(name):
	global resource, clients, event
	while True:
		delay = random.randrange(1, 5)
		time.sleep(delay)
		with w:
			event.wait()
			resource = generateData()
			print "Writer %s changed data to %s" % (name, resource)
			event.clear()

try:
	for i in range(1, 10):
		thread.start_new_thread(reader, (i,))
	for i in range(1, 2):
		thread.start_new_thread(writer, (i,))
except:
	print "Error: Unable to start thread"

while True:
	pass
