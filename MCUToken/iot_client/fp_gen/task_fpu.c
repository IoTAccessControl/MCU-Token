#include <stdint.h>
#include "fp_gen.h"
#include "utils.h"
#include "timer.h"
#include <math.h>
#include <stdlib.h>
#include "iwdg.h"

const static int TASK_ID = 1000;

static void fpu_add(int argc, char *argv[]);
static void fpu_sub(int argc, char *argv[]);
static void fpu_mul(int argc, char *argv[]);
static void fpu_div(int argc, char *argv[]);
static void fpu_add_64(int argc, char *argv[]);
static void fpu_sub_64(int argc, char *argv[]);
static void fpu_mul_64(int argc, char *argv[]);
static void fpu_div_64(int argc, char *argv[]);
static void mandekbrot_test(int argc, char *argv[]);
static void mandekbrot_test_64(int argc, char *argv[]);
static void get_trainset_testset(int argc, char * argv[]);

const task_func_multi g_tasks[] = {
	{0, fpu_add},
	{1, fpu_sub},
	{2, fpu_mul},
	{3, fpu_div},
	{4, fpu_add_64},
	{5, fpu_sub_64},
	{6, fpu_mul_64},
	{7, fpu_div_64},
	{8, mandekbrot_test},
	{9, mandekbrot_test_64},
	{10, get_trainset_testset},
};


int dispatch_fpu_task(int argc, char *argv[]) {
	int ttype = str2int(argv[2]) % 10000;
	int round = str2int(argv[2]) / 10000;
	int tid = ttype % 1000;
	int task_num = sizeof(g_tasks) / sizeof(fp_task_desc);
	if (tid > task_num) {
		DEBUG_LOG("Only %d fpu tasks, but tid = %d.\n", task_num, tid);
		return -1;
	}
	wdg_init();
	for (int i = 0; i < round; i++) {
		g_tasks[tid].func(argc, argv);
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
static void fpu_add(int argc, char *argv[]) {
	int round = str2int(argv[3]);
	reset_timer_tick();
	float a = 1.2345;
	int last_tick = get_cur_tick();
	for (int i = 0; i < round; i++) {
		a += 0.678f;
	}
	int result = get_cur_tick() - last_tick;
	fp_evs ev;
	ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
	ev.result1 = result;
	ev.result2 = 0;
	send_package((uint8_t *) &ev, sizeof(ev));
	DEBUG_LOG("In fpu add : %d, %d\n", round, result);
}

static void fpu_sub(int argc, char *argv[]) {
	int round = str2int(argv[3]);
	reset_timer_tick();
	float a = 1.2345;
	int last_tick = get_cur_tick();
	for (int i = 0; i < round; i++) {
		a -= 0.678f;
	}
	int result = get_cur_tick() - last_tick;
	fp_evs ev;
	ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
	ev.result1 = result;
	ev.result2 = 0;
	send_package((uint8_t *) &ev, sizeof(ev));
	DEBUG_LOG("In fpu sub : %d, %d\n", round, result);
}

static void fpu_mul(int argc, char *argv[]) {
	int round = str2int(argv[3]);
	reset_timer_tick();
	float a = 1.2345;
	int last_tick = get_cur_tick();
	for (int i = 0; i < round; i++) {
		a *= 1.008f;
	}
	int result = get_cur_tick() - last_tick;
	fp_evs ev;
	ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
	ev.result1 = result;
	ev.result2 = 0;
	send_package((uint8_t *) &ev, sizeof(ev));
	DEBUG_LOG("In fpu mul : %d, %d\n", round, result);
}

static void fpu_div(int argc, char *argv[]) {
	int round = str2int(argv[3]);
	reset_timer_tick();
	float a = 1.2345;
	int last_tick = get_cur_tick();
	for (int i = 0; i < round; i++) {
		a /= 0.987f;
	}
	int result = get_cur_tick() - last_tick;
	fp_evs ev;
	ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
	ev.result1 = result;
	ev.result2 = 0;
	send_package((uint8_t *) &ev, sizeof(ev));
	DEBUG_LOG("In fpu div float : %d, %d\n", round, result);
}

static void fpu_add_64(int argc, char *argv[]) {
	int round = str2int(argv[3]);
	reset_timer_tick();
	double a = 1.2345;
	int last_tick = get_cur_tick();
	for (int i = 0; i < round; i++) {
		a += 0.678f;
	}
	int result = get_cur_tick() - last_tick;
	fp_evs ev;
	ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
	ev.result1 = result;
	ev.result2 = 0;
	send_package((uint8_t *) &ev, sizeof(ev));
	DEBUG_LOG("In fpu add double: %d, %d\n", round, result);
}

static void fpu_sub_64(int argc, char *argv[]) {
	int round = str2int(argv[3]);
	reset_timer_tick();
	double a = 1.2345;
	int last_tick = get_cur_tick();
	for (int i = 0; i < round; i++) {
		a -= 0.678f;
	}
	int result = get_cur_tick() - last_tick;
	fp_evs ev;
	ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
	ev.result1 = result;
	ev.result2 = 0;
	send_package((uint8_t *) &ev, sizeof(ev));
	DEBUG_LOG("In fpu sub double: %d, %d\n", round, result);
}

static void fpu_mul_64(int argc, char *argv[]) {
	int round = str2int(argv[3]);
	reset_timer_tick();
	double a = 1.2345;
	int last_tick = get_cur_tick();
	for (int i = 0; i < round; i++) {
		a *= 1.008f;
	}
	int result = get_cur_tick() - last_tick;
	fp_evs ev;
	ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
	ev.result1 = result;
	ev.result2 = 0;
	send_package((uint8_t *) &ev, sizeof(ev));
	DEBUG_LOG("In fpu mul double: %d, %d\n", round, result);
}

static void fpu_div_64(int argc, char *argv[]) {
	int round = str2int(argv[3]);
	reset_timer_tick();
	double a = 1.2345;
	int last_tick = get_cur_tick();
	for (int i = 0; i < round; i++) {
		a /= 0.987;
	}
	int result = get_cur_tick() - last_tick;
	fp_evs ev;
	ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
	ev.result1 = result;
	ev.result2 = 0;
	send_package((uint8_t *) &ev, sizeof(ev));
	DEBUG_LOG("In fpu div double : %d, %d\n", round, result);
}

static void mandekbrot_test(int argc, char *argv[]) {
	reset_timer_tick();
	int W = str2int(argv[3]);
	int H = str2int(argv[4]);
	int k;
	float c_imag, c_real = 0.;
	float z_imag, z_real, y_imag, y_real;
	srand(42);
	int last_tick = get_cur_tick();
	for (int j = H; j >= H / 2; j--) {
		// c_imag = *(y+j);
		c_imag = (float) rand() / RAND_MAX;
		for (int i = 0; i <= W; i++) {
			// c_real = *(x+i);
			c_real = (float) rand() / RAND_MAX;
			z_imag = 0.0;
			z_real = 0.0;
			y_imag = 0.0;
			y_real = 0.0;
			for (k = 0; k < 64; k++) {
				y_real = z_real * z_real - z_imag * z_imag;
				y_imag = z_real * z_imag + z_imag * z_real;

				z_real = y_real + c_real;
				z_imag = y_imag + c_imag;
		
				if ((z_real * z_real + z_imag * z_imag) > 4.0f)
					break;
			}
		}
	}
	int result = get_cur_tick() - last_tick;
	fp_evs ev;
	ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
	ev.result1 = result;
	ev.result2 = 0;
	send_package((uint8_t *) &ev, sizeof(ev));
	DEBUG_LOG("In mandelbrot: %d, w: %d, h:%d\n", result, H, W);
}

static void mandekbrot_test_64(int argc, char *argv[]) {
	reset_timer_tick();
	int W = str2int(argv[3]);
	int H = str2int(argv[4]);
	double c_imag, c_real;
	double z_imag, z_real, y_imag, y_real;
	srand(42 + 1);
	int last_tick = get_cur_tick();
	for (int j = H; j >= H / 2; j--) {
		c_imag = (double) rand() / RAND_MAX;
		for (int i = 0; i <= W; i++) {
			c_real = (double) rand() / RAND_MAX;
			z_imag = 0.0;
			z_real = 0.0;
			y_imag = 0.0;
			y_real = 0.0;
			for (int k = 0; k < 64; k++) {
				y_real = z_real * z_real - z_imag * z_imag;
				y_imag = z_real * z_imag + z_imag * z_real;

				z_real = y_real + c_real;
				z_imag = y_imag + c_imag;
		
				if ((z_real * z_real + z_imag * z_imag) > 4.0 )
					break;
			}
		}
	}
	int result = get_cur_tick() - last_tick;
	fp_evs ev;
	ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
	ev.result1 = result;
	ev.result2 = 0;
	send_package((uint8_t *) &ev, sizeof(ev));
	DEBUG_LOG("In mandelbrot double: %d, w: %d, h:%d\n", result, H, W);
}

static void get_trainset_testset(int argc, char * argv[]) {
	// mandelbret
	argv[2] = "8";
	for (int i = 1; i < 21; i+=2) {
		char t[10];
		itoa(i, (char*)t, 10);
		argv[3] = t;
		for (int j = 1; j < 21; j+=2) {
			char t1[10];
			itoa(j, (char*)t1, 10);
			argv[4] = t1;
			mandekbrot_test(argc, argv);
			wdg_feed();
		}
	}

	// mandelbret double
	argv[2] = "9";
	for (int i = 1; i < 21; i+=2) {
		char t[10];
		itoa(i, (char*)t, 10);
		argv[3] = t;
		for (int j = 1; j < 21; j+=2) {
			char t1[10];
			itoa(j, (char*)t1, 10);
			argv[4] = t1;
			mandekbrot_test_64(argc, argv);
			wdg_feed();
		}
	}
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
