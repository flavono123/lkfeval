#!/usr/bin/env python3

import os
import sys
import argparse
from subprocess import Popen, PIPE


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

    def download(self, frm, to):
        return shell_command('scp -i {0} -P {1} "{2}@{3}:{4}" "{5}"'
                             .format(self._ssh_key, self._port, self._user, self._addr, frm, to))

    def upload(self, frm, to):
        return shell_command('scp -i {0} -P {1} "{2}" "{3}@{4}:{5}"'
                             .format(self._ssh_key, self._port, frm, self._user, self._addr, to))

parser = argparse.ArgumentParser(description='feature evaluation tools : make a kernel image and run a feature evaluation script')

#required arguments
parser.add_argument('vm', help='(.vmx) vmware machine')
parser.add_argument('ssh_key', help='ssh key to connect to geust')
parser.add_argument('k_version', help='copliling kerenl image on which evaluation will run')
parser.add_argument('eval_scripts', help='evaluation scripts', nargs='+')

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
args = parser.parse_args()

os.environ['PATH'] += ':'+args.vmrun_path

if not args.working_dir:
    if args.guest_user == 'root':
        args.working_dir = '/root/lkfes_working_dir'
    else:
        args.working_dir = '/home/{0}/lkfes_working_dir'.format(args.guest_user)


print("kerenl version : "+args.k_version)
print("eval_scripts : " + ", ".join(args.eval_scripts))
print("configs : " + ", ".join(args.config))

if not os.path.isfile(args.vm):
    print("error : "+args.vm+" does not exist.")
    exit(1)

shell_command('vmrun start "{0}"'.format(args.vm))

guest_ip = Popen(['vmrun', 'getGuestIPAddress', args.vm], env=os.environ.copy() ,stdout=PIPE).stdout.readline().decode('utf-8')#TODO error handling
guest_ip = guest_ip.strip()

guest = Remote_ssh(guest_ip, args.ssh_key, user=args.guest_user)

guest.shell_command('mkdir {0}'.format(args.working_dir), print_on_error=False, exit_on_error=False)

cores = [f for f in os.listdir(script_dir()) if os.path.isfile(os.path.join(script_dir(), f))]

for core in cores:
    guest.upload(script_dir()+'/'+core, args.working_dir)

for script in args.eval_scripts:
    guest.upload(script, args.working_dir)

#TODO externel tool upload

compile_script = args.working_dir+'/kmake.py'
compile_script_args = '-v "{0}" -c "{1}" -e "{2}"'.format(args.k_version, ",".join(args.config), args.extraversion)
guest.shell_command(compile_script+" "+compile_script_args)

update_script = args.working_dir+'/kupdate.sh'
update_script_args = '{0}-{1}+'.format(args.k_version, args.extraversion) #+ suffix is attached because of git change
guest.shell_command(update_script+' '+update_script_args)

shell_command('vmrun reset "{0}"'.format(args.vm))

log_dir = args.k_version+'-'+args.extraversion
guest.shell_command('mkdir {0}'.format(args.working_dir+'/'+log_dir), print_on_error=False, exit_on_error=False)

shell_command('mkdir {0}'.format(script_dir()+'../../logs/'+log_dir), print_on_error=False, exit_on_error=False)
for script in args.eval_scripts:
    log_file = args.working_dir+'/'+log_dir+'/'+script.split('/')[-1]+'.log'
    guest.shell_command(script+" | tee "+log_file)
    guest.download(log_file, script_dir()+'/../../logs/'+log_dir)

#guest.shell_command('rm -rf '+args.working_dir)

