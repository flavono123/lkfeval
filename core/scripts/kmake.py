import sys
import os

required_ops = ["-v"]
k_version = ''
k_extra = ''
k_configs = dict() # { "CONFIG_A" : "y", "CONFIG_B" : "m", ...}

k_src_dir = "/usr/src/linux"
k_repo = "https://github.com/torvalds/linux.git"

def print_help():
	print "print_help"

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def sell_command(command, error_str='', print_on_error=True, exit_on_error=True) :
	ret = os.system(command)
	if ret : 
		if print_on_error :
			if error_str :
				eprint(error_str)
			else : 
				eprint("failed : "+command)
			if exit_on_error :
				exit(1)
	return ret
	 
		

#check required args
if not (set(required_ops) < set(sys.argv)) :
	eprint("failed : required_ops : "+str(requied_ops))
	print_help()
	exit(1)

#parsing argument
pre_arg = argv[0]
for arg in argv :
	if pre_arg == '-v' :
		k_version = arg
	elif pre_arg == '-e' :
		k_extra = arg
	elif pre_arg == '-c' :
		configs = arg.split(',')
		k_configs = {config : value for config, value in 
			(configs.split('=') for configs in arg.split(',')) }
	elif pre_arg == '--kernel_src_dir' :
		k_src_dir = arg
	elif pre_arg == '--kernel_repo' :
		k_repo = arg
	pre_arg = arg

print "args : ",
print "k_version : ", k_version
print "k_extra : ", k_extra
print "k_configs : ", k_configs


#if git does not exist
shell_command("command -v git", "failed : git does not exist")

#if src does not exist, git clone
if os.path.isdir(k_src_dir) :
	shell_command("git clone "+k_repo)

shell_command("git chekcout v"+k_version)

#TODO maybe initial kernel repo doesn't have .config
print("configureing...")
config_keys = k_configs.keys()
with open(k_src_dir="/new_config", 'w') as new_config :
	with open(k_src_dir+"/.config") as config :
		for line in config :
			for config in config_keys :
				if line.startswith(config) : #if already there is the config
				
				
			
			

