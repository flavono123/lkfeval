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

def parallel_dir():
    exec_cmd("echo 3 > /proc/sys/vm/drop_caches")
    exec_cmd("echo 3 > /proc/sys/vm/drop_caches")
    exec_cmd("echo 3 > /proc/sys/vm/drop_caches")
    return exec_cmd("./parallel_dir")

# System set
exec_cmd("echo 3 > /proc/sys/vm/drop_caches")
exec_cmd("echo 90 > /proc/sys/vm/dirty_ratio")

# Generate some file to lookup
for i in range(10):
    exec_cmd("dd if=/dev/zero of=file" + str(i) + " bs=1k count=1 2>/dev/null") # Small size does NOT effects path lookup
bin_name = "parallel_dir"

if not os.path.isfile(bin_name):
    exec_cmd("make " + bin_name + " 1>/dev/null")

accesses = 0
usr = 0.0
sys = 0.0

test = 11

# Output format of parallel_dir(resemble with 'ebizzy'`s)
# <accesses> accesses/s
# real    <time> s
# usr     <time> s
# sys     <time> s
for i in range (test) :
    result = parallel_dir()
    if i == 0: continue # first iteration is just warm up!
    output, err = result.communicate()
    field = str(output).split()
    accesses += int(field[0])
    real = float(field[3])
    usr += float(field[6])
    sys += float(field[9])

accesses /= (test - 1)
usr /= (test - 1)
sys /= (test - 1)

uname_result = exec_cmd("uname -r")
row, err =uname_result.communicate()
col_list= ["Accesses/s", "Real(s)", "User(s)", "System(s)"]
data = numpy.array([int(accesses), real, usr, sys])
row_format = "{:>15}" * (len(col_list) + 1)

print row_format.format("", *col_list)
print row_format.format(row, *data)

# Clean up temporary files
exec_cmd("make clean")
exec_cmd("rm file*")
