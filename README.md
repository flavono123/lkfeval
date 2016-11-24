# LKFES
Linux Kernel Feature Evaluation System

---
## Overview

 본 프로젝트는 커널에 추가되는 여러 Feature에 대해 일관적이고 일반화된 테스트를 진행할 수 있도록해준다. 사용자는 테스트하고 싶은 환경을 설정하고, 원하는 피쳐를 선택해 버전과 config를 명시한후, 측정스크립트를 돌림으로써 해당 Feature(fetch)에 대해 파악할 수 있다.  
  또한, 결과를 웹으로 다른 이용자들과 공유할 수 있다.  
[Web-Archive](http://104.199.211.38/report/)


---

## Prerequisite

* **python-related**  
>python3.x  
requests

* **others**
>bash  
vmware  
guest vmx (linux, tested on ubuntu 14.04)  
ssh key (that is registerd to guest)

---
## Note
* guest vm에는 vmwaretools가 설치되어 있어야 한다.
* guest에 등록된 ssh(rsa) key가 필요하다.
* host에 ssh client가 설치되어 있어야 한다.
* 위의 조건들을 갖춘 기본 ubuntu image가 준비중이다.
* core/scripts/defconfig는 가상머신 위에서의 커널 컴파일을 위한 최적화된 kernel config 파일로, 커널 컴파일에 이용된다.


---


## Quick Usage
1. 프로젝트를 clone받거나 download받는다.
2. feature-evals하위에 feature측정을 위한 script를 정의해 넣는다. (명령어 옵션을 통해 경로 수정가능)
3. fectl로 피쳐 측정에 대한 정보를 추가한다.(kernel version, config, script)
4. lkfes를 실행한다.
5. logs하위에 로그를 통해 결과를 확인할 수있으며, web-archive로 공유가 가능하다.

---

## Usage details
* fectl  
    <pre>
  usage: fectl [-h] {add,del,list,show} ...  

  feature evaluation control : edit feature_eval.conf for lkfes

  positional arguments:
      {add,del,list,show}  actions
      add                add new evaluating feature
      del                delete evaluating feature
      list               list evaluating features
      show               show evaluating feature

  optional arguments:
    -h, --help           show this help message and exit
    </pre>

* lkfes
  <pre>
  usage: lkfes [-h] [-cp CONFIG_PATH] vm ssh_key eval_fname

  Linux Kerenl Feature Evaluation System : by referring the config file, proceed
  kernel feature evaluation(compile, run the script, report, ...)

  positional arguments:
    vm                    (.vmx) vmware machine on which the evaluations is
                          executed
    ssh_key               ssh-key to vmware guest(rsa)
    eval_fname            evalution feature name in config file

  optional arguments:
    -h, --help            show this help message and exit
    -cp CONFIG_PATH, --config_path CONFIG_PATH
                          location of config gile. default :
                          (ROOT)/core/sciprts/feature_eval.conf

    </pre>
* kfeature-eval
      <pre>
      usage: kfeature-eval [-h] [-c CONFIG [CONFIG ...]] [-vp VMRUN_PATH]
                           [-e EXTRAVERSION] [-gu GUEST_USER] [-gp GUEST_PASSWD]
                           [-sshp SSH_PORT] [-wd WORKING_DIR] [-sl]
                           vm ssh_key f_name k_version eval_script log_file_name

      feature evaluation tools : make a kernel image and run a feature evaluation
      script

      positional arguments:
        vm                    (.vmx) vmware machine on which the evaluations is
                              executed
        ssh_key               ssh key to connect to geust
        f_name                the name of evaluated feature
        k_version             copliling kerenl image on which evaluation will run
        eval_script           evaluation script
        log_file_name         evaluation log file name

      optional arguments:
        -h, --help            show this help message and exit
        -c CONFIG [CONFIG ...], --config CONFIG [CONFIG ...]
                              configs for kernel compile (CONFIG_*)
        -vp VMRUN_PATH, --vmrun_path VMRUN_PATH
                              vmrun path of vmware
        -e EXTRAVERSION, --extraversion EXTRAVERSION
                              extraversion used kernel compile
        -gu GUEST_USER, --guest_user GUEST_USER
                              guest id on vmware machine
        -gp GUEST_PASSWD, --guest_passwd GUEST_PASSWD
                              geust password on vmware machine
        -sshp SSH_PORT, --ssh_port SSH_PORT
                              ssh port of guest
        -wd WORKING_DIR, --working_dir WORKING_DIR
                              working dir in guest. scripts and logs are maked
                              temporarily on the directory.
        -sl, --spec_log       enable logging the spec of guest.
    </pre>
