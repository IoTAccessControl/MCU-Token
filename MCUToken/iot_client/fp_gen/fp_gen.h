#ifndef FP_GEN_H_
#define FP_GEN_H_
#include <stdio.h>
#include <stdint.h>

#define MAX_ROUND 50

typedef void (*task_func)(int, int);
typedef void (*task_func_multi_args)(int, char**);

typedef struct fp_task_desc {
	int tid;
	task_func func;
} fp_task_desc;

typedef struct task_func_multi {
	int tid;
	task_func_multi_args func;
} task_func_multi;

enum FP_TYPE {
	FP_FPU = 1000,
	FP_DSP = 2000,
	FP_VOLTAGE = 3000,
	FP_CLOCK = 4000,
	FP_STORE = 5000,
	FP_INITIAL = 6000,
};

typedef struct __attribute__((__packed__)) fp_event_simple {
	uint32_t eid_tid; // task_id type_id
	uint32_t result1; // result1 of task
	uint32_t result2; // result2 of task
} fp_evs;

int send_package(uint8_t *buf, int len);
int send_message(const char *fmt, ...);

int start_data_collect(int argc, char *argv[]);

// task
int dispatch_fpu_task(int argc, char *argv[]);
int dispatch_clock_task(int argc, char *argv[]);
int dispatch_store_task(int argc, char *argv[]);
int dispatch_voltage_task(int argc, char *argv[]);
int dispatch_init_task(int argc, char *argv[]);

#endif
