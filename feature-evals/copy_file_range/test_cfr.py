#!/usr/bin/env python2
#-*-coding:utf-8-*-

import sys
import os
import subprocess

def exec_cmd(cmd):
    return subprocess.Popen(cmd,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

def set_copy_cmd(test):
    src = fn_origin
    if test == "cp":
        cmd = "./cp_time "
        dest = fn_copy
    elif test == "copy_file_range":
        cmd = "./copy_file_range "
        dest = fn_cfr
    return cmd + src + " " + dest

def copy_test(test):
    exec_cmd("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    exec_cmd("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    exec_cmd("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    cmd = set_copy_cmd(test)
    return exec_cmd(cmd)


# Generate random file for given size
if not os.path.isfile ("copy_file_range_time"):
    os.system("make copy_file_range_time")
size = 1073741824
count = int (size / 1024)

fn_origin = "origin.txt"
fn_copy = "copy.txt"
fn_cfr = "cfr.txt"

exec_cmd("dd if=/dev/zero of=" + fn_origin + " bs=1k count=" + str(count) + " 2>/dev/null")

# System set
exec_cmd("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
exec_cmd("sudo sh -c \"/bin/echo 90 > /proc/sys/vm/dirty_ratio\"")

avg_copy_file_range = 0.0

test = 11

for i in range (test) :
    avg_copy_file_range = copy_test("copy_file_range")
    exec_cmd("rm " + fn_cfr)

exec_cmd("make clean")

print avg_copy_file_range / (test - 1)