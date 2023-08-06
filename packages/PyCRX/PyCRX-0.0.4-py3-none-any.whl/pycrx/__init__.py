import os
import GPUtil
from tabulate import tabulate

#Regsitry functions below
def RegistryAdd(file, value):
	reg = open(file, 'w')
	reg.write(value)
	reg.close
def RegistryRemove(file):
	regrem = open(file, 'w')
	regrem.write('0')
	regrem.close
def RegistryEdit(file, value):
	editfile = open(file, 'w')
	editfile.write(value)
	editfile.close()

#"Kernel" Functions below
def KernelOpenFile(mode, file):
	os.system(mode + ' ' + file)
def KernelShutdownSystem():
	if os.name == 'nt':
		os.system('shutdown -t 0')
	else:
		os.system('shutdown now')
def KernelKillProc(proc):
	if os.name == 'nt':
		os.system(f'taskkill /f /IM {proc}')
	else:
		os.system(f'kill {proc}')
def KernelRebootSystem():
	if os.name == 'nt':
		os.system('shutdown -r -t 0')
	else:
		print('Running sudo reboot...')
		os.system('sudo reboot')
def KernelDevice(device):
	def get_size(bytes, suffix="B"):
  """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

	if device == 'all':
		print("="*40, "System Information", "="*40)
		uname = platform.uname()
		print(f"System: {uname.system}")
		print(f"Node Name: {uname.node}")
		print(f"Release: {uname.release}")
		print(f"Version: {uname.version}")
		print(f"Machine: {uname.machine}")
		print(f"Processor: {uname.processor}")
	if device == 'boot':
		# Boot Time
		print("="*40, "Boot Time", "="*40)
		boot_time_timestamp = psutil.boot_time()
		bt = datetime.fromtimestamp(boot_time_timestamp)
		print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
	if device == 'cpu':
		# let's print CPU information
		print("="*40, "CPU Info", "="*40)
		# number of cores
		print("Physical cores:", psutil.cpu_count(logical=False))
		print("Total cores:", psutil.cpu_count(logical=True))
		# CPU frequencies
		cpufreq = psutil.cpu_freq()
		print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
		print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
		print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
		#	CPU usage
		print("CPU Usage Per Core:")
		for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    	print(f"Core {i}: {percentage}%")
		print(f"Total CPU Usage: {psutil.cpu_percent()}%")
	if device == 'ram':
		# Memory Information
		print("="*40, "Memory Information", "="*40)
		# get the memory details
		svmem = psutil.virtual_memory()
		print(f"Total: {get_size(svmem.total)}")
		print(f"Available: {get_size(svmem.available)}")
		print(f"Used: {get_size(svmem.used)}")
		print(f"Percentage: {svmem.percent}%")
		print("="*20, "SWAP", "="*20)
		# get the swap memory details (if exists)
		swap = psutil.swap_memory()
		print(f"Total: {get_size(swap.total)}")
		print(f"Free: {get_size(swap.free)}")
		print(f"Used: {get_size(swap.used)}")
		print(f"Percentage: {swap.percent}%")
	if device == 'network':
		# Network information
		print("="*40, "Network Information", "="*40)
		# get all network interfaces (virtual and physical)
		if_addrs = psutil.net_if_addrs()
		for interface_name, interface_addresses in if_addrs.items():
    	for address in interface_addresses:
        print(f"=== Interface: {interface_name} ===")
        if str(address.family) == 'AddressFamily.AF_INET':
        	print(f"  IP Address: {address.address}")
        	print(f"  Netmask: {address.netmask}")
        	print(f"  Broadcast IP: {address.broadcast}")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
        	print(f"  MAC Address: {address.address}")
          print(f"  Netmask: {address.netmask}")
          print(f"  Broadcast MAC: {address.broadcast}")
		# get IO statistics since boot
		net_io = psutil.net_io_counters()
		print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
		print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")

	if device == 'gpu':
		print('Installing GPUtil...')
		os.system('python3 -m pip install gputil')
		print('Either finished, errored, or is already installed.')
		print('Installing Tabulate')
		os.system('python3 -m pip install tabulate')
		print('Either finished, errored, or is already installed.')
		print("="*40, "GPU Details", "="*40)
		gpus = GPUtil.getGPUs()
		list_gpus = []
		for gpu in gpus:
    	# get the GPU id
    	gpu_id = gpu.id
    	# name of GPU
    	gpu_name = gpu.name
    	# get % percentage of GPU usage of that GPU
    	gpu_load = f"{gpu.load*100}%"
    	# get free memory in MB format
    	gpu_free_memory = f"{gpu.memoryFree}MB"
    	# get used memory
    	gpu_used_memory = f"{gpu.memoryUsed}MB"
    	# get total memory
    	gpu_total_memory = f"{gpu.memoryTotal}MB"
    	# get GPU temperature in Celsius
    	gpu_temperature = f"{gpu.temperature} °C"
    	gpu_uuid = gpu.uuid
    	list_gpus.append((gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory, gpu_total_memory, gpu_temperature, gpu_uuid))
	print(tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory", "temperature", "uuid")))
