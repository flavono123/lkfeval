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

# Generate random file for given size
if not os.path.isfile ("copy_file_range_time") or not os.path.isfile ("cp_time"):
    os.system("make copy_file_range_time cp_time")
size = 1073741824
count = int (size / 1024)

fn_origin = "origin.txt"
fn_copy = "copy.txt"
fn_cfr = "cfr.txt"
fn_time = "time.log"
fn_result = "copy_file_range_.log"

exec_cmd("dd if=/dev/zero of=" + fn_origin + " bs=1k count=" + str(count) + " 2>/dev/null")

# System set
exec_cmd("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
exec_cmd("sudo sh -c \"/bin/echo 90 > /proc/sys/vm/dirty_ratio\"")

test = 11
for i in range (test) :
    exec_cmd("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    exec_cmd("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    exec_cmd("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")

    exec_cmd("echo cp >> " + fn_time + " 2>&1")
    exec_cmd("./cp_time " + fn_origin + " " + fn_copy + " >> " + fn_time + " 2>&1")
    exec_cmd("diff " + fn_origin + " " + fn_copy)
    exec_cmd("rm " + fn_copy)

    exec_cmd("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    exec_cmd("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    exec_cmd("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")

    exec_cmd("echo copy_file_range >> " + fn_time + " 2>&1")
    exec_cmd("./copy_file_range_time " + fn_origin + " " + fn_cfr + " >> " + fn_time + " 2>&1")
    exec_cmd("diff " + fn_origin + " " + fn_cfr)
    exec_cmd("rm " + fn_cfr)

    if i == 0 :
        print ("CPU warming up!")
    else :
        print ("Testing copy " + str(size / 1024 / 1024 / 1024) + "GB file (%d/10)" % i )
f_time = open (fn_time)
f_time.close ()

