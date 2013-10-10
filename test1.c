#include <stdio.h>
#include <string.h>
#include "magic.h"

//gcc -L/opt/local/lib/ -o 1 test1.c -lmagic

int main(int argc, char **argv) {
    char * tmp="Hello World\n";
    magic_t myt = magic_open(MAGIC_CONTINUE|MAGIC_ERROR/*|MAGIC_DEBUG*/|MAGIC_MIME);
    magic_load(myt,NULL);
    
    if (argc > 1)
    {
        printf("magic output: '%s'\n",magic_file(myt,argv[1]));
    }
    else
    {
        printf("magic output: '%s'\n",magic_buffer(myt,tmp,strlen(tmp)));

    }
    magic_close(myt);
    return 0;
}