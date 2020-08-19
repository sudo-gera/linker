#!/usr/bin/env python3
d=open
from os import *
from os.path import *
from sys import argv
from subprocess import run
if geteuid():
	print('restart with sudo')
	exit()
q=abspath(argv[0])
q=q[:-len(q.split('/')[-1])]
s=d(q+'linker.service','r').read()
s=s.replace('PATH',q)
d('/etc/systemd/system/linker.service','w').write(s)
system('sudo systemctl start linker')
system('sudo systemctl enable linker')
