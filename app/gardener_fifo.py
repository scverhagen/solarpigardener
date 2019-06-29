#!/usr/bin/python3

import os
import json

thisfilepath = os.path.dirname(__file__)

cmdfifopath = '/media/gardener/cmd'
statusfifopath = '/media/gardener/status'
fifobuffersize = 100

# create /tmp-gardener tmpfs mount point:
os.system("mkdir -p /media/gardener")
os.system("umount /media/gardener")
os.system("mount -t tmpfs -o size=32M,mode=777 tmpfs /media/gardener")

# set permissions:
os.system("chmod -R 0777 /media/gardener")

# make all params 777
os.system("chmod -R 777 /media/gardener")

if not os.path.exists(cmdfifopath):
    os.mkfifo(cmdfifopath)
    os.chmod(cmdfifopath, 0o777)
else:
    os.remove(cmdfifopath)
    os.mkfifo(cmdfifopath)
    os.chmod(cmdfifopath, 0o777)
    
class command_fifo(object):
    def checkforcommand(self):
        try:
            file = os.open(cmdfifopath, os.O_RDONLY | os.O_NONBLOCK)
            incmd = os.read(file, fifobuffersize)
            os.close(file)
            incmd = incmd.decode('utf-8')
        except:
            incmd = ''
        
        return incmd.strip()

    def sendcommand(self, cmd):
        try:
            with open(cmdfifopath, 'w') as fifo:
                fifo.write(cmd)
        except:
            pass
    
class status_fifo(object):
    def setstatus(self, statustxt):
        fifohandle = os.open(statusfifopath, os.O_TRUNC | os.O_WRONLY | os.O_CREAT)
        os.write(fifohandle, str.encode(statustxt + '\n'))
        os.close(fifohandle)

    def setstatusdict(self, statusdict):
        self.setstatus(json.dumps(statusdict))

    def getstatus(self):
        #try:
        fifohandle = os.open(statusfifopath, os.O_RDONLY)
        data = os.read(fifohandle, 100)
        os.close(fifohandle)
        status = data.decode()
        #except:
        #    stata = ''
        return status
    
    def getstatusdict(self):
        return json.loads(self.getstatus())