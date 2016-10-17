#!/bin/bash

# Generate Random Files
# generate file of various sizes with random contents for test copy offloading
# Test based on (https://lwn.net/Articles/658718/)
# How to?: by util 'dd'(http://superuser.com/questions/470949/how-do-i-create-a-1gb-random-file-in-linux)

RND=/dev/urandom
CP=cp
CFR=src/copy_file_range
#TMP=tmp/
TIME=/usr/bin/time
DIR=logs/
#`git rev-parse --show-toplevel`/test/copy_file_range/

#cd src
#sudo make
#if [ -z "`cat ~/.bashrc | grep alias\ time=\'/usr/bin/time\'`" ]; then
#    echo alias\ time=\'/usr/bin/time\' >> ~/.bashrc
#fi
# Genearate files for test
for i in {1..10}; do
    if [ $i -eq 7 ]; then
        i=10
    fi
    size=`expr "$i" "*" "512"`
    origin=${DIR}origin_$size.txt
    copy=${DIR}copy_$size.txt
    dd if=$RND of=$origin count=$i 2>/dev/null
    #strace cp $origin $copy > $log 2>&1
done

#echo "Generated origin, copy and log files for test,'copy_file_range()'"
rm logs/log

for j in {1..10000}; do
    for i in {1..10}; do
        if [ $i -eq 7 ]; then
            i=10
        fi
        size=`expr "$i" "*" "512"`
        origin=${DIR}origin_$size.txt
        copy=${DIR}copy_$size.txt
        ( $TIME -f "%C\tuser: %U\tsystem: %S\tcpu: %P\ttotal: %e" $CP $origin $copy ) 2>&1 | awk '{print $2}'
        ( $TIME -f "%C\tuser: %U\tsystem: %S\tcpu: %P\ttotal: %e" $CFR $origin $copy ) 2>>logs/log
    done
    break
done

