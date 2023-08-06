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

def KernelAction(action, two):
	if action == 'openfile':
		os.system(two)
	if action == 'shutdownsys':
		if os.name == 'nt':
			os.system('shutdown -t 0')
		else:
			os.system('shutdown now')
	if action == 'kproc':
		if os.name == 'nt':
			os.system(f'taskkill /f /IM {two}')
		else:
			os.system(f'kill {two}')
	if action == 'rebootsys':
		if os.name == 'nt':
			os.system('shutdown -r -t 0')
		else:
			print('Running sudo reboot...')
			os.system('sudo reboot')