#include <stdint.h>
#include "fp_gen.h"
#include "utils.h"
#include "timer.h"
#include <stdlib.h>
#include "rtc.h"
#include "pwm.h"
#include "iwdg.h"
#include "adc.h"

const static int TASK_ID = 4000;

static void rtc_wait_count(int argc, char *argv[]);
static void pwm_time_measure(int argc, char *argv[]);
static void pwm_continuous_time_measure(int argc, char* argv[]);
static void rtc_phase_measure(int argc, char *argv[]);
static void get_trainset_testset(int argc, char * argv[]);

// static bool if_rtc_initial = false;

const task_func_multi clock_tasks[] = {
	{0, rtc_wait_count},
	{1, pwm_time_measure},
	{2, pwm_continuous_time_measure},
	{3, rtc_phase_measure},
	{4, get_trainset_testset},
};

int dispatch_clock_task(int argc, char *argv[]) {
  int ttype = str2int(argv[2]) % 10000;
	int round = str2int(argv[2]) / 10000;
	int tid = ttype % 1000;
	int task_num = sizeof(clock_tasks) / sizeof(fp_task_desc);
	if (tid >= task_num) {
		DEBUG_LOG("Only %d clock tasks, but tid = %d.\n", task_num, tid);
		return -1;
	}
	wdg_init();
	for (int i = 0; i < round; i++) {
		clock_tasks[tid].func(argc, argv);
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

int previous_clock_source = -1;
int previous_division = -1;
int previous_adjustment = -1;
static void rtc_wait_count(int argc, char *argv[]) {
	int wait_time = str2int(argv[3]);
	int clock_source = str2int(argv[4]);
	int division = str2int(argv[5]);
	int adjustment = str2int(argv[6]);
	reset_timer_tick();
	if (previous_clock_source != clock_source || previous_division != division || previous_adjustment != adjustment) { // 若需要反复使用，该代码段仅执行一次即可
		rtc_setup(clock_source, division, adjustment);
		rtc_set_time();
		previous_clock_source = clock_source;
		previous_division = division;
		previous_adjustment = adjustment;
	}

	int last_second = 0;
	int curr_second = 0;
	int second_count = 0;
	int last_tick = 0;

	while(1) {
		// DEBUG_LOG("%d\n", curr_second);
		curr_second = rtc_get_second();
		if (last_second != curr_second) {
			second_count++;
			if (second_count >= 3) {
				break;
			}
		}
		last_second = curr_second;
	}

	second_count = 0;
	last_tick = get_cur_tick();
	while(1) {
		curr_second = rtc_get_second();
		if (last_second != curr_second) {
			second_count++;
		}
		last_second = curr_second;
		if (second_count >= wait_time) {
			break;
		}
	}
	int result = get_cur_tick() - last_tick;

	// int accumulation = 0;
	// while (1) {
	// 	last_tick = get_cur_tick();
	// 	curr_second = rtc_get_second();
	// 	while (rtc_get_second() == curr_second);
	// 	accumulation += get_cur_tick() - last_tick;
	// 	second_count++;
	// 	if (second_count >= wait_time) break;
	// }
	// int result = accumulation;

	fp_evs ev;
	ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
	ev.result1 = result;
	ev.result2 = 0;
	send_package((uint8_t *) &ev, sizeof(ev));
	DEBUG_LOG("In rtc wait_time : %d, %d\n", wait_time, result);
}

static void pwm_time_measure(int argc, char* argv[]) {
	int wait_time = str2int(argv[3]);
	int clock_number = str2int(argv[4]);
	int duty = str2int(argv[5]);
	int freqency = str2int(argv[6]);
	int duty_resolution = str2int(argv[7]);
	
	reset_timer_tick();
	fp_pwm_init(clock_number, duty, freqency, duty_resolution, str2int(argv[8]), str2int(argv[9]));
	adc_multi_channel_init();
	extern volatile uint16_t ADC_ConvertedValues[3];
	
	bool arrived_peak = false;
	int curr_second = 0;
	int second_count = 0;
	int last_tick = 0;
	int upper = 6552;
	#ifdef USE_KEIL
	upper = 3600;
	#endif // USE_KEIL

	while (1) {
		adc_get_value(true);
		curr_second = ADC_ConvertedValues[2];
		#ifdef USE_KEIL
		curr_second = ADC_ConvertedValues[1];
		#endif // USE_KEIL
		if (curr_second >= upper) {
			arrived_peak = true;
		}
		if (curr_second <= 1000 && arrived_peak) {
			arrived_peak = false;
			second_count++;
		}
		if (second_count >= 4) {
			second_count = 0;
			break;
		}
	}

	last_tick = get_cur_tick();
	while(1) {
		adc_get_value(true);
		curr_second = ADC_ConvertedValues[2];
		#ifdef USE_KEIL
		curr_second = ADC_ConvertedValues[1];
		#endif // USE_KEIL
		if (curr_second >= upper) {
			arrived_peak = true;
		}
		if (curr_second <= 1000 && arrived_peak) {
			arrived_peak = false;
			second_count++;
		}
		if (second_count >= wait_time) {
			break;
		}
	}
	int result = get_cur_tick() - last_tick;

	adc_multi_channel_stop();
	fp_pwm_stop();

	fp_evs ev;
	ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
	ev.result1 = result;
	ev.result2 = 0;
	send_package((uint8_t *) &ev, sizeof(ev));
	DEBUG_LOG("In pwm clock task: %d, %d\n", wait_time, result);
};

static void pwm_continuous_time_measure(int argc, char* argv[]) {
	int wait_time = str2int(argv[3]);
	int clock_number = str2int(argv[4]);
	int duty = str2int(argv[5]);
	int freqency = str2int(argv[6]);
	int duty_resolution = str2int(argv[7]);
	
	reset_timer_tick();
	fp_pwm_init(clock_number, duty, freqency, duty_resolution, str2int(argv[8]), str2int(argv[9]));
	adc_multi_channel_init();
	extern volatile uint16_t ADC_ConvertedValues[3];
	
	bool arrived_peak = false;
	int curr_second = 0;
	int second_count = 0;
	int last_tick = 0;
	int upper = 6552;
	#ifdef USE_KEIL
	upper = 3600;
	#endif // USE_KEIL
	while (1) {
		adc_get_value(true);
		curr_second = ADC_ConvertedValues[2];
		#ifdef USE_KEIL
		curr_second = ADC_ConvertedValues[1];
		#endif // USE_KEIL
		if (curr_second >= upper) {
			arrived_peak = true;
		}
		if (curr_second <= 1000 && arrived_peak) {
			arrived_peak = false;
			second_count++;
		}
		if (second_count >= 4) {
			second_count = 0;
			break;
		}
	}

	uint32_t continuous_time = 0;
	last_tick = get_cur_tick();
	while(1) {
		adc_get_value(true);
		curr_second = ADC_ConvertedValues[2];
		#ifdef USE_KEIL
		curr_second = ADC_ConvertedValues[1];
		#endif // USE_KEIL
		if (curr_second >= upper && arrived_peak == false) {
			arrived_peak = true;
			last_tick = get_cur_tick();
		}
		if (curr_second <= 1000 && arrived_peak) {
			arrived_peak = false;
			second_count++;
			continuous_time += get_cur_tick() - last_tick;
		}
		if (second_count >= wait_time) {
			break;
		}
	}
	int result = continuous_time / second_count;

	adc_multi_channel_stop();
	fp_pwm_stop();

	fp_evs ev;
	ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
	ev.result1 = result;
	ev.result2 = 0;
	send_package((uint8_t *) &ev, sizeof(ev));
	DEBUG_LOG("In pwm clock task: %d, %d\n", wait_time, result);
}

static void rtc_phase_measure(int argc, char *argv[]) {
	int wait_time = str2int(argv[3]);
	int phase_mod = str2int(argv[4]);
	int clock_source = str2int(argv[5]);
	int division = str2int(argv[6]);
	int adjustment = str2int(argv[7]);
	reset_timer_tick();
	if (previous_clock_source != clock_source || previous_division != division || previous_adjustment != adjustment) {
		rtc_setup(clock_source, division, adjustment);
		rtc_set_time();
		previous_clock_source = clock_source;
		previous_division = division;
		previous_adjustment = adjustment;
	}

	int last_second = 0;
	int curr_second = 0;
	int second_count = 0;

	while(1) {
		curr_second = rtc_get_second();
		if (last_second != curr_second) {
			second_count++;
		}
		last_second = curr_second;
		if (second_count >= 3) {
			break;
		}
	}

	uint32_t phase = 0;
	while(1) {
		curr_second = rtc_get_second();
		if (last_second != curr_second) {
			second_count++;
			phase += get_cur_tick() % phase_mod;
		}
		last_second = curr_second;
		if (second_count >= wait_time) {
			break;
		}
	}
	int result = phase;
	fp_evs ev;
	ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
	ev.result1 = result;
	ev.result2 = 0;
	send_package((uint8_t *) &ev, sizeof(ev));
	DEBUG_LOG("In pwm phase task: %d, %d, %d\n", wait_time, phase_mod, result);
}

static void get_trainset_testset(int argc, char * argv[]) {
	// RTCFreq
	#ifdef USE_ESP32
	argv[2] = "0";
	for (int wait_time = 50; wait_time < 250; wait_time += 50) {
		int2str(argv[3], wait_time);
		for (int clock_source = 0; clock_source < 2; clock_source++) {
			int2str(argv[4], clock_source);
			for (int division = 0; division < 4; division++) {
				int2str(argv[5], (1 << division) - 1);
				for (int adjustment = 0; adjustment < 256; adjustment+=2) {
					int2str(argv[6], adjustment);
					rtc_wait_count(argc, argv);
					wdg_feed();
				}
			}
		}
	}
	#endif // USE_ESP32

	// RTC phase
	#ifdef USE_ESP32
	argv[2] = "3";
	for (int wait_time = 50; wait_time < 250; wait_time += 50) { // 4
		int2str(argv[3], wait_time);
		for (int clock_source = 0; clock_source < 2; clock_source++) { // 2
			int2str(argv[5], clock_source);
			for (int division = 0; division < 4; division++) { // 4
				int2str(argv[6], (1 << division) - 1);
				for (int phase = 100; phase < 40000; phase += 400) {
					int2str(argv[4], phase);
					rtc_phase_measure(argc, argv);
					wdg_feed();
				}
			}
		}
	}
	#endif // USE_ESP32

	#ifdef USE_KEIL
	argv[2] = "0";
	for (int clock_source = 0; clock_source < 1; clock_source++) { // 1
		int2str(argv[4], clock_source);
		for (int division = 1; division < 3; division++) { // 2
			int2str(argv[5], division);
			for (int adjustment = 1; adjustment < 3; adjustment+=1) { // 2
				int2str(argv[6], adjustment);
				for (int wait_time = 50; wait_time < 150; wait_time += 5) { // 20
					int2str(argv[3], wait_time);
					rtc_wait_count(argc, argv);
					wdg_feed();
				}
			}
		}
	}

	argv[2] = "3";
	argv[7] = "1";
	
	for (int clock_source = 0; clock_source < 1; clock_source++) { // 1
		int2str(argv[5], clock_source);
		for (int division = 1; division < 3; division++) { // 2
			int2str(argv[6], division);
			for (int wait_time = 50; wait_time < 70; wait_time += 10) { // 2
				int2str(argv[3], wait_time);
				for (int phase = 10000; phase < 50000; phase += 2000) { // 20
					int2str(argv[4], phase);
					rtc_phase_measure(argc, argv);
					wdg_feed();
				}
			}
		}
	}
	#endif // USE_KEIL
	
	#ifdef USE_STM32F103
	argv[2] = "0";
	for (int clock_source = 0; clock_source < 1; clock_source++) { // 1
		int2str(argv[4], clock_source);
		for (int division = 1; division < 3; division++) { // 2
			int2str(argv[5], division);
			for (int adjustment = 1; adjustment < 3; adjustment+=1) { // 2
				int2str(argv[6], adjustment);
				for (int wait_time = 50; wait_time < 150; wait_time += 5) { // 20
					int2str(argv[3], wait_time);
					rtc_wait_count(argc, argv);
					wdg_feed();
				}
			}
		}
	}

	argv[2] = "3";
	argv[7] = "1";
	for (int clock_source = 0; clock_source < 1; clock_source++) { // 1
		int2str(argv[5], clock_source);
		for (int division = 1; division < 3; division++) { // 2
			int2str(argv[6], division);
			for (int wait_time = 50; wait_time < 70; wait_time += 10) { // 2
				int2str(argv[3], wait_time);
				for (int phase = 10000; phase < 50000; phase += 2000) { // 20
					int2str(argv[4], phase);
					rtc_phase_measure(argc, argv);
					wdg_feed();
				}
			}
		}
	}
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
