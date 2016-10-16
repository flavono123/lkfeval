#!/usr/bin/python3
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

def add_feature(features, argv):
	fname = argv[2]
	eval_script = input('feature evalustaion script : ') #TODO check if it exists
	img_cnt = int(input('the number of kernel images : ')) 
	imgs = []
	for i in range(img_cnt) :
		img = dict()
		img['version'] = input('image[%d] : kerenl version : ' % i)
		img['config'] = dict()
		print('image[%d] : config info (ctrl+D to finish)' % i)
		j=0
		while True :
			try:
				config_name = input('image [%d] : kernel config[%d] name : ' % (i, j)) 
				config_value = input('image [%d] : kernel config[%d] value : ' % (i, j)) 
				img[config_name] = config_value
			except EOFError:
				print('')
				break
			j += 1
		imgs.append(img)
	feature = dict()
	feature['evaluation_script'] = eval_script
	feature['image_cnt'] = img_cnt
	feature['images'] = imgs
	features[fname] = feature
				

def del_featrue(features, argv):
	pass

def show_feature(features, argv):
	pass

def list_feature(features, argv):
	opts = ['--detail', '--default']
	opt = '--default'
	if len(argv) > 2:
		opt = argv[2]
	if opt not in opts:
		raise Exception('invalid option')
	

if len(sys.argv) < 2 :
	eprint("missing required arguments")
	print_help()
	exit(1)

current_module = sys.modules[__name__]
command = sys.argv[1]

if not hasattr(current_module, command+'_feature') :
	eprint("invalid command : %s" % command)
	print_help()
	exit(1)

feconf_file_name = 'feature_eval.conf'
feconf_file = ''
features = ''
if os.path.exists(feconf_file_name) :
	feconf_file = open(feconf_file_name, 'r')
	features = json.load(feconf_file)
	feconf_file.close()
else:
	features = json.loads('{}')

command_handler = getattr(current_module, command+'_feature')
command_handler(features, sys.argv)

feconf_file = open(feconf_file_name, 'w+')
json.dump(features, feconf_file)
feconf_file.close()
