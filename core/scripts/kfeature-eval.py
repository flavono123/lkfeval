#!/usr/bin/env python3

import os
import sys
import argparse
from subprocess import Popen, PIPE
import json


def script_dir():
    return sys.path[0]

def shell_command(command, error_str='', print_on_error=True, exit_on_error=True):
    ret = os.system(command)

    if ret:
        if print_on_error:
            if error_str:
                print(error_str, file=sys.stderr)
            else:
                print("failed : " + command, file=sys.stderr)
        if exit_on_error:
            exit(1)
    return ret

def popen_command(command, print_stdout=False, print_stderr=False):
    p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    if p.returncode :
        return None, None
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    if print_stdout:
        print(out)
    if print_stderr:
        print(err)
    return out, err


class Remote_ssh:
    def __init__(self, addr, ssh_key, user='root', port=22):
        self._addr = addr
        self._port = port
        self._ssh_key = ssh_key
        self._user = user

    def shell_command(self, command, error_str='', print_on_error=True, exit_on_error=True):
        # print('ssh -i {0} -p {1} {2}@{3} {4}'
        #                      .format(self._ssh_key, self._port, self._user, self._addr, command))
        return shell_command('ssh -i {0} -p {1} "{2}@{3}" "{4}"'
                             .format(self._ssh_key, self._port, self._user, self._addr, command),
                             error_str, print_on_error, exit_on_error)

    def popen_command(self, command, print_stdout=False, print_stderr=False):
        command = 'ssh -i {0} -p {1} "{2}@{3}" "{4}"'\
            .format(self._ssh_key, self._port, self._user, self._addr, command)
        return popen_command(command)

    def download(self, frm, to):
        return shell_command('scp -i {0} -P {1} -r "{2}@{3}:{4}" "{5}"'
                             .format(self._ssh_key, self._port, self._user, self._addr, frm, to))

    def upload(self, frm, to):
        return shell_command('scp -i {0} -P {1} -r "{2}" "{3}@{4}:{5}"'
                             .format(self._ssh_key, self._port, frm, self._user, self._addr, to))

def get_vm_ip(vm):
	popen_guest_ip = Popen(['vmrun', 'getGuestIPAddress', vm], env=os.environ.copy() ,stdout=PIPE)
	
	out, err = popen_guest_ip.communicate()


	if popen_guest_ip.returncode:
            return None
	return out.decode('utf-8').strip()

parser = argparse.ArgumentParser(description='feature evaluation tools : make a kernel image and run a feature evaluation script')

#required arguments
parser.add_argument('vm', help='(.vmx) vmware machine')
parser.add_argument('ssh_key', help='ssh key to connect to geust')
parser.add_argument('f_name', help='the name of evaluated feature')
parser.add_argument('k_version', help='copliling kerenl image on which evaluation will run')
parser.add_argument('eval_script', help='evaluation script')
parser.add_argument('log_file_name', help='evaluation log file name')

#main optional arguments
parser.add_argument('-c', '--config', nargs='+', help='configs for kernel compile (CONFIG_*)',
                    default='')
uname = os.uname()[0]
def_vmrun_path = ''
if uname == 'Darwin':
    def_vmrun_path = '/Applications/VMware Fusion.app/Contents/Library'
elif uname == 'Linux':
    def_vmrun_path = '/usr/lib/vmware-vix/lib'
parser.add_argument('-vp', '--vmrun_path', help='vmrun path of vmware', default=def_vmrun_path)
parser.add_argument('-e', '--extraversion', help='extraversion used kernel compile', default='')


#extra optional arguments
parser.add_argument('-gu', '--guest_user', help='guest id on vmware machine', default='root')
parser.add_argument('-gp', '--guest_passwd', help='geust password on vmware machine', default='root')
parser.add_argument('-sshp', '--ssh_port', help='ssh port of guest', type=int, default=22)
parser.add_argument('-wd', '--working_dir', help=
'working dir in guest. scripts and logs are maked temporarily on the directory.')
parser.add_argument('-sl', '--spec_log', help='enable logging the spec of guest.', action='store_true')
args = parser.parse_args()


print("kerenl version : "+args.k_version)
print("eval_script : " + args.eval_script)
print("configs : " + ", ".join(args.config))

last_evaluated_kernel_file_name = script_dir()+'/.last_evaluated_kernel'
eqaul_to_last = True
print("comparing last kernel options...")
try:
    last_evaluated_kernel_file = open(last_evaluated_kernel_file_name, 'r')
    last_evaluated_kernel = json.load(last_evaluated_kernel_file)
    print('last : ')
    print(last_evaluated_kernel)
    if last_evaluated_kernel['version'] != args.k_version:
        eqaul_to_last = False
    if sorted(last_evaluated_kernel['config']) != sorted(args.config):
        eqaul_to_last = False
    last_evaluated_kernel_file.close()
    #TODO 이번정보랑 이전정보랑 같을 경우 컴파일하고 리부트하는거 스킵
except FileNotFoundError:
    eqaul_to_last = False
if eqaul_to_last:
    print("equals to last compiled kernel image, skip making new kernel image.")
else:
    print("different to last compiled kernel image, make new kernel image.")

os.environ['PATH'] += ':'+args.vmrun_path

if not args.working_dir:
    if args.guest_user == 'root':
        args.working_dir = '/root/lkfes_working_dir'
    else:
        args.working_dir = '/home/{0}/lkfes_working_dir'.format(args.guest_user)

if args.extraversion:
	if not args.extraversion.startswith('-'):
		args.extraversion = '-'+args.extraversion
	args.extraversion = args.extraversion.replace('_','-')



if not os.path.isfile(args.vm):
    print("error : "+args.vm+" does not exist.")
    exit(1)

shell_command('vmrun start "{0}"'.format(args.vm))

guest_ip = get_vm_ip(args.vm)
while not guest_ip:
    guest_ip = get_vm_ip(args.vm)
print("guest ip : "+guest_ip)

guest = Remote_ssh(guest_ip, args.ssh_key, user=args.guest_user)

guest.shell_command('mkdir -p "{0}"'.format(args.working_dir))


eval_dir = '/'.join(args.eval_script.split('/')[:-1])

guest.upload(script_dir(), args.working_dir)
guest.upload(eval_dir, args.working_dir)

remote_script_dir = args.working_dir+'/'+script_dir().split('/')[-1]

if not eqaul_to_last :
    compile_script = remote_script_dir+'/kmake.py'
    if args.config:
        compile_script_args = '-v "{0}" -c "{1}" -e "{2}"'.format(args.k_version, ",".join(args.config), args.extraversion)
    else:
        compile_script_args = '-v "{0}" -e "{2}"'.format(args.k_version, ",".join(args.config), args.extraversion)
    guest.shell_command('cd {0};{1} {2}'.format(remote_script_dir, compile_script, compile_script_args))

    # save make info for redundant re-compile
    last_evaluated_kernel = dict()
    last_evaluated_kernel["version"] = args.k_version
    last_evaluated_kernel["config"] = args.config

    # 이번 컴파일 정보를 저장, 바로 다음의 정보가 같을 경우 재컴파일할 필요가 없겠지
    last_evaluated_kernel_file = open(last_evaluated_kernel_file_name, 'w+')
    json.dump(last_evaluated_kernel, last_evaluated_kernel_file)
    last_evaluated_kernel_file.close()


    update_script = remote_script_dir+'/kupdate.sh'
    k_version = args.k_version
    if k_version.count('.') == 1 :
        k_version = k_version+'.0'
    update_script_args = '{0}{1}+'.format(k_version, args.extraversion) #+ suffix is attached because of git change
    guest.shell_command('cd {0};{1} {2}'.format(remote_script_dir, update_script, update_script_args))

    print("reboot guest..")
    shell_command('vmrun reset "{0}"'.format(args.vm))

    guest_ip = get_vm_ip(args.vm)
    while not guest_ip:
        guest_ip = get_vm_ip(args.vm)
    print("guest ip : " + guest_ip)

log_dir = args.f_name
guest.shell_command('mkdir -p {0}'.format(args.working_dir+'/'+log_dir))
shell_command('mkdir -p {0}'.format(script_dir()+'/../../logs/'+log_dir))

#eval log
print("feature evaluation starts")
remote_eval_dir = args.working_dir+'/'+eval_dir.split('/')[-1]
script_name = args.eval_script.split('/')[-1]
print("-------{0}-------".format(script_name))
log_file = args.working_dir+'/'+log_dir+'/'+args.log_file_name
guest.shell_command('cd {0};{1}'.format(remote_eval_dir, './'+script_name+" | tee "+log_file), exit_on_error=False)

guest.download(log_file, script_dir()+'/../../logs/'+log_dir)

guest.shell_command('rm -rf '+args.working_dir)

#spec log
if args.spec_log:

    print("measuring spec of guest vm..")
    hw_spec_log_file = script_dir()+'/../../logs/'+log_dir +'/'+args.f_name+'.hw_spec'
    if not os.path.exists(hw_spec_log_file):
        hw_spec = dict()
        cpu = dict()
        out, err = guest.popen_command('cat /proc/cpuinfo | grep "model name"')

        if out:
            cpus = out.strip().split('\n')
            cpu['model'] = cpus[0].split(':')[-1].strip()
            cpu['cnt'] = len(cpus)
        out, err = guest.popen_command('lscpu')
        if out:
            cpu['detail'] = out.strip()

        mem = dict()
        out, err = guest.popen_command('cat /proc/meminfo | grep MemTotal')
        if out:
            mem['size'] = out.split(':')[-1].strip()

        disk = dict()
        out1, err = guest.popen_command('cat /sys/block/sd*/device/model')
        if out1:
            models = [model.strip() for model in out1.strip().split('\n')]
        out2, err = guest.popen_command('cat /sys/block/sd*/size')
        if out2:
            sizes = [size.strip() for size in out2.strip().split('\n')]
        if out1 and out2:
            disk['devs'] = [{'model' : ms[0], 'size' : str(int(ms[1])*512/1024)+' kB'  } for ms in zip(models, sizes)]
        out, err = guest.popen_command('lsblk')
        if out:
            disk['detail'] = out.strip()

        vga = dict()
        out, err = guest.popen_command('lspci | grep VGA')
        if out:
            vga['model'] = out.split(':')[-1].strip()

        hw_spec['cpu'] = cpu
        hw_spec['mem'] = mem
        hw_spec['disk'] = disk
        hw_spec['vga'] = vga

        with open(hw_spec_log_file, 'w') as hw_spec_log:
            json.dump(hw_spec, hw_spec_log)

    sw_spec = dict()
    sw_spec['configs'] = args.config
    out, err = guest.popen_command('cat /etc/os-release | PRETTY_NAME')
    if out:
        sw_spec['os_release'] = out.strip().strip('"')
    sw_spec['kernel_version'] = args.k_version
    out, err = guest.popen_command('echo __VERSION__ | gcc -E - | grep -v ^#')
    if out:
        sw_spec['compiler'] = out.strip().strip('"')
    sw_spec_log_file = script_dir()+'/../../logs/'+log_dir+'/'+args.log_file_name+'.sw_spec'
    with open(sw_spec_log_file, 'w') as sw_spec_log:
        json.dump(sw_spec, sw_spec_log)








