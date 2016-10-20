#define _GNU_SOURCE
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>
#include <sys/mman.h>
#include <time.h>
#include <stdint.h>

#define MMAP_SIZE 139264 
#define BUF_SIZE  128 * 1024

#define MIN(A, B) \
       ({ __typeof__ (A) _A = (A); \
        __typeof__ (B) _B = (B); \
        _A < _B ? _A : _B; })

struct timespec 
diff(struct timespec start, struct timespec end) 
{
    struct timespec tmp;
    if ((end.tv_nsec - start.tv_nsec) < 0) {
        tmp.tv_sec = end.tv_sec - start.tv_sec - 1;
        tmp.tv_nsec = 1000000000 + end.tv_nsec - start.tv_nsec;
    } else {
        tmp.tv_sec = end.tv_sec - start.tv_sec;
        tmp.tv_nsec = end.tv_nsec - start.tv_nsec;
    }
    return tmp;
}

int
main(int argc, char **argv)
{
    int fd_in, fd_out;
    struct stat stat;
    loff_t len, ret;
    void *buf;
    struct timespec start_ts, end_ts;
    
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <source> <destination>\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    
    fd_in = open(argv[1], O_RDONLY);
    if (fd_in == -1) {
        perror("open (argv[1])");
        exit(EXIT_FAILURE);
    }
    if (fstat(fd_in, &stat) == -1) {
        perror("fstat");
        exit(EXIT_FAILURE);
    }
    
    fd_out = open(argv[2], O_CREAT | O_WRONLY | O_TRUNC, 0644);
    if (fd_out == -1) {
        perror("open (argv[2])");
        exit(EXIT_FAILURE);
    }
    
    len = stat.st_size;

    buf = mmap(NULL, MMAP_SIZE, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, - 1, 0);
    
    if (clock_gettime(CLOCK_MONOTONIC, &start_ts) == -1) {
        perror("clock_gettime");
        exit(EXIT_FAILURE);
    }

    do {
        ret = read(fd_in, buf, MIN(UINTMAX_MAX, BUF_SIZE));
        if (ret == -1) {
            perror("read");
            exit(EXIT_FAILURE);
        }
        ret = write(fd_out, buf, ret);
        if (ret == -1) {
            perror("write");
            exit(EXIT_FAILURE);
        }
        len -= ret;
    } while (len > 0);
   
    if (clock_gettime(CLOCK_MONOTONIC, &end_ts) == -1) {
        perror("clock_gettime");
        exit(EXIT_FAILURE);
    }

    printf("%lu.%03lus\n", diff(start_ts, end_ts).tv_sec, diff(start_ts, end_ts).tv_nsec / 1000000);

    close(fd_in);
    close(fd_out);
    exit(EXIT_SUCCESS);
}
