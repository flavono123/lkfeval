#include <linux/module.h> // module_init(), module_exit()
#include <linux/highmem.h> 
#include <asm/unistd.h>

#define __NR_copy_file_range 326

void **syscall_table = (void**)SYSCALL_TABLE;

/* Make the page writable */
void make_rw(void *address) {
    unsigned int level;
    pte_t *pte = lookup_address((unsigned long)address, &level);
    if (pte->pte &~ _PAGE_RW)
        pte->pte |= _PAGE_RW;
}

/* Make page write protected */
void make_ro(void *address) {
    unsigned int level;
    pte_t *pte = lookup_address((unsigned long)address, &level);
    pte->pte = pte->pte &~ _PAGE_RW;
}

int syscall_init(void) {
    make_rw(syscall_table);
    return 0;
}

void syscall_exit(void) {
    make_ro(syscall_table);
}

module_init(syscall_init);
module_exit(syscall_exit);
MODULE_LICENSE("GPL");
