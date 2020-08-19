import gi
from subprocess import run as sh
import os
from traceback import format_exc as error
from os import get_terminal_size
from json import loads
from json import dumps
from os import getenv
from os import popen
from subprocess import check_output as output
from sys import argv

quiet=0
if '-q' in argv:
    quiet=1

slow=0
if '-s' in argv:
    slow=1

gi.require_version('Gtk', '3.0')
exec('from gi.repository import Gtk')


def get(q, a, z):
    d = [w.split('=')[1] for w in a.split('\n') if '=' in w and w.split(
        '=')[0].strip().lower() == q.lower()]
    d += [z]
    d = d[0]
    return d


Gtk = Gtk.IconTheme.get_default()

os.chdir('/mnt/c/Users/user/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/wsl/')

try:
    db = loads(open(getenv('HOME') + '/.linker').read())
except BaseException:
    db = dict()

d = os.popen(
    "dpkg --search '*.desktop' | awk '{print $2}' | sort --unique").read().split('\n')
d = [w.strip()[:-8] for w in d if os.path.exists(w)]

ps = open('linker.ps1', 'w')

count = 0
lc = 0
wid = get_terminal_size()[0]
from time import time
t=dict()
for w in d:

    if slow:
        sleep(0.01)

    if quiet==0:
        pc = int(count / len(d) * wid)
        print(pc * '#', end='\r')
        count += 1

    new=0

    try:
        a = open(w + '.desktop').read()
    except BaseException:
        print(error())


    comm = get('exec', a, None)
    if comm is None or get('nodisplay', a, 'false').lower().strip() == 'true':
        continue

    while '%' in comm:
        comm = comm[:comm.index('%')] + comm[comm.index('%') + 2:]

    name = get('name', a, w)
    for e in '\\/:*?"<>|+%!@':
        name = name.replace(e, '_')

    if name not in db:
        db[name]=dict()
        new=1

    icon = None
    for w in [48]+list(range(512)):
        if icon:
            break
        icon=Gtk.lookup_icon(get('icon', a, 'application-x-executable'), w, 0)
    for w in [48]+list(range(512)):
        if icon:
            break
        icon=Gtk.lookup_icon('application-x-executable', w, 0)

    icon = icon.get_filename()

    hash = str(sum([w*2**(e%60) if e%2 else -w*2**(e%60) for e,w in enumerate(open(icon,'rb').read())]))
    if icon not in db[name] or db[name][icon] != hash:
        db[name][icon] = hash
        sh(['convert', icon, name + '.ico'])
        new=1

#    sh(['cp', w + '.desktop', name + '.desktop'])

    script='export DISPLAY=localhost:0.0; ' + comm
    if 'sh' not in db[name] or db[name]['sh']!=script:
        b = open(name + '.sh', 'w')
        b.write(script)
        b.close()
        db[name]['sh']=script

    script='wsl "/mnt/c/Users/user/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/wsl/'+name +'.sh"'
    if 'bat' not in db[name] or db[name]['bat']!=script:
        b = open(name + '.bat', 'w')
        b.write(script)
        b.close()
        db[name]['bat']=script

    if new:
        ps.write(f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("c:/Users/user/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/wsl/{name}.lnk")
$Shortcut.TargetPath = "c:/Users/user/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/wsl/{name}.bat"
$Shortcut.IconLocation = "c:/Users/user/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/wsl/{name}.ico"
$Shortcut.Save()
''')
    if quiet==0:
        ps.write(f'''
Write-Host -NoNewline "{'#'*(pc-lc)}"
''')
        lc = pc
ps.close()
if quiet==0:
    print(' '*wid)
sh(['powershell.exe', './linker.ps1'])
if quiet==0:
    print(' '*wid)
open(getenv('HOME') + '/.linker', 'w').write(dumps(db))
