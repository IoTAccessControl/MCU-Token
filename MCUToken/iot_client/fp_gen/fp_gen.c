#include <stdlib.h>
#include "usart.h"
#include "fp_gen.h"
#include "utils.h"
#include <time.h>

int send_package(uint8_t *buf, int len) {
	// Length Type Value
	// for (int i = 0; i < len; i++) {
	// 	DEBUG_LOG("Send bytes:  \\x%X ", buf[i]);
	// }
	// DEBUG_LOG("\n");
	uasrt_send_pkt(PKT_DATA, buf, len, false);
	return len;
}

int send_message(const char *fmt, ...) {
	va_list args;
	va_start(args, fmt);
	log_print_porting(fmt, &args);
	va_end(args);
	return 1;
}


int start_data_collect(int argc, char *argv[]) {
	// all send_message should be called after usart_reset
	usart_reset();
	int ttype = str2int(argv[2]) % 10000;
	// int round = str2int(argv[3]);
	int fp_type = ttype / 1000 * 1000;
	// if (round > MAX_ROUND) {
	// 	send_message("Task Failed: round should %d <= %d\n", round, MAX_ROUND);
	// 	return -1;
	// }
	if (fp_type == FP_FPU) {
		dispatch_fpu_task(argc, argv);
	} else if (fp_type == FP_DSP) {

	} else if (fp_type == FP_VOLTAGE) {
		dispatch_voltage_task(argc, argv);
	} else if (fp_type == FP_CLOCK) {
		dispatch_clock_task(argc, argv);
	} else if (fp_type == FP_STORE) {
		dispatch_store_task(argc, argv);
	} else if (fp_type == FP_INITIAL) {
		dispatch_init_task(argc, argv);
	} else {
		DEBUG_LOG("Unsupport task type: %d %d\n", fp_type, ttype);
		return -1;
	}
	return 0;
}
