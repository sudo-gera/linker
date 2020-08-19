import gi
gi.require_version('Gtk', '3.0')
from subprocess import run as sh
import os
from gi.repository import Gtk
from traceback import format_exc as error
from os import get_terminal_size


def get(q, a, z):
	d = [w.split('=')[1] for w in a.split('\n') if '=' in w and w.split('=')[0].strip().lower() == q.lower()]
	d += [z]
	d = d[0]
	return d


Gtk = Gtk.IconTheme.get_default()

os.chdir('/mnt/c/Users/user/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/wsl/')

d = os.popen("dpkg --search '*.desktop' | awk '{print $2}' | sort --unique").read().split('\n')
d = [w.strip()[:-8] for w in d if os.path.exists(w)]

ps = open('linker.ps1', 'w')

count=0
lc=0
wid=get_terminal_size()[0]
for w in d:
	pc=int(count / len(d)*wid)
	print(pc*'#', end='\r')
	count+=1

	try:
		a = open(w + '.desktop').read()
	except:
		print(error())


	comm=get('exec',a, None)
	if comm == None or get('nodisplay',a,'false').lower().strip() == 'true':
		continue

	name = get('name', a, w)
	for e in '\\/:*?"<>|+%!@':
		name=name.replace(e,'_')

	icon = [Gtk.lookup_icon(get('icon', a, 'application-x-executable'), w, 0)
			for w in [48] + list(range(512))]
	icon += [Gtk.lookup_icon('application-x-executable', w, 0)
			 for w in [48] + list(range(512))]
	icon = [w.get_filename() for w in icon if w][0]
	sh(['convert', icon, name + '.ico'])

	sh(['cp',w+'.desktop',name+'.desktop'])

	b = open(name + '.bat', 'w')
	b.write('wsl "export DISPLAY=localhost:0.0; ' + comm + '"')
	b.close()

	ps.write(f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("c:/Users/user/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/wsl/{name}.lnk")
$Shortcut.TargetPath = "c:/Users/user/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/wsl/{name}.bat"
$Shortcut.IconLocation = "c:/Users/user/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/wsl/{name}.ico"
$Shortcut.Save()
Write-Host -NoNewline "{'#'*(pc-lc)}"
''')
	lc=pc
ps.close()
sh(['powershell.exe', './linker.ps1'])
print()