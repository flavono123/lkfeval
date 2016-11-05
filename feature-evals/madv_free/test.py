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

fn_time = "time.log"

# System set
os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
os.system ("sudo sh -c \"/bin/echo 90 > /proc/sys/vm/dirty_ratio\"")

test = 11

if os.path.isfile(fn_time):
    os.system("rm " + fn_time)

os.system("touch " + fn_time)
os.system("chmod 755 " + fn_time)

for i in range (test) :
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")

    os.system ("./ebizzy_madv -S 10 -n 512 -f >> " + fn_time + " 2>&1")

    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")

    os.system ("./ebizzy_madv -S 10 -n 512>> " + fn_time + " 2>&1")

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

fn_time.close()
os.system("rm " + fn_time)

free_records /= (test - 1)
free_usr /= (test - 1)
free_sys /= (test - 1)

dontneed_records /= (test - 1)
dontneed_usr /= (test - 1)
dontneed_sys /= (test - 1)

os.system("echo \"MADV_FREE_records\t%d\"" % free_records)
os.system("echo \"MADV_FREE_usr\t%5.2f\"" % free_usr)
os.system("echo \"MADV_FREE_sys\t%5.2f\"" % free_sys)

os.system("echo \"MADV_DONTNEED_records\t%d\"" % dontneed_records)
os.system("echo \"MADV_DONTNEED_usr\t%5.2f\"" % dontneed_usr)
os.system("echo \"MADV_DONTNEED_sys\t%5.2f\"" % dontneed_sys)


