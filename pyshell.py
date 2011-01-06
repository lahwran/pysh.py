#!/usr/bin/python

import os
from glob import glob
import code
import subprocess
import readline
import random

for i in os.environ:
    globals()[i] = os.environ[i]

def strdict(d):
    out={}
    for i in d:
        if hasattr(d[i],"__str__"):
            out[i] = str(d[i])

class callprog:
    def __init__(self, name):
        self.name = name
        
    def __call__(self,*args):#,stdin=None,stdout=None,stderr=None):
        fullcommand = [self.name]
        fullcommand.extend(args)
        p = subprocess.Popen(fullcommand,env=strdict(globals()))#,stdin=stdin,stderr=stderr,stdout=stdout)
        return os.waitpid(p.pid, 0)[1]

__path__=PATH.split(":")
__path__.reverse()
allcommands={}

PROMPT="%u@%h:%d% "


for i in __path__:
    for j in glob(i+"/*"):
        allcommands[os.path.basename(j)] = callprog(j)
for i in allcommands:
    if i not in globals() and i not in dir(__builtins__):
        globals()[i] = allcommands[i]
class shellcommands:
    def __getattr__(self,name):
        return allcommands[name]
sh=shellcommands()
        
def __prompt__(defaultprompt):
    curdir = os.getcwd()
    #print '!'+defaultprompt+'!'
    R=str(random.randint(0,10000000))
    home=os.path.expanduser("~")
    if (R+curdir).startswith(R+home):
        curdir=(R+curdir).replace(R+home, "~")
    p = PROMPT.replace("%d",curdir).replace("%u",USER).replace("%h",os.uname()[1])
    if defaultprompt == ">>> ":
        return raw_input(p)
    else:
        p=(" "*(len(p)-4))+'... '
        
        return raw_input(p)
        
def cd(todir):
    todir=os.path.expanduser(todir)
    os.chdir(todir)
        
code.interact("",__prompt__,globals())
