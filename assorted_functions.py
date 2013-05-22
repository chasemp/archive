def get_ip_address(ifname):
 """Pass an interface name and receive the IP"""
 try:
   s = socket(AF_INET, SOCK_STREAM)
   ip = inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])
   return "OK: " + ifname + " IP Address is " + ip
 except:
   return "WARN: no such interface"

def check_nix_proc(proc):
 """looks up pid's of proccess.  checks to make sure they are running. requires pgrep."""
 cmd = "pgrep" + " " + proc
 p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
 pidlist = p.stdout.read().strip().split()
 if pidlist:
   for pid in pidlist:
     try:
       os.kill(int(pid), 0)
     except OSError, err:
       if err.errno == errno.ESRCH:
           procstat = "Not running"
           check = "WARN: "
       elif err.errno == errno.EPERM:
           procstat =  "No permission to signal this process!"
           check = "ERROR: "
       else:
           procstat = "Unknown error"
           check = "ERROR: "
   else:
       procstat = "is running."
       check = "OK: "
 else:
   procstat = "no such process pid"
   check = "WARN: "
 out = check + proc +  " " +  procstat
 return out

def check_drbd_stat():
 """Checks Heartbeat via cl_status"""
 cmd = "drbdadm state all"
 p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
 rawdrbdadm = p.stdout.read().strip()
 out = rawdrbdadm
 return out


def check_mount(mp):
 """pass a mountpoint and return it's mount status"""
 if os.path.ismount(mp):
   out = "OK: " + mp + " is mounted"
 else:
   out = "WARN: " + mp + " is not mounted"
 return out


#v_cipher functions for run!
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
    return ''.join([chr(n) for n in plain]
