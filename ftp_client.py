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
       else:
           #print "Successful upload."
           log.info("Successful upload")
       f.close()
       return
   def download(self, filename):
       f2 = open(filename, "wb")
       try:
           self.retrbinary("RETR " + filename,f2.write)
       except Exception:
           #print "Error in downloading the remote file"
           log.info("Successful upload")
       else:
           #print "Successful download!"
           log.info("Successful upload")
       f2.close()
       return
