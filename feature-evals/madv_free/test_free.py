#!/usr/bin/env python2
#-*-coding:utf-8-*-

import sys
import os
import subprocess
import numpy

def exec_cmd(cmd):
    return subprocess.Popen(cmd,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

def set_cmd(flag):
    cmd = "./ebizzy_madv -S 10 -n 512"
    if flag == "MADV_FREE":
        cmd += " -f"
    return cmd

def ebizzy_madv(flag):
    exec_cmd("echo 3 > /proc/sys/vm/drop_caches")
    exec_cmd("echo 3 > /proc/sys/vm/drop_caches")
    exec_cmd("echo 3 > /proc/sys/vm/drop_caches")
    cmd = set_cmd(flag)
    return exec_cmd(cmd)

# System set
exec_cmd("echo 3 > /proc/sys/vm/drop_caches")
exec_cmd("echo 90 > /proc/sys/vm/dirty_ratio")

if not os.path.isfile("ebizzy_madv"):
    exec_cmd("make ebizzy_madv 1>/dev/null")

records = 0
usr = 0.0
sys = 0.0

test = 11

# Output format of ebizzy_madv
# <records> records/s
# real    <time> s
# usr     <time> s
# sys     <time> s
for i in range (test) :
    result = ebizzy_madv("MADV_FREE")
    if i == 0: continue # first iteration is just warm up!
    output = result.stdout.read()
    field = output.split()
    records += int(field[0])
    real = float(field[3])
    usr += float(field[6])
    sys += float(field[9])

records /= (test - 1)
usr /= (test - 1)
sys /= (test - 1)

row = "MADV_FREE"
col_list= ["Records/s", "Real(s)", "System(s)", "User(s)"]
data = numpy.array([records, real, usr, sys])
row_format = "{:>15}" * (len(col_list) + 1)

print row_format.format("", *col_list)
print row_format.format(row, *data)

exec_cmd("make clean")
