SRCS := copy_file_range.c
obj-m := syscall_hooker.o

SYSCALL_ADDRESS = 0x$(subst R sys_call_table,,$(shell grep R\ sys_call_table /boot/System.map-$(shell uname -r)))

CFLAGS_syscall_hooker.o += -DSYSCALL_TABLE=$(SYSCALL_ADDRESS)

KDIR := /lib/modules/$(shell uname -r)/build
PWD := $(shell pwd)

default:
	$(MAKE) -C $(KDIR) SUBDIRS=$(PWD) modules

test: default $(SRCS:.c=)
	sudo insmod syscall_hooker.ko
	./$(SRCS:.c=) test test2
	diff test test2
	sudo rmmod syscall_hooker

$(SRCS:.c=):$(SRCS:.c=.o)

clean:
	$(MAKE) -C $(KDIR) SUBDIRS=$(PWD) clean
	$(RM) -rf copy_file_range.o copy_file_range test test2
