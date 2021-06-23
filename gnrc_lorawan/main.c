/*
 * Copyright (C) 2019 HAW Hamburg
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

/**
 * @ingroup     tests
 * @{
 * @file
 * @brief       Test application for GNRC LoRaWAN
 *
 * @author      José Ignacio Alamos <jose.alamos@haw-hamburg.de>
 * @}
 */

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <nanocbor/nanocbor.h>

#include "shell.h"
#include "shell_commands.h"
#include "thread.h"
#include "xtimer.h"

#include "board.h"

#include "net/gnrc/netapi.h"
#include "net/gnrc/netif.h"

#include "net/gnrc/netreg.h"
#include "net/gnrc/pktbuf.h"
#include "net/gnrc/pktdump.h"
#include "net/loramac.h"

#define LORAWAN_QUEUE_SIZE (4U)
/* Unit system wait time to complete join procedure */
#define JOIN_DELAY (10 * US_PER_SEC)

#define CBOR_BUF_SIZE (64)

static uint8_t buf[CBOR_BUF_SIZE];

typedef struct sensor_values {
  // Gas sensor
  int16_t temperature;
  uint32_t pressure;
  uint32_t humidity;
  uint32_t gas_resistance;
  // GPS
  uint16_t coord_1;
  uint16_t coord_2;
  uint64_t time;
} sensor_values_t;

sensor_values_t read_sensors(void) {
  static sensor_values_t vals = {1, 2, 3, 4, 5, 6, 7};
  return vals;
}

int run(void) {
  gnrc_pktsnip_t* pkt;
  uint8_t port = CONFIG_LORAMAC_DEFAULT_TX_PORT; /* Default: 2 */
  int interface = 3;

  sensor_values_t vals = read_sensors();
  nanocbor_encoder_t enc;
  nanocbor_encoder_init(&enc, buf, sizeof(buf));
  nanocbor_fmt_array_indefinite(&enc);
  nanocbor_fmt_int(&enc, vals.temperature);
  nanocbor_fmt_uint(&enc, vals.pressure);
  nanocbor_fmt_uint(&enc, vals.humidity);
  nanocbor_fmt_uint(&enc, vals.gas_resistance);
  nanocbor_fmt_uint(&enc, vals.coord_1);
  nanocbor_fmt_uint(&enc, vals.coord_2);
  nanocbor_fmt_uint(&enc, vals.time);
  nanocbor_fmt_end_indefinite(&enc);

  size_t cbor_encoded_len = nanocbor_encoded_len(&enc);
  printf("Length of cbor thingy = %d", cbor_encoded_len);

  pkt = gnrc_pktbuf_add(NULL, buf, cbor_encoded_len, GNRC_NETTYPE_UNDEF);
  /* register for returned packet status */
  if (gnrc_neterr_reg(pkt) != 0) {
    puts("Can not register for error reporting");
    return 0;
  }
  gnrc_netapi_set(interface, NETOPT_LORAWAN_TX_PORT, 0, &port, sizeof(port));
  gnrc_netif_send(gnrc_netif_get_by_pid(interface), pkt);
  /* wait for packet status and check */
  msg_t msg;
  msg_receive(&msg);
  if ((msg.type != GNRC_NETERR_MSG_TYPE)
      || (msg.content.value != GNRC_NETERR_SUCCESS)) {
    printf("Error sending packet: (status: %d\n)", (int) msg.content.value);
  } else {
    puts("Successfully sent packet");
  }
  return 0;
}

/* Join the network */
static netopt_enable_t _join(const kernel_pid_t* interface) {
  netopt_enable_t en = NETOPT_ENABLE;
  gnrc_netapi_set(*interface, NETOPT_LINK, 0, &en, sizeof(en));
  xtimer_usleep(JOIN_DELAY);
  gnrc_netapi_get(*interface, NETOPT_LINK, 0, &en, sizeof(en));
  return en;
}

/* Get interface ID */
static int _get_interface(kernel_pid_t* interface) {
  gnrc_netif_t* netif = NULL;
  /* Iterate over all network interfaces */
  while ((netif = gnrc_netif_iter(netif))) {
    uint16_t _type = 0;
    gnrc_netapi_get(netif->pid, NETOPT_DEVICE_TYPE, 0, &_type, sizeof(_type));
    if (_type == NETDEV_TYPE_LORA) {
      *interface = netif->pid;
      return 0;
    } else {
      puts("Not a LORA interface...");
      printf("%d != %d", _type, NETDEV_TYPE_LORA);
    }
  }
  return 1;
}

int run_cmd(int argc, char** argv) {
  (void) argc;
  (void) argv;
  puts("Searching for lorawan interface now");
  kernel_pid_t interface_d;
  if (_get_interface(&interface_d)) {
    puts("Couldn't find a LoRaWAN interface");
    return 1;
  }
  puts("Setting the interface state `up`");
  /* Wait for node to join NW */
  while (_join(&interface_d) != NETOPT_ENABLE)
    ;
  puts("Device joined\nrunning loop now!");
  while (1)
    run();
}

static const shell_command_t shell_commands[]
  = {{"run", "Run the program", run_cmd}, {NULL, NULL, NULL}};

int main(void) {
  puts("Initialization successful - starting the shell now");
  gnrc_netreg_entry_t dump = GNRC_NETREG_ENTRY_INIT_PID(
    CONFIG_LORAMAC_DEFAULT_TX_PORT, gnrc_pktdump_pid);
  gnrc_netreg_register(GNRC_NETTYPE_LORAWAN, &dump);
  char line_buf[SHELL_DEFAULT_BUFSIZE];
  shell_run(shell_commands, line_buf, SHELL_DEFAULT_BUFSIZE);
  return 0;
}
