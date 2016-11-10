#!/usr/bin/env python2
#-*-coding:utf-8-*-

import sys
import os
import subprocess # still not adjusted
import numpy
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

def sizeof_fmt(knum):
    for unit in ['K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(knum) < 1024.0:
            return "%3.1f%s" % (knum, unit)
        knum /= 1024.0

def buffercache():
    proc = exec_cmd("cat /proc/meminfo")
    output = proc.stdout.read()
    field = output.split()
    return float(field[10]), float(field[13])

# System set; drop page, cache and , and set the ratio of write back max as possible
exec_cmd("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
exec_cmd("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")

rand_read_iops = 0
rand_read_buffer = 0.0
rand_read_cache = 0.0
read_iops = 0
read_buffer = 0.0
read_cache = 0.0
rand_write_iops = 0
rand_write_buffer = 0.0
rand_write_cache = 0.0
write_iops = 0
write_buffer = 0.0
write_cache =0.0

test = 2

# TODO; method, Popen does not neeed the argument, shell=True, if the scripts running on root
# Test start
for i in range (test) :
    tmp_buffer = 0.0
    tmp_cache = 0.0
    proc = fio("randread")
    if i == 0: continue
    rand_read_iops += get_iops(proc.stdout.read(), "randread")
    tmp_buffer, tmp_cache = buffercache()
    rand_read_buffer += tmp_buffer
    rand_read_cache += tmp_cache

    proc = fio("read")
    read_iops += get_iops(proc.stdout.read(), "read")
    tmp_buffer, tmp_cache = buffercache()
    read_buffer += tmp_buffer
    read_cache += tmp_cache


    proc = fio("randwrite")
    rand_write_iops += get_iops(proc.stdout.read(), "randwrite")
    tmp_buffer, tmp_cache = buffercache()
    rand_write_buffer += tmp_buffer
    rand_write_cache += tmp_cache

    proc = fio("write")
    write_iops += get_iops(proc.stdout.read(), "write")
    tmp_buffer, tmp_cache = buffercache()
    write_buffer += tmp_buffer
    write_cache += tmp_cache

col_list = ["rand_read", "read", "rand_write", "write"]
row_list = ["IOPS", "Buffer", "Cache"]
table_data = numpy.array([[int(rand_read_iops), int(read_iops), int(rand_write_iops), int(write_iops)],
        [sizeof_fmt(rand_read_buffer), sizeof_fmt(read_buffer), sizeof_fmt(rand_write_buffer), sizeof_fmt(write_buffer)],
        [sizeof_fmt(rand_read_cache), sizeof_fmt(read_cache), sizeof_fmt(rand_write_cache), sizeof_fmt(write_cache)]])
row_format = "{:>10}" * (len(col_list) + 1)
print row_format.format("", *col_list)
for row, data in zip(row_list, table_data):
    print row_format.format(row, *data)
