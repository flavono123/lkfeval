#define _GNU_SOURCE
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <unistd.h>
#include <sys/mman.h>

#define __NR_copy_file_range 326

#define MMAP_SIZE 139264 
#define BUF_SIZE  131072

static loff_t
copy_file_range(int fd_in, loff_t *off_in, int fd_out, loff_t *off_out, size_t len, unsigned int flags)
{
    return syscall(__NR_copy_file_range, fd_in, off_in, fd_out, off_out, len, flags);
}

int
main(int argc, char **argv)
{
    int fd_in, fd_out;
    struct stat stat;
    loff_t len, ret;
    void *buf;
    
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
    
    len = stat.st_size;
    
    fd_out = open(argv[2], O_CREAT | O_WRONLY | O_TRUNC, 0644);
    if (fd_out == -1) {
        perror("open (argv[2])");
        exit(EXIT_FAILURE);
    }
    
    buf = mmap(NULL, MMAP_SIZE, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, - 1, 0);
    // do time measure for cp
    do {
        ret = read(fd_in, buf, BUF_SIZE);
        if (ret == -1) {
            perror("read");
            exit(EXIT_FAILURE);
        }
        ret = write(fd_out, buf, BUF_SIZE);
        if (ret == -1) {
            perror("write");
            exit(EXIT_FAILURE);
        }
        len -= ret;
    } while (len > 0);
    // done
    len = stat.st_size;
    // do time measure for copy_file_range
/*    do {
        ret = copy_file_range(fd_in, NULL, fd_out, NULL, len, 0);
        if (ret == -1) {
            perror("copy_file_range");
            exit(EXIT_FAILURE);
        }
        len -= ret;
    } while (len > 0);
*/    // done copy_file_range

    close(fd_in);
    close(fd_out);
    exit(EXIT_SUCCESS);
}
