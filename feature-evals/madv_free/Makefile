CFLAGS += -pthread
LDFLAGS += -pthread -ljemalloc

SRCS := ebizzy_madv.c

default:$(SRCS:.c=.o)

clean:
	$(RM) $(SRCS:.c=.o) $(SRCS:.c=)
