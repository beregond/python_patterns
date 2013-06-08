import thread, threading, time, random, hashlib

"Solution for classic readers-writers problem."

# Semaphores
r = threading.BoundedSemaphore()
w = threading.BoundedSemaphore()

def generateData():
    data = hashlib.sha1()
    data.update(str(random.random()))
    return data.hexdigest()

resource = generateData()

def reader(name):
    global resource
    while True:
        delay = random.randrange(1, 5)
        time.sleep(delay)
        with w, r:
            print "Reader %s is reading resource: %s" % (name, resource)

def writer(name):
    global resource
    while True:
        delay = random.randrange(1, 5)
        time.sleep(delay)
        with w:
            resource = generateData()
            print "Writer %s changed data to %s" % (name, resource)

try:
    for i in range(1, 10):
        thread.start_new_thread(reader, (i,))
    for i in range(1, 2):
        thread.start_new_thread(writer, (i,))
except:
    print "Error: Unable to start thread"

while True:
    pass
