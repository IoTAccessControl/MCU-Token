#include <stdint.h>
#include "fp_gen.h"
#include "utils.h"
#include "timer.h"
#include <stdlib.h>
#include "adc.h"
#include "dac.h"
#include "iwdg.h"
#include "utils.h"
#include "pwm.h"

const static int TASK_ID = 3000;

static void dac_test(int argc, char *argv[]);
static void adc_test(int argc, char *argv[]);
static void dac_adc_test(int argc, char *argv[]);
static void adc_ref_test(int argc, char *argv[]);
static void pwm_voltage_test(int argc, char *argv[]);
static void dac_adc_test_2(int argc, char *argv[]);
static void get_trainset_testset(int argc, char *argv[]);

const task_func_multi voltage_tasks[] = {
  {0, dac_test},
	{1, adc_test},
	{2, dac_adc_test},
	{3, adc_ref_test},
	{4, pwm_voltage_test},
	{5, dac_adc_test_2},
	{6, get_trainset_testset},
};

int dispatch_voltage_task(int argc, char *argv[]) {
	int ttype = str2int(argv[2]) % 10000;
	int round = str2int(argv[2]) / 10000;
  int tid = ttype % 1000;
	int task_num = sizeof(voltage_tasks) / sizeof(fp_task_desc);
	if (tid >= task_num) {
		DEBUG_LOG("Only %d voltage tasks, but tid = %d.\n", task_num, tid);
		return -1;
	}
	wdg_init();
	for (int i = 0; i < round; i++) {
		voltage_tasks[tid].func(argc, argv);
		wdg_feed();
	}// Warning: Don't delete this log. It notices the server current task is finished.
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

static void dac_test(int argc, char *argv[]) {
	int val = str2int(argv[3]);
	dac_init(DAC_OP_VALUE);
	for (int i = 0; i < 8000; i++);
	for (int i = 0; i < 2000; i++) {
		dac_set_value(val);
		DEBUG_LOG("output voltage %d\n", val);
	}
	dac_stop(DAC_OP_VALUE);
};

static void adc_test(int argc, char *argv[]) {
	int round = str2int(argv[3]);
	adc_multi_channel_init();
	extern volatile uint16_t ADC_ConvertedValues[3];
	for (int i = 0; i < round; i++) {
		adc_get_value(false);
		fp_evs ev;
		ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
		ev.result1 = (ADC_ConvertedValues[0] << 16) + ADC_ConvertedValues[1];
		ev.result2 = ADC_ConvertedValues[2];
		send_package((uint8_t *) &ev, sizeof(ev));
		DEBUG_LOG("%d, %d, %d\n", ADC_ConvertedValues[0], ADC_ConvertedValues[1], ADC_ConvertedValues[2]);
	}
	adc_multi_channel_stop();
}

static void dac_adc_test(int argc, char *argv[]) {
	int round = str2int(argv[3]);
	int val = str2int(argv[4]);
	dac_init(DAC_OP_VALUE);
	adc_multi_channel_init();
	extern volatile uint16_t ADC_ConvertedValues[3];
	while (round --> 0) {
		if (val != dac_set_value(val)) {
			round++;
			continue;
		}
		adc_get_value(false);
		fp_evs ev;
		ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
		ev.result1 = (ADC_ConvertedValues[0] << 16) + ADC_ConvertedValues[1];
		ev.result2 = ADC_ConvertedValues[2];
		send_package((uint8_t *) &ev, sizeof(ev));
		DEBUG_LOG("val: %d, v1: %d, v2: %d, v3: %d\n", val, ADC_ConvertedValues[0], ADC_ConvertedValues[1], ADC_ConvertedValues[2]);
	}
	adc_multi_channel_stop();
	dac_stop(DAC_OP_VALUE);
}

static void adc_ref_test(int argc, char *argv[]) {
	int round = str2int(argv[3]);
	adc_reference_init();
	#ifdef USE_ESP32
  	// https://www.esp32.com/viewtopic.php?t=17155
		// delay
		for (int i = 0; i < 4000 * 1000; i++) {
			if (i % 10000 == 0) wdg_feed();
		};
	#endif
	extern volatile uint16_t ADC_ConvertedValue;
	for (int i = 0; i < round; i++) {
		adc_get_ref_value();
		fp_evs ev;
		ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
		ev.result1 = ADC_ConvertedValue;
		ev.result2 = 0;
		send_package((uint8_t *) &ev, sizeof(ev));
		DEBUG_LOG("VREF: %d\n", ADC_ConvertedValue);
	}
	adc_reference_stop();
}

static void pwm_voltage_test(int argc, char *argv[]) {
	int wait_time = str2int(argv[3]);
	int clock_number = str2int(argv[4]);
	int duty = str2int(argv[5]);
	int freqency = str2int(argv[6]);
	int duty_resolution = str2int(argv[7]);
	
	fp_pwm_init(clock_number, duty, freqency, duty_resolution, str2int(argv[8]), str2int(argv[9]));

	adc_multi_channel_init();
	extern volatile uint16_t ADC_ConvertedValues[3];
	
	bool arrived_peak = false;
	int curr_second = 0;
	int second_count = 0;
	int upper = 6552;
	#ifdef USE_KEIL
	upper = 3600;
	#endif // USE_KEIL
	#ifdef USE_STM32F103
	upper = 3600;
	#endif

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

	uint32_t record_voltage = 0;
	while(1) {
		adc_get_value(true);
		curr_second = ADC_ConvertedValues[2];
		#ifdef USE_KEIL
		curr_second = ADC_ConvertedValues[1];
		#endif // USE_KEIL
		record_voltage += curr_second;
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

	adc_multi_channel_stop();
	fp_pwm_stop();
	
	fp_evs ev;
	ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
	ev.result1 = record_voltage;
	ev.result2 = 0;
	send_package((uint8_t *) &ev, sizeof(ev));
	DEBUG_LOG("PWM voltage test: %d\n", record_voltage);
}

static void dac_adc_test_2(int argc, char *argv[]) {
	int round = str2int(argv[3]);
	int val = str2int(argv[4]);
	dac_init(DAC_OP_VALUE);
	adc_multi_channel_init();
	extern volatile uint16_t ADC_ConvertedValues[3];
	extern volatile uint16_t ADC_ConvertedValuesCorrected[3];
	while (round --> 0) {
		if (val != dac_set_value(val)) {
			round++;
			continue;
		}
		adc_get_value(false);
		fp_evs ev;
		ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
		ev.result1 = (ADC_ConvertedValues[0] << 16) + ADC_ConvertedValues[1];
		ev.result2 = ADC_ConvertedValues[2];
		send_package((uint8_t *) &ev, sizeof(ev));
		DEBUG_LOG("val: %d, v1: %d, v2: %d, v3: %d\n", val, ADC_ConvertedValues[0], ADC_ConvertedValues[1], ADC_ConvertedValues[2]);
		ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
		ev.result1 = (ADC_ConvertedValuesCorrected[0] << 16) + ADC_ConvertedValuesCorrected[1];
		ev.result2 = ADC_ConvertedValuesCorrected[2];
		send_package((uint8_t *) &ev, sizeof(ev));
		DEBUG_LOG("val: %d, v1: %d, v2: %d, v3: %d\n", val, ADC_ConvertedValuesCorrected[0], ADC_ConvertedValuesCorrected[1], ADC_ConvertedValuesCorrected[2]);
	}
	adc_multi_channel_stop();
	dac_stop(DAC_OP_VALUE);
}

static void get_trainset_testset(int argc, char * argv[]) {
	// adc before vref: 2 * 1 * 255
	#ifdef USE_ESP32
	argv[2] = "2";
	argv[3] = "1";
	for (int val = 0; val < 256; val++) {
		int2str(argv[4], val);
		dac_adc_test_2(argc, argv);
	}

	// PWM-voltage
	argv[2] = "4";
	argv[3] = "50"; // round 
	argv[4] = "0"; // clock source
	argv[7] = "13"; // duty resolution
	argv[8] = "0";
	argv[9] = "0";
	for (int frequency = 2500; frequency < 6000; frequency += 2500) { // 2
		int2str(argv[6], frequency);
		for (int clock_source = 0; clock_source < 3; clock_source+=2) { // 2
			int2str(argv[4], clock_source);
			for (int duty = 16; duty < 8016; duty += 16) { // 500
				int2str(argv[5], duty);
				pwm_voltage_test(argc, argv);
				wdg_feed();
			}
		}
	}
	
	// VREF: 1
	argv[2] = "3";
	argv[3] = "1";
	adc_ref_test(argc, argv);

	// adc after vref: 2 * 1 * 255
	argv[2] = "2";
	argv[3] = "1";
	for (int val = 0; val < 256; val++) {
		int2str(argv[4], val);
		dac_adc_test_2(argc, argv);
	}

	// PWM-voltage
	argv[2] = "4";
	argv[3] = "50"; // round 
	argv[4] = "0"; // clock source
	argv[7] = "13"; // duty resolution
	argv[8] = "0";
	argv[9] = "0";
	for (int frequency = 2500; frequency < 6000; frequency += 2500) { // 2
		int2str(argv[6], frequency);
		for (int clock_source = 0; clock_source < 3; clock_source+=2) { // 2
			int2str(argv[4], clock_source);
			for (int duty = 16; duty < 8016; duty += 16) { // 500
				int2str(argv[5], duty);
				pwm_voltage_test(argc, argv);
				wdg_feed();
			}
		}
	}
	#endif // USE_ESP32

	#ifdef USE_KEIL
	argv[2] = "2";
	argv[3] = "1";
	for (int val = 0; val < 4096; val += 128) { // 32
		int2str(argv[4], val);
		dac_adc_test_2(argc, argv);
	}

	// PWM-voltage
	argv[2] = "4";
	argv[3] = "50"; // round 
	argv[4] = "0"; // clock source
	argv[7] = "13"; // duty resolution
	argv[8] = "0";
	argv[9] = "0";
	for (int frequency = 100; frequency < 150; frequency += 10) { // 5
		int2str(argv[6], frequency);
		for (int clock_source = 0; clock_source < 1; clock_source++) { // 1
			int2str(argv[4], clock_source);
			for (int duty = 1; duty < 999; duty += 50) { // 20
				int2str(argv[5], duty);
				pwm_voltage_test(argc, argv);
				wdg_feed();
			}	
		}
	}
	#endif // USE_KEIL

	#ifdef USE_STM32F103
	argv[2] = "2";
	argv[3] = "1";
	for (int val = 0; val < 4096; val += 128) { // 32
		int2str(argv[4], val);
		dac_adc_test_2(argc, argv);
	}

	// PWM-voltage
	argv[2] = "4";
	argv[3] = "50"; // round 
	argv[4] = "0"; // clock source
	argv[7] = "1500"; // duty resolution
	argv[8] = "0";
	argv[9] = "0";
	for (int frequency = 80; frequency < 130; frequency += 10) { // 5
		int2str(argv[6], frequency);
		for (int clock_source = 0; clock_source < 1; clock_source++) { // 1
			int2str(argv[4], clock_source);
			for (int duty = 1; duty < 999; duty += 50) { // 20
				int2str(argv[5], duty);
				pwm_voltage_test(argc, argv);
				wdg_feed();
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
