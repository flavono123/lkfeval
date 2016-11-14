#!/usr/bin/env python2
#-*-coding:utf-8-*-

import sys
import os
import subprocess # still not adjusted
import json

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
f_time = open (fn_time)
f_time.close ()

