#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <dirent.h>
#include <pthread.h>
#include <time.h>
#include <sys/time.h>
#include <sys/resource.h>

#define tv_to_sec(tv) tv.tv_sec + tv.tv_usec/1e6

static unsigned int threads = 1000;
static unsigned int seconds = 10;
static time_t start_time;
static volatile int threads_go;
static unsigned int access_cnt;

/*
 * This fucntion is the meat of the program; the rest is just support.
 *
 * In this function, we access the files and directories, also this source
 * is included, on current directoy('.') as 'dirent' through 'readdir()'.
 * 
 */

static struct timeval difftimeval(struct timeval *end, struct timeval *start)
{
    struct timeval diff;
    diff.tv_sec = end->tv_sec - start->tv_sec;
    diff.tv_usec = end->tv_usec - start->tv_usec;

    return diff;
}

static unsigned int access_dir()
{
    DIR *dir_info;
    struct dirent *dir_entry;
    int i;

    for (i = 0; threads_go == 1;) {
        dir_info = opendir(".");
        if (dir_info != NULL) {
            while (dir_entry =readdir(dir_info)) i++;
            closedir(dir_info);
        }
    }

    return (i);
}

static void * thread_run(void *arg)
{
    /* Wait for the start signal */
    while (threads_go == 0);

    access_cnt += access_dir();

    return NULL;
}

static void start_threads(void)
{
    pthread_t thread_array[threads];
    double elapsed;
    unsigned int i;
    struct rusage start_ru, end_ru;
    struct timeval usr_time, sys_time;
    int err;

    for (i = 0; i < threads; i++) {
        err = pthread_create(&thread_array[i], NULL, thread_run, NULL);
        if (err) {
            printf("Error creating thread %d\n", i);
            exit(1);
        }
    }
    
    /* 
     * Begin accounting - this is when we actually do the things
     * we want to measure.
     */

    getrusage(RUSAGE_SELF, &start_ru);
    start_time = time(NULL);
    threads_go = 1;
    sleep(seconds);
    threads_go = 0;
    elapsed = difftime(time(NULL), start_time);
    getrusage(RUSAGE_SELF, &end_ru);

    for (i = 0; i < threads; i++) {
        err = pthread_join(thread_array[i], NULL);
        if (err) {
            printf("Error joining thread %d\n", i);
            exit(1);
        }
    }
    
    usr_time = difftimeval(&end_ru.ru_utime, &start_ru.ru_utime);
    sys_time = difftimeval(&end_ru.ru_stime, &start_ru.ru_stime);


    printf("%u\t access/s\n", (unsigned int) (((double)access_cnt)/elapsed));
    printf("real\t%5.2f s\n", elapsed);
    //printf("user %5.2f s\n", usr_time.tv_sec + usr_time.tv_usec/1e6);
    printf("user\t%5.2f s\n", tv_to_sec(usr_time));
    printf("sys\t%5.2f s\n", tv_to_sec(sys_time));
}

int main()
{
    start_threads();

    return 0;
}
