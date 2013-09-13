import pythoncom, pyHook, signal, os, sys, re
from collections import deque
import pickle
import blowfish
import random
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
from multiprocessing import Process, freeze_support
import time
import signal
import thread
import win32service
import win32serviceutil
import win32api
import win32con
import win32event
import win32evtlogutil
import os

bf_passphrase = '3138363238322e343035'
key_store = {}
applications = []
key_queue = deque()
data_dir = "c:\\kdata"

class Key_Serve(SimpleXMLRPCServer):
	
	def win_log(self, msg):
		import servicemanager
		servicemanager.LogInfoMsg(str(msg))
	
	def start(self):
		self.run = True
		while self.run:
			try:
				self.serve_forever()
			except KeyboardInterrupt:
				self.win_log("Keyboard Interrupt!")
				self.run = False
			except:
				self.win_log("Failed to start!")
				self.run = False
				
	def stop(self):
		self.run = False
		self.win_log("Stopping Service")
		
def read_binary(file):
    full_pick = data_dir + "\\" + file
    print data_dir
    print file
    print full_pick
    with open(full_pick, "rb") as handle:
        return xmlrpclib.Binary(handle.read())

def list_keyfiles():
    #define dll content list
    dll_list = []
    contents = os.listdir(data_dir)
    for item in contents:
	    if '.dll' in item:
		    dll_list.append(item)
    return dll_list

#serve xml and wait for connection
def xml_serve():
	
	try:
		
	    freeze_support()
 
	    setrundir()
        
            key_server = Key_Serve(("0.0.0.0", 8001))
            key_server.register_function(read_binary, 'read_binary')
            key_server.register_function(list_keyfiles, 'list_available')
            #key_server.start()
	
	except KeyboardInterrupt:
		
	    key_server.stop()
	
def setrundir():
    pathname = os.path.dirname(sys.argv[0])
    fullpath = os.path.abspath(pathname) 
    os.chdir(fullpath)

"""
try:
    freeze_support()
 
    setrundir()
        
    key_server = Key_Serve(("0.0.0.0", 8002))
    key_server.register_function(read_binary, 'read_binary')
    key_server.register_function(list_keyfiles, 'list_available')
    key_server.start()
	
except KeyboardInterrupt:
		
    key_server.stop()
"""

if __name__ == '__main__':
	pass
	#xml_serve()
	