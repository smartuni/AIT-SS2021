/*
 * Copyright (C) 2017 Freie Universität Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

/**
 * @ingroup     examples
 * @{
 *
 * @file
 * @brief       Example for demonstrating SAUL and the SAUL registry
 *
 * @author      Hauke Petersen <hauke.petersen@fu-berlin.de>
 *
 * @}
 */

#include <stdio.h>

#include "shell.h"
#include "saul_reg.h"


int echo(int argc, char **argv)
{
    /* ... */
    (void)argc;
    (void)argv;

    puts("hello");

    return 0;
}

int read_sensor(int argc, char **argv)
{
    /* ... */
    (void)argc;
    (void)argv;

    int sensor_id = 5;
    saul_reg_t *dev;
    dev = saul_reg_find_nth(sensor_id);
  
    if (dev == NULL) {
        puts("error: undefined device id given");
    }
  
    phydat_t res;
    
    int dim = saul_reg_read(dev, &res);
  
    int16_t val = res.val[0];
    uint8_t unit = res.unit;
    int8_t scale = res.scale;
  
    printf("Value: %d, Unit: %d, Scale: %d, Dim: %d\n", val, unit, scale, dim);
  
    /* print results */
    //printf("Reading from #%i (%s|%s)\n", sensor_id, _devname(dev),
    //       saul_class_to_str(dev->driver->type));
    phydat_dump(&res, dim);

    return 0;
}

static const shell_command_t commands[] = {
    { "echo", "my echo function", echo },
    { "read_sensor", "my sensor function", read_sensor},
    { NULL, NULL, NULL }
};

int main(void)
{
    puts("Welcome to RIOT!\n");
    puts("Type `help` for help, type `saul` to see all SAUL devices\n");
  
    char line_buf[SHELL_DEFAULT_BUFSIZE];
    shell_run(commands, line_buf, SHELL_DEFAULT_BUFSIZE);
    return 0;
}
