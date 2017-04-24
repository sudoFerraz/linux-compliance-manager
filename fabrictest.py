import os

host = "centos"
ip = "10.51.202.72"
password = "animal"
out = os.popen('sudo fab -H'+host+'@'+ip+' -p '+password+' checklist').read()
print out
print 'fab -H '+host+'@'+ip+' checklist'