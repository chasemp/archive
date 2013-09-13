'''

 Author: Alex Baker
 Date: 7th July 2008
 Description : Simple python program to generate wrap as a service based on example on the web, see link below.
 
 http://essiene.blogspot.com/2005/04/python-windows-services.html

 Usage : python aservice.py install
 Usage : python aservice.py start
 Usage : python aservice.py stop
 Usage : python aservice.py remove
 
 C:\>python aservice.py  --username <username> --password <PASSWORD> --startup auto install

'''

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
import custoclavis2
import XML_SClass
#from custoclavis2 import xml_serve
from XML_SClass import Key_Serve
from XML_SClass import read_binary
from XML_SClass import list_keyfiles
from XML_SClass import setrundir

class cxml_serve3(win32serviceutil.ServiceFramework):
   global key_server
   _svc_name_ = "cxml_serve3"
   _svc_display_name_ = "cxml_serve3 -- it serves xml!"
   _svc_description_ = "xml service"
         
   def __init__(self, args):
           win32serviceutil.ServiceFramework.__init__(self, args)
           self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
	   setrundir()
           self.key_server = Key_Serve(("0.0.0.0", 8005))
           self.key_server.register_function(read_binary, 'read_binary')
           self.key_server.register_function(list_keyfiles, 'list_available')

   def SvcStop(self):
           self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
           win32event.SetEvent(self.hWaitStop)
           self.key_server.stop()
         
   def SvcDoRun(self):
      import servicemanager      
      servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,servicemanager.PYS_SERVICE_STARTED,(self._svc_name_, '')) 
      
      self.timeout = 3000

      while 1:
         # Wait for service stop signal, if I timeout, loop again
         rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
         # Check to see if self.hWaitStop happened
         if rc == win32event.WAIT_OBJECT_0:
            # Stop signal encountered
            servicemanager.LogInfoMsg("aservice - STOPPED")
            break
         else:
            #servicemanager.LogInfoMsg("aservice - is alive and well")   
            servicemanager.LogInfoMsg("aservice - running custorun")
	    self.key_server.start()
      
def ctrlHandler(ctrlType):
   return True
                  
if __name__ == '__main__':   
   win32api.SetConsoleCtrlHandler(ctrlHandler, True)   
   win32serviceutil.HandleCommandLine(cxml_serve3)
