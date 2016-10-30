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
REQ_ARG_CNT=3 #TODO -v, -f|-c 로 체크해야함. f나 c가 선택이기떄문에 카운트로 검사하면 안댐.
version=''
feature=''
path=''
config=''
extraversion=''
eval_script=''

while [ "$1" != "" ]; do
	case $1 in
		"-v")
			shift
			version=$1  
			required_arg_cnt=`expr $required_arg_cnt "+" "1"`
			;;
		"-f")
			shift
			feature=$1
			required_arg_cnt=`expr $required_arg_cnt "+" "1"`
			;;
		"-c")
			shift
			config=$1
			required_arg_cnt=`expr $required_arg_cnt "+" "1"`
			;;
		"-s")
			shift
			eval_script=$1
			required_arg_cnt=`expr $required_arg_cnt "+" "1"`
			;;
		"-e")
			shift
			extraversion=$1
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

if [ -z $extraversion ]; then
	extraversion="-$feature"
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

#echo "Host's shared folder(  which data and source is read from, write to) : "
#read host_shared_folder

shell_dir=$(dirname $0)
cd ${shell_dir}
cd ..
cd ..
host_shared_folder=`pwd` #root dir

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
compile_script=$guest_shared_dir_linux/core/scripts/kmake.py
#TODO have to change to youngmin's script' args (version, config?)
compile_script_args="-v $version -c $config -e $extraversion"


#maybe root
#TODO root as default
#echo "guest_user(maybe root) : "
#read guest_user
#echo "guest_passwd : "
#read guest_passwd

guest_user='root'
guest_passwd='root'


echo "kernel making..."
#
if ! vmrun -gu $guest_user -gp $guest_passwd runProgramInGuest \
	"$virtual_machine" "$compile_script" $compile_script_args; then
	echo "failed : $compile_script $compile_script_args compile script execution."
	exit 72
fi

echo "kernel update..."

update_script=$guest_shared_dir_linux/core/scripts/kupdate.sh
update_script_args="${version}-${extraversion}"


if ! vmrun -gu $guest_user -gp $guest_passwd runProgramInGuest \
	"$virtual_machine" "$update_script" $update_script_args; then
	echo "failed : $compile_script $compile_script_args compile script execution."
fi

echo "reboot vm..."
vmrun reset "$virtual_machine"

echo "evaluation start : $eval_script"
#feature evaluation (maybe in shared folder) TODO
feature_eval_script="$guest_shared_dir_linux/feature-evals/$eval_script"
#feature_eval_script_args="$guest_shared_dir_linux/feature_evaluation.test"

#TODO kfeature_eval에서 각 피쳐 스크립트를 실행 시킨 결과를 logs폴더로 "특정 규칙의 이름"으로 리다이렉션 시켜야한다.
if ! vmrun -gu $guest_user -gp $guest_passwd runProgramInGuest \
	"$virtual_machine" "$feature_eval_script"; then
	echo "failed : feature evaluation script execution."
	exit 73
fi

#clean
vmrun removeSharedFolder "$virtual_machine" "$shared_name" 1>/dev/null 2>/dev/null 


echo "feature evaluatoin finished"
#cat "$host_shared_folder/feature_evaluation.test"
echo done
