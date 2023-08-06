import os

def Registry(addremoveedit, regname, value):
	if addremoveedit == 'add':
		reg = open(regname, 'w')
		reg.write(value)
		reg.close
	if addremoveedit == 'remove':
		if os.name == 'nt':
			os.system(f'del /f {regname}')
		else:
			os.system(f'rm sysfiles/registry/{regname}')
	if addremoveedit == 'edit':
		print('')
		editfile = open(regname, 'w')
		editfile.write(value)
		editfile.close()

def Kernel():
	def openfile(mode, file):
		os.system(mode + ' ' + file)
	def shutdownsys():
		if os.name == 'nt':
			os.system('shutdown -t 0')
		else:
			os.system('shutdown now')
	def kproc(proc):
		if os.name == 'nt':
			os.system(f'taskkill /f /IM {proc}')
		else:
			os.system(f'kill {proc}')
def rebootsys():
		if os.name == 'nt':
			os.system('shutdown -r -t 0')
		else:
			print('Running sudo reboot...')
			os.system('sudo reboot')