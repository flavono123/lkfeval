#!/usr/bin/env python2
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
size = 1073741824
count = int (size / 1024)

fn_origin = "origin.txt"
fn_copy = "copy.txt"
fn_cfr = "cfr.txt"
fn_time = "time.log"
fn_result = "copy_file_range_.log"

os.system ("dd if=/dev/zero of=" + fn_origin + " bs=1k count=" + str(count) + " 2>/dev/null")

# System set
os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
os.system ("sudo sh -c \"/bin/echo 90 > /proc/sys/vm/dirty_ratio\"")

test = 11
for i in range (test) :
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")

    os.system ("echo cp >> " + fn_time + " 2>&1")
    os.system ("./cp_time " + fn_origin + " " + fn_copy + " >> " + fn_time + " 2>&1")
    os.system ("diff " + fn_origin + " " + fn_copy)
    os.system ("rm " + fn_copy)

    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
    os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")

    os.system ("echo copy_file_range >> " + fn_time + " 2>&1")
    os.system ("./copy_file_range_time " + fn_origin + " " + fn_cfr + " >> " + fn_time + " 2>&1")
    os.system ("diff " + fn_origin + " " + fn_cfr)
    os.system ("rm " + fn_cfr)

    if i == 0 :
        print ("CPU warming up!")
    else :
        print ("Testing copy " + str(size / 1024 / 1024 / 1024) + "GB file (%d/10)" % i )
'''
    os.system ("( /usr/bin/time -f \"%C\t%U\t%S\t%P\t%e\" cp " + fn_origin + " " + fn_copy + " ) 2>>" + fn_time)
    os.system ("( /usr/bin/time -f \"%C\t%U\t%S\t%P\t%e\" ./copy_file_range " + fn_origin + " " + fn_cfr + " ) 2>>" + fn_time)
    os.system ("rm " + fn_copy)
    os.system ("rm " + fn_cfr)

os.system ("rm " + fn_origin)
'''
f_time = open (fn_time)

'''
user_cp = 0.0
sys_cp = 0.0
cpu_cp = 0.0
total_cp = 0.0

user_cfr = 0.0
sys_cfr = 0.0
cpu_cfr = 0.0
total_cfr = 0.0


os.system ("sudo sh -c \"/bin/echo 3 > /proc/sys/vm/drop_caches\"")
   if (result[0] == "cp") :
        user_cp += float (result[3])
        sys_cp += float (result[4])
        result[5] = result[5].replace("%","")
        if result[5] != "?" :
            cpu_cp += float (result[5])
        total_cp += float (result[6])
    elif (result[0] == "./copy_file_range") :
        user_cfr += float (result[3])
        sys_cfr += float (result[4])
        result[5] = result[5].replace("%","")
        if result[5] != "?" :
            cpu_cfr += float (result[5])
        total_cfr += float (result[6])
'''

f_time.close ()

'''
user_cp /= test
sys_cp /= test
cpu_cp /= test
total_cp /= test

user_cfr /= test
sys_cfr /= test
cpu_cfr /= test
total_cfr /= test

f_result = open (fn_result, "w")
f_result.write ("\tuser\tsys\tcpu\ttotal\n")
f_result.write ("cp\t%.2fs\t%.2fs\t%d%%\t%.3f\n" % (user_cp, sys_cp, cpu_cp, total_cp))
f_result.write ("./copy_file_range\t%.2fs\t%.2fs\t%d%%\t%.3f\n" % (user_cfr, sys_cfr, cpu_cfr, total_cfr))
'''
f_result = open (fn_result, "w")
f_result.close ()
