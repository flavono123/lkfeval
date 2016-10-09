#!/bin/sh

PTS=~/phoronix-test-suite/phoronix-test-suite
JTR=~/testutil/john-the-ripper/john-1.8.0/run/john
CONF=/etc/default/cpufrequtils
LOG_FILE=../log/schedutil.log
# Need package 'cpufrequtils'
#!NOTE_ file checking methods
#ret=`dpkg -l | grep cpufrequtils`
#if [ -z ret ]
if [ ! -x /usr/bin/cpufreq-set ] #|| [ ! -f $CONF ]
then
    echo "utility, \"cpufrequtils\, is needed."
    # Install or just exit?
    #apt-get install cpufrequtils
    exit
fi

# Test for existing governor and log to file
echo "# Log the john the ripper blow test with governor start " > $LOG_FILE 
$JTR --test >> $LOG_FILE &2>1

# Change the governor to 'schedutil'
#cpufreq-set -g schedutil
echo "=====================================================================" >> $LOG_FILE
echo "# Log the john the ripper blow test with governor 'schedutil' start " >> $LOG_FILE 
$JTR --test >> $LOG_FILE &2>1
#$PTS benchmark john-the-ripper
# How can I control (put arguments or commands) pts?
# Link with it?
#sed -i 's/GOVERNOR=*/GOVERNOR=schedutil/g'
#$PTS benchmark john-the-ripper


