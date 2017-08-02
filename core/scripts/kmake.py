#!/usr/bin/env python3
#-*-coding:utf-8-*-

import sys
import os
import argparse
import subprocess
#from subprocess import Popen, PIPE

## constants
ROOT = 0

## global vars
# kernel resources
kernel_src_dir = "/usr/src/linux-stable"
kernel_stable_repo = "git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git"
# arguments
parser = argparse.ArgumentParser(description='Kerenl Make:'
                                             'make specific kernel image by referring args.'
                                             '(kernel version, configs ..)')
parser.add_argument = ('version', help='taget kernel version')
args = parser.parse_args()
version = args.version

## funcs
# run 'string' shell command
def run(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (stdout, stderr) = popen.communicate()
    if stderr :
        perror(stderr.decode('UTF-8'))
    else :
        print(stdout.decode('UTF-8'))
    return

def perror(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

## NOTE: script run under the root previledge
if os.geteuid() != 0:
    perror("kmake: Pemission denied")
    exit(1)

else:
    print("Hello, root!")
## 0. Prepare dependency tools
# gcc, make, git and openssl are essential
# 

## 1. Clone kernel's git stable repository
#

run("cd /usr/src")
run("git clone git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git")

## 2. Checkout to speicific kernel version
#

run("git tag ", + version)
