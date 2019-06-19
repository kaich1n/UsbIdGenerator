#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "usb_ids.h"

#define ARRAY_SIZE(a) (sizeof(a) / sizeof(a[0]))

int main(int argc, char **argv)
{
    int i, v;

    if (argc >= 2)
        v = (int)strtol(argv[1], NULL, 16);
    else
        v = 0;

    unsigned int now = time(NULL);
    for (i = 0; i < ARRAY_SIZE(usb_device_ids); i++) {
        static int done = 0;
        if (v == usb_device_ids[i].vid) {
            if (!done++)
                printf("0x%04x %s\n", usb_device_ids[i].vid, usb_device_ids[i].v_name);
            printf("\t0x%04x %s\n", usb_device_ids[i].did, usb_device_ids[i].d_name);
        }
    }

    printf("%d - %u\n", i, (unsigned int)time(NULL) - now);
    return 0;
}
