#!/bin/sh


#args : k, f, l
#k - kernel version, f - feature, l = locatoin of vmrun

print_help(){
	echo "잘못된 아규먼트나 헬프 아규먼트시 프린트할 문장" 
}

check_valid_version(){
	local arg_value=$1
	#version check
	return 0 # TODO current always true 
}

check_valid_feature(){
	local arg_feature=$1
	#version check
	return 0 # TODO current always true
}


required_arg_cnt=0
REQ_ARG_CNT=2
version=''
feature=''
path=''

while [ "$1" != "" ]; do
	case $1 in
		"-k")
			shift
			version=$1  
			(( required_arg_cnt++ ))
			;;
		"-f")
			shift
			feature=$1
			(( required_arg_cnt++ ))
			;;
		"-l")
			shift
			path=$1
			;;
		*)
			shift
			;;
	esac
done 


if [ $required_arg_cnt -lt $REQ_ARG_CNT ]
then
	echo "error : missing required args"
	exit 1
fi

if check_valid_feature $feature; then
	echo "valid feature : $feature"
else
	echo "invalid feature : $feature"
	exit 67
fi

if check_valid_version $version; then
	echo "valid version : $version"
else
	echo "invalid version : $version"
	exit 68
fi

uname=`uname -s 2>/dev/null`
PATH=$PATH:$path
if [ "$uname" = "Darwin" ]; then
	PATH="$PATH:/Applications/VMware Fusion.app/Contents/Library"
elif [ "$uname" = "Linux" ]; then
	PATH="$PATH:/usr/lib/vmware-vix/lib"
fi

echo "environment is configured"
echo "feature : $feature"
echo "version : $version"
echo "path : $path"
echo "PATH : $PATH"

if ! type vmrun > /dev/null; then #does vmrun exist?
	echo "error : vmrun does not exist."
	exit 68
fi

#TODO have to check vmware tools is installed.

echo "Virtual Machine(.vmx) : "
read virtual_machine

if [ ! -f "$virtual_machine" ]; then
	echo "There is no virtual machine"
	exit 69
fi

if ! vmrun start "$virtual_machine"; then
	echo "failed : $virtual_machine booting"
	exit 71
fi

echo "Host's shared folder(  which data and source is read from, write to) : "
read host_shared_folder

if [ ! -d "$host_shared_folder" ]; then
	echo "Ther is no $host_shared_folder"
	exit 70
fi

shared_name="lkes"
guest_shared_dir_linux="/mnt/hgfs/$shared_name"
#TODO multi platform


if ! vmrun enableSharedFolders "$virtual_machine" runtime; then
	echo "failed : vmrun enableSharedFolders"
	exit 71
fi

vmrun removeSharedFolder "$virtual_machine" "$shared_name" 1>/dev/null 2>/dev/null 

#TODO if lkes dir is exits
#TODO if there is already guest_shared_dir(name), it fails.
if ! vmrun addSharedFolder "$virtual_machine" "$shared_name" "$host_shared_folder"; then
	echo "failed : vmrun addSharedFolder"
	exit 71
fi

#TODO have to change to youngmin's script( maybe in shared folder )
compile_script=/bin/vmtest.sh
#TODO have to change to youngmin's script' args (version, config?)
compile_script_args="$guest_shared_dir_linux/compile.test"


#maybe root
#TODO root as default
echo "guest_user(maybe root) : "
read guest_user
echo "guest_passwd : "
read guest_passwd

#
if ! vmrun -gu $guest_user -gp $guest_passwd runProgramInGuest \
	"$virtual_machine" "$compile_script" $compile_script_args; then
	echo "failed : compile script execution."
	exit 72
fi

vmrun reset "$virtual_machine"


#feature evaluation (maybe in shared folder) TODO
feature_eval_script=/bin/vmtest.sh
feature_eval_script_args="$guest_shared_dir_linux/feature_evaluation.test"

if ! vmrun -gu $guest_user -gp $guest_passwd runProgramInGuest \
	"$virtual_machine" "$feature_eval_script" $feature_eval_script_args; then
	echo "failed : feature evaluation script execution."
	exit 73
fi

#clean
vmrun removeSharedFolder "$virtual_machine" "$shared_name" 1>/dev/null 2>/dev/null 

echo "feature evaluatoin finished"
cat "$host_shared_folder/feature_evaluation.test"
echo done

