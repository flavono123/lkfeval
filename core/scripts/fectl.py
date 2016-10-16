#!/usr/bin/python
#-*-coding:utf-8-*-

import sys
import os
import json


def print_help():
    print("print_help")

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def shell_command(command, error_str='', print_on_error=True, exit_on_error=True) :
    ret = os.system(command)
    if ret :  
        if print_on_error :
            if error_str :
                eprint(error_str)
            else :  
                eprint("failed : "+command)
        if exit_on_error :
            exit(1)
    return ret  

def add_feature(features, fname):
	eval_script = input('feature evalustaion script : ')
	img_cnt = int(input('the number of kernel images : '))
	imgs = []
	for i in range(img_cnt) :
		img = dict()
		img['version'] = input('image[%d] : kerenl version : ' % i)
		img['config'] = dict()
		print('image[%d] : config info (ctrl+D to finish')
		while True :
			try:
				config_name = input('image [%d] : kernel config[%d] name : ' % j) 
				config_value = input('image [%d] : kernel config[%d] value : ' % j) 
				img[config_name] = config_value
			except EOFError:
				break
		imgs.append(img)
	feature = dict()
	feature['evaluation_script'] = eval_script
	feature['image_cnt'] = img_cnt
	feature['images'] = imgs
			
				

def del_featrue(features, fname):
	pass

def show_feature(features, fname):
	pass

def list_feature(features, opt):
	opts = ['--detail']
	if opt not in opts
		raise Exception('invalid option')

current_module = sys.modules[__name__]
command = argv[1]

if not hasattr(current_module, command+'_feature' :
	eprint("invalid command : %s" % command)
	print_help()
	exit(1)

feconf_file_name = 'feature_eval.conf'
feconf_file = open(feconf_file_name, 'r')
features = json.load(feature_eval_conf)
feconf_file.close()

command_handler = getattr(current_moduel, command+'_feature')
commadn_handler(argv[2])

feconf_file = open(feconf_file_name, 'w')
json.dump(features, feconf_file)
feconf_file.close()
