#!/usr/bin/env python3
#-*-coding:utf-8-*-

import sys
import os
import json

def script_dir():
    return sys.path[0]

BASE_EVAL_PATH = '/'.join(script_dir().split('/')[:-2])+"/feature-evals"

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
	eval_dir = input('feature evauation dir : ') #상대경로일 경우 feature_eval에서
	if not eval_dir.startswith('/'):
		eval_dir = BASE_EVAL_PATH+'/'+eval_dir
	eval_script_name = input('feature evaluation script name : ') #TODO check if it exists
	print('--before evaluated kernel image--')
	before = dict()
	before['version'] = input('kerenl version : ')
	before['config'] = dict()
	j=0
	print('kernel configs(Crtl+D to stop) : ')
	while True :
		try:
			config_name = input('kernel config[%d] name : ' % j)
			config_value = input('kernel config[%d] value : ' % j)
			before['config'][config_name] = config_value
			j += 1
		except EOFError:
			break

	print('--after evaluated kernel image--')
	after = dict()
	if input('same as before?(y/N)').lower() != 'y':
		after['version'] = input('kerenl version : ')
		after['config'] = dict()
		j=0
		print('kernel configs(Crtl+D to stop) : ')
		while True:
			try:
				config_name = input('kernel config[%d] name : ' % j)
				config_value = input('kernel config[%d] value : ' % j)
				after['config'][config_name] = config_value
				j += 1
			except EOFError:
				break
	else:
		after = before
	feature = dict()
	feature['evaluation_dir'] = eval_dir
	feature['evaluation_script_name'] = eval_script_name
	feature['before'] = before
	feature['after'] = after
	features[fname] = feature
				

def del_feature(features, fname):
	del features[fname]

def show_feature(features, fname):
	try:
		feature = features[fname]
	except KeyError:
		eprint('feature not found.')
		exit(1)
	print('\tfeature evaluation script dir : '+feature['evaluation_dir'])
	print('\tfeature evaluation script name : '+feature['evaluation_script_name'])

	print('\tbefore : ')
	before = feature['before']
	after = feature['after']
	print('\t\tkernel versoin : %s' % before['version'])
	print('\t\tkernel configs : ')
	f_configs = before['config']
	for k,v in f_configs.items():
		print('\t\t '+k+'='+str(v))
	print('\tafter : ')
	print('\t\tkernel versoin : %s' % after['version'])
	print('\t\tkernel configs : ')
	f_configs = after['config']
	for k, v in f_configs.items():
		print('\t\t ' + k + '=' + str(v))

def list_feature(features, opt = '--default'):
	opts = ['--details', '--default']
	if opt not in opts:
		raise Exception('invalid option')
	if opt == '--default':
		for fname in features.keys():
			print(fname)
	elif opt == '--details':
		for fname in features.keys():
			show_feature(features, fname)

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
if len(sys.argv) > 2:
	command_handler(features, sys.argv[2])
else:
	command_handler(features)

feconf_file = open(feconf_file_name, 'w+')
json.dump(features, feconf_file)
feconf_file.close()

print('done')
