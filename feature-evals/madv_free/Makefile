#CFLAGS += -pg
LDFLAGS += -lpthread -ljemalloc

SRCS := ebizzy_madv.c

default:$(SRCS:.c=.o)

clean:
	$(RM) $(SRCS:.c=.o) $(SRCS:.c=)
