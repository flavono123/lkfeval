#!/bin/bash

# Generate Random Files
# generate file of various sizes with random contents for test copy offloading
# Test based on (https://lwn.net/Articles/658718/)
# How to?: by util 'dd'(http://superuser.com/questions/470949/how-do-i-create-a-1gb-random-file-in-linux)

RND=/dev/urandom
DIR=`git rev-parse --show-toplevel`/test/copy_file_range/

for ((i=1;i<11;i++)); do
    if [ $i -eq 7 ]; then
        i=10
    fi
    size=`expr "$i" "*" "512"`
    origin=$DIR"origin_$size.txt"
    copy=$DIR"copy_$size.txt"
    log=$DIR"strace_$size.log"
    dd if=$RND of=$origin count=$i 2>/dev/null
    strace cp $origin $copy > $log 2>&1
done

echo "Generated origin, copy and log files for test,'copy_file_range()'"
