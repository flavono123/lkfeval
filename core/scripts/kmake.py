#!/usr/bin/env python3
#-*-coding:utf-8-*-
import sys
import os

#for test
f = open('/home/bigs/testb', 'a+')
sys.stderr = f
sys.stdout = f

required_ops = ["-v"]
k_version = ''
k_extra = ''
k_configs = dict() # { "CONFIG_A" : "y", "CONFIG_B" : "m", ...}

k_src_dir = "/usr/src/linux-stable"
#k_repo = "https://github.com/torvalds/linux.git" #
k_repo = "git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git"

def print_help():
	print("print_help")

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def shell_command(command, error_str='', print_on_error=True, exit_on_error=True) :
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

def backup():
	pass
 
def restore():
	pass

#root privilage check
if os.geteuid() != 0:
	eprint("You need root permission.")
	exit(1)

#check required args
if not (set(required_ops) < set(sys.argv)) :
	eprint("failed : required_ops : "+str(requied_ops), print_on_error=False, exit_on_error=False)
	exit(1)

#parsing argument
pre_arg = ''
for arg in sys.argv :
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

print("args : ")
print("k_version : ", k_version)
print("k_extra : ", k_extra)
print("k_configs : ", k_configs)
print("k_src_dir : ", k_src_dir)
print("krepo : ", k_repo)


#dependeny
#shell_command("yes '' | apt-get install git fakeroot build-essential ncurses-dev xz-utils libssl-dev bc")

#if git does not exist
shell_command("command -v git", "failed : git does not exist")



#if src does not exist, git clone
if not os.path.isdir(k_src_dir) :
	print("source not founded.")
	print("git clone "+k_repo)
	shell_command("git clone "+k_repo+" "+k_src_dir)



print("cd "+k_src_dir)
os.chdir(k_src_dir)

shell_command("git stash", exit_on_error=False)
shell_command("git stash drop", exit_on_error=False)
#reset --hard 하는게 나은듯?

print("checkout "+k_version)
shell_command("git checkout v"+k_version)

#TODO maybe initial kernel repo doesn't have .config
print("configureing...")
#shell_command("yes '' | make localmodconfig") #TODO require default configㅑ
shell_command("yes '' | make defconfig") 
shell_command("yes '' | make olddefconfig")
shell_command("yes '' | make localmodconfig") #특히 vmware관련된게 있는듯
#shell_command("yes '' | make oldconfig") #엔터 자동입력으로 하면 localmodeconfig가 oldconfig로 넘어가는 중에 에러를 뱉으며 죽는다. 때문에 oldconfig 디폴트값으로 다시 설정해줘야함
'''
config_keys = k_configs.keys()
with open(k_src_dir="/new_config", 'w') as fnew_config :
	with open(k_src_dir+"/.config") as fconfig :
		for line in fconfig :
			if line.startswith('#'):
				break
			for config in config_keys :
				if line.startswith(config) : #if already there is the config
					fnew_config.write(config+"="+k_configs[config]
os.rename(k_src_dir+"/new_config", k_src_dir+"/.config")
'''
for k,v in k_configs.items() :
	if v.startswith('"') :
		shell_command('./scripts/config --set-str %s %s' % (k, v))
	else :
		shell_command('./scripts/config --set-val %s %s' % (k, v))

print("kernel extra version : ", k_extra)
#shell_command('sed -i "s/EXTRAVERSION =.*/EXTRAVERSION = %s/g" Makefile' % k_extra)
#make에 EXTRAVERSION=xxx 인자로 해서 줄 수있는듯, 그러면 소스변경이 없으니 stash도 필요없겠지?

print("make EXTRAVERSION=-%s" % k_extra)
shell_command("make EXTRAVERSION=-%s" % k_extra)
print("make modules")
shell_command("make modules")
print("make modules_install")
shell_command("make modules_install")
print("make install")
shell_command("make install")

				
				
			
			

