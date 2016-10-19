CFLAGS += -pg
LDFLAGS += -lrt

SRCS := copy_file_range_time.c cp_time.c

test:$(SRCS:.c=)
	./test.py

default:$(SRCS:.c=.o)
