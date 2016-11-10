#!/usr/bin/env python2

import sys
import subprocess

def exec_cmd(cmd):
    return subprocess.Popen(cmd,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

def caltobyte(hnum):
    num = float(hnum[0:-1])
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if hnum[-1] == unit:    return num
        num *= 1024.0

def sizeof_fmt(num):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s" % (num, unit)
        num /= 1024.0

proc = exec_cmd("cat /proc/meminfo")
output = proc.stdout.read()
field = output.split()

print field
