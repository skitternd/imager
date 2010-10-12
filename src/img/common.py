'''
Created on Oct 11, 2010

@author: locusfwork
'''
import os
import io
import random
import pwd,grp
from worker import ImageWorker
import ConfigParser

conf = open("/etc/imager/img.conf")
config = ConfigParser.ConfigParser()
config.readfp(conf)
conf.close()

base_url = config.get('worker', 'base_url')
base_dir = config.get('worker', 'base_dir')
def mic2(id, name,  type, email, kickstart, release, arch="i586", work_item=None):
        dir = "%s/%s"%(base_dir, id)
        print dir
        os.mkdir(dir, 0775)
        
        ksfilename = ""
        ksfilename = dir+'/'+name+'.ks'
        
        tmp = open(ksfilename, mode='w+b')
        print tmp.name   
        tmpname = tmp.name
        logfile_name = dir+'/'+name+"-log"
        tmp.write(kickstart)            
        tmp.close()
        os.chmod(tmpname, 0644)
        file = base_url+"%s"%id    
        logfile = open(logfile_name,'w')
        logurl = base_url+id+'/'+os.path.split(logfile.name)[-1]
        worker = ImageWorker(id, tmpname, type, logfile, dir, work_item=work_item, name=name, release=release, arch=arch)
        worker.build()
        logfile.close()