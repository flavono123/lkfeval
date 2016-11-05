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

for i in range (test) :
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")

    os.system ("./ebizzy_madv -S 10 -n 512 -f >> " + fn_time + " 2>&1")

    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")

    os.system ("./ebizzy_madv -S 10 -n 512>> " + fn_time + " 2>&1")

#f_time = open (fn_time)

