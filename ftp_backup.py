#!/usr/bin/env python
import zipfile, ftplib, os, sys, email, smtplib, logging, logging.handlers, time, signal
from datetime import datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

#################Zip File Settings##############
#full path to folder for archive
Archivedfolder = "/opt"
#
#################FTP Settings##############
#ftp login, usually 'bob@bob.com' format
username = "username"
#ftp password for above username
password = "pass"
#ftp server name or ip
server = "server"
#relative folder on ftp server
destpath = "."
#
#################Email Settings###############
to_addr = "you@you.com"
from_addr = "myjob@server.com"
subject = "job ran: "
mailserver = "localhost"
#
#################Log Settings################
LOG_FILENAME = "/var/log/ftpbackups.txt"
##############################################


class FTP_Client(ftplib.FTP):
   '''
   Extends the default FTP class to include upload and download methods
   '''
   def upload(self, filename):
       f = open(filename, "rb")
       try:
           self.storbinary("STOR " + filename,f)
       except Exception:
#           print "Error in uploading file"
           log.error("Error in uploading file")
           return False
       else:
           #print "Successful upload."
           log.info("Successful upload")
           return True
       f.close()
   def download(self, filename):
       f2 = open(filename, "wb")
       try:
           self.retrbinary("RETR " + filename,f2.write)
       except Exception:
           #print "Error in downloading the remote file"
           log.error("Error in uploading file")
           return False
       else:
           #print "Successful download!"
           log.info("Successful upload")
           return True
       f2.close()

def signal_handler(signal, frame):
       sname = os.path.split(sys.argv[0])[1]
       print "\n   %s stopped via ctrl+c signal!\n" % (sname)
       sys.exit(0)

def makeArchive(fileList, archive):
 """
 'fileList' is a list of file names - full path each name
 'archive' is the file name for the archive with a full path
 """
 try:
   a = zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED)
   for f in fileList:
#      print "archiving file %s" % (f)
     log.debug("archiving file %s" % (f))
     a.write(f)
   a.close()
   log.info("Archive zip file %s was created." % (archive))
   return True

 except:
     return False
     log.error("Archive zip file %s failed to create" % (archive))

def dirEntries(dir_name, subdir, *args):
 '''
 Return a list of file names found in directory 'dir_name'
 If 'subdir' is True, recursively access subdirectories under 'dir_name'.
 Additional arguments, if any, are file extensions to match filenames. Matched
   file names are added to the list.
 If there are no additional arguments, all files found in the directory are
   added to the list.
 Example usage: fileList = dirEntries(r'H:\TEMP', False, 'txt', 'py')
   Only files with 'txt' and 'py' extensions will be added to the list.
 Example usage: fileList = dirEntries(r'H:\TEMP', True)
   All files and all the files in subdirectories under H:\TEMP will be added
   to the list.
 '''
 fileList = []
 for file in os.listdir(dir_name):
   dirfile = os.path.join(dir_name, file)
   if os.path.isfile(dirfile):
     if not args:
       fileList.append(dirfile)
     else:
       if os.path.splitext(dirfile)[1][1:] in args:
         fileList.append(dirfile)
   # recursively access file names in subdirectories
   elif os.path.isdir(dirfile) and subdir:
     log.debug("Accessing directory: %s" % (dirfile))
     fileList.extend(dirEntries(dirfile, subdir, *args))
 return fileList

def ftp_upload(server, username, password, destpath, srcpath):
 """
 Connects, logs in, and uploads a file to a particular path
 """
 try:
   log.info("connecting to FTP server...")
   ftpconnect = FTP_Client(server)
   log.debug(server)
   ftpconnect.login(username,password)
   ftpconnect.cwd(destpath)
   log.debug("Destpath: " + destpath)
   splitpath = os.path.split(srcpath)
   file = splitpath[1]
   srcdir = splitpath[0]
   os.chdir(srcdir)
   log.debug("Srcdir: " + srcdir)
   log.info("uploading file %s." % (file))
   ftpconnect.upload(file)
   result = "Backup Successed!"
   log.info(result)
 except:
   result = "Backup Failured!"
   log.error(result)
 return result

def remove_file(file):
   os.remove(file)
   if os.path.isfile(file):
       log.error("Error: file %s cannot be removed" % (file))
   else:
       log.info("Temp file %s has been removed" % (file))
   return

def send_mail(from_addr, to_addr, subject, body, attach=[], server="localhost"):
 try:
   msg = MIMEMultipart()
   msg['From'] = from_addr
   log.debug(from_addr)
   msg['To'] = to_addr
   log.debug(to_addr)
   msg['Date'] = formatdate(localtime=True)
   msg['Subject'] = subject
   log.debug(subject)
   log.debug("Body: \n" + body)
   msg.attach( MIMEText(body) )


   for f in attach:
     log.debug("Attaching file %s" % (f))
     part = MIMEBase('application', "octet-stream")
     part.set_payload( open(f,"rb").read() )
     Encoders.encode_base64(part)
     part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
     msg.attach(part)


   smtp = smtplib.SMTP(server)
   log.debug("Mail server " + server)
   smtp.sendmail(from_addr, to_addr, msg.as_string())
   smtp.close()
   log.info("Mail sent!")
 except:
     log.error("Mail failed to send!")

def set_logging(LOGFILENAME, CON_LEVEL="info", FILE_LEVEL="info", RUNLOG_LEVEL="info"):
 """
   sets up logging instance with log file, console level, and file level logging.
   logger name is script name without ".py" on the end.
 """
 #global names defined in logging module
 global log
 global single_run_log
 #logger name will be script name without ".py"
 sname = os.path.split(sys.argv[0])[1].rstrip(".py")
 logger = sname
 #set log variable name as global
 single_run_log = LOG_FILENAME.rstrip(".txt") + "_runlog.txt"
 runlogfile = open ( single_run_log, 'w' )
 #Define dictionary of levels
 LEVELS = {'debug': logging.DEBUG,
         'info': logging.INFO,
         'warning': logging.WARNING,
         'error': logging.ERROR,
         'critical': logging.CRITICAL}
 # set up logger instance and set level
 log = logging.getLogger(logger)
 log.setLevel(logging.DEBUG)
 # Handlers for console, file size, and last run log
 console = logging.StreamHandler()
 rotate = logging.handlers.RotatingFileHandler(LOGFILENAME, mode='w', maxBytes=10000, backupCount=0)
 runlog = logging.StreamHandler(runlogfile)
 # set a format for handlers
 console_format = logging.Formatter('%(levelname)-8s %(message)s')
 file_format = logging.Formatter("%(asctime)s %(name)s %(levelname)-8s %(message)s")
 runlog_format = logging.Formatter("%(asctime)s %(name)s %(levelname)-8s %(message)s")
 #set logging levels
 runlog_out = LEVELS.get(RUNLOG_LEVEL, logging.NOTSET)
 runlog.setLevel(runlog_out)
 conout = LEVELS.get(CON_LEVEL, logging.NOTSET)
 console.setLevel(conout)
 fileout = LEVELS.get(FILE_LEVEL, logging.NOTSET)
 rotate.setLevel(fileout)
 # tell the handlers to use their format
 runlog.setFormatter(runlog_format)
 console.setFormatter(console_format)
 rotate.setFormatter(file_format)
 # add the handler to the logger
 logging.getLogger(logger).addHandler(runlog)
 logging.getLogger(logger).addHandler(console)
 logging.getLogger(logger).addHandler(rotate)

def file_by_date(filename, type):
 date = time.strftime('%x').replace("/", "_")
 date_file = "/tmp/%s_%s%s" % (date, filename, type)
 return date_file

def main():

 #Set up script to handle quit signals
 signal.signal(signal.SIGINT, signal_handler)

 #set logging (info and debug most useful) and log current time
 set_logging(LOG_FILENAME, CON_LEVEL="debug", FILE_LEVEL="info", RUNLOG_LEVEL="info")
 log.info(datetime.now().ctime())

 #define zip file name by date
 ZipFileDest = file_by_date("NMSCLS_Backup", ".zip")

 #recursively creates zip (named above) of a directory
 makeArchive(dirEntries(Archivedfolder, True), ZipFileDest)

 #connect and upload to FTP
 result = ftp_upload(server, username, password, destpath, ZipFileDest)

 #removing temporary zip file
 remove_file(ZipFileDest)

 mail_body= """\
The backup %s to %s has returned the following: \n %s: %s
  """ % (ZipFileDest, server + "\\" + destpath, datetime.now().ctime(), result)

 #send email via smtp
 send_mail(from_addr, to_addr, subject + result, mail_body, attach=[single_run_log], server=mailserver)

if __name__ == '__main__':
 main()
