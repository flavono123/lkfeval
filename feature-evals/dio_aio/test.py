#!/usr/bin/env python2
#-*-coding:utf-8-*-

import sys
import os
import subprocess # still not adjusted
import json

def exec_cmd(cmd):
    return subprocess.Popen(cmd,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

def fio(test):
    exec_cmd("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    exec_cmd("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    exec_cmd("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    cmd = "sudo fio --directory=/mnt/loop --direct=1 --bs=4k --size=1G --numjobs=4 --time_based --runtime=60 --group_reporting --norandommap --minimal --name dio_aio --rw=" + test
    return exec_cmd(cmd)
    #proc = exec_cmd(cmd)
    #return get_iops(proc.stdout.read(), test)

def get_iops(output, rw):
    field = str(output).split(';')
    if (rw == "read" or rw == "randread"):
        return int(field[7])
    elif (rw == "write" or rw == "randwrite"):
        return int(field[48])

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

def buffercache():
    proc = exec_cmd("free -h")
    output = proc.stdout.read()
    field = output.split() # field of 11 index is valu of buff/cache
    return caltobyte(field[11])

# System set; drop page, cache and , and set the ratio of write back max as possible
exec_cmd("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
exec_cmd("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")

rand_read_iops = 0
rand_read_buffercache = 0.0
read_iops = 0
read_buffercache = 0.0
rand_write_iops = 0
rand_write_buffercache = 0.0
write_iops = 0
write_buffercache =0.0

test = 6

# TODO; method, Popen does not neeed the argument, shell=True, if the scripts running on root
# Test start
for i in range (test) :
    proc = fio("randread")
    rand_read_iops += get_iops(proc.stdout.read(), "randread")
    rand_read_buffercache += buffercache()

    proc = fio("read")
    read_iops += get_iops(proc.stdout.read(), "read")
    read_buffercache += buffercache()

    proc = fio("randwrite")
    rand_write_iops += get_iops(proc.stdout.read(), "randwrite")
    rand_write_buffercache += buffercache()

    proc = fio("write")
    write_iops += get_iops(proc.stdout.read(), "write")
    write_buffercache += buffercache()

print rand_read_iops / (test - 1)
print read_iops / (test - 1)
print rand_write_iops / (test - 1)
print write_iops / (test - 1)

print sizeof_fmt(rand_read_buffercache)
print sizeof_fmt(read_buffercache)
print sizeof_fmt(rand_write_buffercache)
print sizeof_fmt(write_buffercache)
"""
free_records = 0
free_usr = 0.0
free_sys = 0.0

dontneed_records = 0
dontneed_usr = 0.0
dontneed_sys = 0.0

f_time = open (fn_time)

# Discard
for i in range(8):
    f_time.readline()

while 1:
    line = f_time.readline()
    if not line: break
    result = line.split("_")
    value = result[2].split()
    if (result[1] == "FREE"):
        if (value[0] == "records/s"):
            free_records += int(value[1])
        elif (value[0] == "user"):
            free_usr += float(value[1])
        elif (value[0] == "sys"):
            free_sys += float(value[1])
    elif (result[1] == "DONTNEED"):
        if (value[0] == "records/s"):
            dontneed_records += int(value[1])
        elif (value[0] == "user"):
            dontneed_usr += float(value[1])
        elif (value[0] == "sys"):
            dontneed_sys += float(value[1])

f_time.close()
subprocess.Popen("rm " + fn_time)

free_records /= (test - 1)
free_usr /= (test - 1)
free_sys /= (test - 1)

dontneed_records /= (test - 1)
dontneed_usr /= (test - 1)
dontneed_sys /= (test - 1)

subprocess.Popen("echo \"MADV_FREE_records\t%d\"" % free_records)
subprocess.Popen("echo \"MADV_FREE_usr\t%5.2f\"" % free_usr)
subprocess.Popen("echo \"MADV_FREE_sys\t%5.2f\"" % free_sys)

subprocess.Popen("echo \"MADV_DONTNEED_records\t%d\"" % dontneed_records)
subprocess.Popen("echo \"MADV_DONTNEED_usr\t%5.2f\"" % dontneed_usr)
subprocess.Popen("echo \"MADV_DONTNEED_sys\t%5.2f\"" % dontneed_sys)

"""
