#!/bin/sh

GRUB_FILE=/etc/default/grub
BOOT_IMAGE="\"1>Ubuntu, with Linux "$1'\"'

if [ $# -ne 1 ]
then
    echo chk: missing kernel image operand to boot.
    exit
fi

prev_image=`grep -w "^GRUB_DEFAULT" $GRUB_FILE | awk -F'=' '{print $2}'`
echo "Previous default booting kernel image was $prev_image"

# Backup the previous grub file.
cp $GRUB_FILE $GRUB_FILE.old

# Modify and adjust the new kernel image as default booting image.
sed -i "s/GRUB_DEFAULT=$prev_image/GRUB_DEFAULT=$BOOT_IMAGE/g" $GRUB_FILE
update-grub
echo "Default booting kernel image is changed to $BOOT_IMAGE"
#echo "System reboots now!"
#reboot
