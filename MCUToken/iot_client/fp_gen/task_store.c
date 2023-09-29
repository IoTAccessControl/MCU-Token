#include <stdint.h>
#include "fp_gen.h"
#include "utils.h"
#include "timer.h"
#include <stdlib.h>
#include "rtc.h"
#include <string.h>
#include "iwdg.h"

#include "flash_internal.h"

const static int TASK_ID = 5000;

static void get_sram_distribution(int argc, char *argv[]);
static void get_trainset_testset(int argc, char * argv[]);

const task_func_multi store_tasks[] = {
	{0, get_sram_distribution},
	{1, get_trainset_testset},
};

int dispatch_store_task(int argc, char *argv[]) {
	int ttype = str2int(argv[2]) % 10000;
	int round = str2int(argv[2]) / 10000;
  int tid = ttype % 1000;
	int task_num = sizeof(store_tasks) / sizeof(fp_task_desc);
	if (tid >= task_num) {
		DEBUG_LOG("Only %d store tasks, but tid = %d.\n", task_num, tid);
		return -1;
	}
	wdg_init();
	for (int i = 0; i < round; i++) {
		store_tasks[tid].func(argc, argv);
		wdg_feed();
	}
	// Warning: Don't delete this log. It notices the server current task is finished.
	send_message("Finish Task: %d\n", ttype);
	return 0;
}

#ifdef USE_KEIL
	#pragma push
	#pragma O0
#endif // USE_KEIL
#ifdef USE_STM32F103
	#pragma push
	#pragma O0
#endif // USE_KEIL
#ifdef USE_ESP32
	#pragma GCC push_options
	#pragma GCC optimize("O0")
#endif // USE_ESP32 OPTIMIZE

static void get_sram_distribution(int argc, char *argv[]) {
	if (argc != 5) return;
	int offset = str2int(argv[3]);
	int len = str2int(argv[4]);
	extern int sram_start_address;
	uint32_t start_address = sram_start_address;
	for (uint32_t address = start_address + offset; address <= start_address + offset + len; address += 4) {
		uint32_t data =  *(volatile uint32_t*)(address);
		fp_evs ev;
		ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
		ev.result1 = address;
		ev.result2 = data;
		send_package((uint8_t *) &ev, sizeof(ev));
		DEBUG_LOG("%u_", data);
		wdg_feed();
	}
}

static void get_trainset_testset(int argc, char * argv[]) {
	#ifdef USE_ESP32
	argv[2] = "0";
	argv[3] = "0";
	argv[4] = "20000";
	get_sram_distribution(argc, argv);
	#endif // USE_ESP32

	#ifdef USE_KEIL
	argv[2] = "0";
	argv[3] = "0";
	argv[4] = "10000";
	get_sram_distribution(argc, argv);
	#endif // USE_KEIL
	
	#ifdef USE_STM32F103
	argv[2] = "0";
	argv[3] = "0";
	argv[4] = "10000";
	get_sram_distribution(argc, argv);
	#endif // USE_STM32F103
}

#ifdef USE_KEIL
	#pragma pop
#endif // USE_KEIL
#ifdef USE_STM32F103
	#pragma pop
#endif // USE_KEIL
#ifdef USE_ESP32
	#pragma GCC pop_options
#endif // USE_ESP32 OPTIMIZE
