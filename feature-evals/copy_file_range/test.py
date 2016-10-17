#!/usr/bin/python3
#-*-coding:utf-8-*-

import sys
import os
import json

# Generate random file for given size
if len(sys.argv) != 2 or int (sys.argv[1]) % 512 :
    print ("Usage: test.py <size>, size should be a multiple of 512")
    exit(1)

if not os.path.isfile ("copy_file_range") :
    os.chdir ("src")
    os.system ("sudo make test")
    os.system ("mv copy_file_range ../")
    os.chdir ("..")
size = int (sys.argv[1])
count = int (size / 512)

fn_origin = "logs/origin_" + str (size) + ".txt"
fn_copy = "logs/copy_" + str (size) + ".txt"
fn_cfr = "logs/cfr_" + str (size) + ".txt"
fn_time = "logs/time_" + str (size) + ".log"
fn_result = "logs/result_" + str (size) + ".log"

os.system ("dd if=/dev/urandom of=" + fn_origin + " count=" + str(count) + " 2>/dev/null")

test = 1000
for i in range (test) :
    os.system ("( /usr/bin/time -f \"%C\t%U\t%S\t%P\t%e\" cp " + fn_origin + " " + fn_copy + " ) 2>>" + fn_time)
    os.system ("( /usr/bin/time -f \"%C\t%U\t%S\t%P\t%e\" ./copy_file_range " + fn_origin + " " + fn_cfr + " ) 2>>" + fn_time)
    os.system ("rm " + fn_copy)
    os.system ("rm " + fn_cfr)

os.system ("rm " + fn_origin)

f_time = open (fn_time)

user_cp = 0.0
sys_cp = 0.0
cpu_cp = 0.0
total_cp = 0.0

user_cfr = 0.0
sys_cfr = 0.0
cpu_cfr = 0.0
total_cfr = 0.0

line = f_time.readline ()
while line :
    line = line.replace ("\n","")
    result = line.split ()
    line = f_time.readline ()
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

f_time.close ()

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

