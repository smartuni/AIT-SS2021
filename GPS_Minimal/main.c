/**
 * @{
 *
 * @file
 * @brief       Minimal application for minimal gps captures
 *
 * @author      Mehmet Cakir <mehmet.cakir@haw-hamburg.de>
 *
 * @}
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "board.h"
#include "shell.h"
#include "thread.h"
#include "msg.h"
#include "ringbuffer.h"
#include "periph/uart.h"
#include "xtimer.h"

#include "minmea.h"
#include "fmt.h"

#ifndef SHELL_BUFSIZE
#define SHELL_BUFSIZE       (128U)
#endif
#ifndef UART_BUFSIZE
#define UART_BUFSIZE        (128U)
#endif

#define PRINTER_PRIO        (THREAD_PRIORITY_MAIN - 1)
#define PRINTER_TYPE        (0xabcd)

typedef struct {
    char rx_mem[UART_BUFSIZE];
    ringbuffer_t rx_buf;
} uart_ctx_t;

static uart_ctx_t ctx[UART_NUMOF];

static kernel_pid_t printer_pid;
static char printer_stack[THREAD_STACKSIZE_MAIN];

static char arr[128] = {0};
static unsigned arrpos = 0;
struct minmea_sentence_gll frame;

static void rx_cb(void *arg, uint8_t data)
{
    uart_t dev = (uart_t)arg;

    ringbuffer_add_one(&(ctx[dev].rx_buf), data);
    if (data == '\n') {
        msg_t msg;
        msg.content.value = (uint32_t)dev;
        msg_send(&msg, printer_pid);
    }
}

static void print_gps(char *line) {
    if (minmea_sentence_id(line, false) == MINMEA_SENTENCE_RMC) {
        struct minmea_sentence_rmc frame;
        if (minmea_parse_rmc(&frame, line)) {
            //nmea RMC format
            printf("raw coordinates: (%ld,%ld)\n", frame.latitude.value,frame.longitude.value);
            printf("Time(HH:MM:SS) (%d:%d:%d)\n",frame.time.hours,frame.time.minutes,frame.time.seconds);
            printf("Date(YY-MM-DD) (%d-%d-%d)\n",frame.date.year,frame.date.month,frame.date.day);
        }
    }
}

static void *printer(void *arg)
{
    (void)arg;
    msg_t msg;
    msg_t msg_queue[8];
    msg_init_queue(msg_queue, 8);

    while (1) {
        msg_receive(&msg); // waits here until rx_cb calls msg_send
        uart_t dev = (uart_t)msg.content.value;
        char c;

        do {
            c = (int)ringbuffer_get_one(&(ctx[dev].rx_buf));
            arr[arrpos++] = c;
        } while (c != '\n');
        arr[arrpos-5] = '\0';
        arrpos = 0;
        print_gps(arr);
    }

    /* this should never be reached */
    return NULL;
}

static int _initialize(void)
{
    int dev = 1;

    /* initialize UART */
    uart_init(UART_DEV(dev), 9600, rx_cb, (void *)dev);
    return 0;
}

static const shell_command_t shell_commands[] = {
    { NULL, NULL, NULL }
};

int main(void)
{
    /* initialize uart */
    _initialize();
  
    /* initialize ringbuffers */
    for (unsigned i = 0; i < UART_NUMOF; i++) {
        ringbuffer_init(&(ctx[i].rx_buf), ctx[i].rx_mem, UART_BUFSIZE);
    }

    /* start the printer thread */
    printer_pid = thread_create(printer_stack, sizeof(printer_stack),
                                PRINTER_PRIO, 0, printer, NULL, "printer");

    /* run the shell */
    char line_buf[SHELL_BUFSIZE];
    shell_run(shell_commands, line_buf, SHELL_BUFSIZE);
    return 0;
}
