#!/usr/bin/env python3
#-*-coding:utf-8-*-

import sys
import os
import subprocess # still not adjusted
import json

# Generate random file for given size
'''
if len(sys.argv) != 2 or int (sys.argv[1]) % 512 :
    print ("Usage: test.py <size>, size should be a multiple of 512")
    exit(1)
'''
#stdout, stderr = exec(git rev-parse --show-toplevel)
#TODO get path
#gitroot = str(os.system("git rev-parse --show-toplevel")) + "/"
#print(gitroot)
if not os.path.isfile ("copy_file_range_time") or not os.path.isfile ("cp_time"):
    os.system("make copy_file_range_time cp_time")
size = 1073741824 * 3
count = int (size / 1024)

fn_origin = "origin.txt"
fn_copy = "copy.txt"
fn_cfr = "cfr.txt"
fn_time = "time.log"

os.system ("dd if=/dev/zero of=" + fn_origin + " bs=1k count=" + str(count) + " 2>/dev/null")

# System set
os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
os.system ("sudo sh -c \"/bin/echo 90 > /proc/sys/vm/dirty_ratio\"")

if os.path.isfile(fn_time):
    os.system("rm " + fn_time)

os.system("touch " + fn_time)
os.system("chmod 755 " + fn_time)

test = 11
for i in range (test) :
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")

    os.system ("./cp_time " + fn_origin + " " + fn_copy + " >> " + fn_time + " 2>&1")
    os.system ("diff " + fn_origin + " " + fn_copy)
    os.system ("rm " + fn_copy)

    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")

    os.system ("./copy_file_range_time " + fn_origin + " " + fn_cfr + " >> " + fn_time + " 2>&1")
    os.system ("diff " + fn_origin + " " + fn_cfr)
    os.system ("rm " + fn_cfr)

os.system("rm " + fn_origin)

f_time = open(fn_time, "r+")
os.system("rm " + fn_time)

avg_cp = 0.0
avg_cfr = 0.0

while 1:
    line = f_time.readline()
    if not line: break
    result = line.split()
    if (result[0] == "cp"): avg_cp += float(result[1])
    elif (result[0] == "cfr"): avg_cfr += float(result[1])

f_time.close ()
os.system("rm ")

avg_cp /= (test - 1)
avg_cfr /= (test - 1)

os.system("echo \"cp\t%5.3f\"" % avg_cp)
os.system("echo \"copy_file_range\t%5.3f\"" % avg_cfr)

