# a simple portscanner with multithreading
# QUEUE BASED VERSION

import socket
import sys
import threading, Queue

MAX_THREADS = 2

class Scanner(threading.Thread):
    def __init__(self, inq, outq):
        threading.Thread.__init__(self)
        self.setDaemon(1)
        # queues for (host, port)
        self.inq = inq
        self.outq = outq

    def run(self):
        while 1:
            host, port = self.inq.get()
            sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
            try:
                # connect to the given host:port
                sd.connect((host, port))
            except socket.error:
                # set the CLOSED flag
                self.outq.put((host, port, 'CLOSED'))
            else:
                self.outq.put((host, port, 'OPEN'))
                sd.close()

def scan(host, start, stop, nthreads=MAX_THREADS):
    scan_results = {}
    scan_results["host"] = host
    scan_results["start_port"] = start
    scan_results["stop_port"] = stop
    scan_results["threads"] = MAX_THREADS
    toscan = Queue.Queue()
    scanned = Queue.Queue()

    scanners = [Scanner(toscan, scanned) for i in range(nthreads)]
    for scanner in scanners:
        scanner.start()

    hostports = [(host, port) for port in xrange(start, stop+1)]
    for hostport in hostports:
        toscan.put(hostport)

    results = {}

    for host, port in hostports:
        while (host, port) not in results:
            nhost, nport, nstatus = scanned.get()
            results[(nhost, nport)] = nstatus
        status = results[(host, port)]
	scan_results["state"] = status
        if status <> 'CLOSED':
	    tcp_status = "open"
	else:
	    tcp_status = "closed"
	return scan_results

if __name__ == '__main__':
    scan('localhost', 25, 1024)