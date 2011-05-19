'''
Created on Oct 11, 2010

@author: locusfwork
'''
import os

from urlparse import urlparse

import pykickstart.parser as ksparser
import pykickstart.version as ksversion
from pykickstart.handlers.control import commandMap
from pykickstart.handlers.control import dataMap

from mic.imgcreate.kscommands import desktop 
from mic.imgcreate.kscommands import moblinrepo
from mic.imgcreate.kscommands import micboot

import ConfigParser
from  RuoteAMQP.workitem import DictAttrProxy

KSCLASS = ksversion.returnClassForVersion(version=ksversion.DEVEL)

class KSHandlers(KSCLASS):
    def __init__(self):
        ver = ksversion.DEVEL
        commandMap[ver]["desktop"] = desktop.Moblin_Desktop
        commandMap[ver]["repo"] = moblinrepo.Moblin_Repo
        commandMap[ver]["bootloader"] = micboot.Moblin_Bootloader
        dataMap[ver]["RepoData"] = moblinrepo.Moblin_RepoData
        KSCLASS.__init__(self, mapping=commandMap[ver])
    
def build_kickstart(base_ks, packages=[], groups=[], projects=[]):
    ks = ksparser.KickstartParser(KSHandlers())
    ks.readKickstart(base_ks)
    ks.handler.packages.add(packages)
    ks.handler.packages.add(groups)
    for prj in projects:
        name = urlparse(prj).path
        name = name.replace(":/","_")
        name = name.replace("/","_")
        repo = moblinrepo.Moblin_RepoData(baseurl=prj, name=name)
        ks.handler.repo.repoList.append(repo)
    ks_txt = str(ks.handler)
    return ks_txt

def worker_config(config=None, conffile="/etc/imager/img.conf"):
    if not config:
        config = ConfigParser.ConfigParser()
        config.read(conffile)

    section = "worker"
    conf = {}
    for item in ["base_url", "base_dir", "mic_opts", "img_home", "img_tmp"]:
        conf[item] = config.get(section, item)

    for item in ["use_kvm", "use_sudo"]:
        conf[item] = config.getboolean(section, item)

    if config.has_option(section, "ssh_key"):
        conf["ssh_key"] = config.get(section, "ssh_key")
    else:
        conf["ssh_key"] = os.path.join(conf["img_home"], 'id_rsa')
    
    if config.has_option(section, "base_img"):
        conf["base_img"] = config.get(section, "base_img")
    else:
        conf["base_img"] = os.path.join(conf["img_home"], 'base.img')

    if config.has_option(section, "mic_opts"):
        extra_opts = config.get(section, "mic_opts")
        extra_opts = extra_opts.split(",")
        conf["extra_opts"] = extra_opts

    dap = DictAttrProxy(conf)

    return dap

