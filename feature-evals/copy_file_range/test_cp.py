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
    exec_cmd("echo 3 > /proc/sys/vm/drop_caches")
    exec_cmd("echo 3 > /proc/sys/vm/drop_caches")
    exec_cmd("echo 3 > /proc/sys/vm/drop_caches")
    cmd = set_copy_cmd(test)
    result = exec_cmd(cmd)
    return float(result.stdout.read().strip())


# Generate random file for given size
if not os.path.isfile ("cp_time"):
    os.system("make cp_time 2>/dev/null") # Meaningless output go to trash
size = 1073741824 * 3 # Guest Env. 4GB memory
count = int (size / 1024)

fn_origin = "origin.txt"
fn_copy = "copy.txt"
fn_cfr = "cfr.txt"

exec_cmd("dd if=/dev/zero of=" + fn_origin + " bs=1k count=" + str(count) + " 2>/dev/null")

# System set
exec_cmd("echo 3 > /proc/sys/vm/drop_caches")
exec_cmd("echo 90 > /proc/sys/vm/dirty_ratio")

avg_cp = 0.0

test = 11

for i in range (test) :
    avg_cp += copy_test("cp")
    if i == 0: # first iteration is just warming up
        avg_cp = 0.0
    exec_cmd("rm " + fn_copy)

exec_cmd("make clean")
exec_cmd("rm " + fn_origin)

print avg_cp / (test - 1)
