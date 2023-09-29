#include "token_gen.h"
#include "utils.h"
#include "timer.h"
#include "rtc.h"
#include "pwm.h"
#include "iwdg.h"
#include "adc.h"
#include "dac.h"

static const int total_num = 5;
static const int used_num = 3;

static unsigned int sram_task(unsigned int task, bool poisoned);
static unsigned int fpu_task(unsigned int task, bool poisoned);
static unsigned int dac_adc_task(unsigned int task, bool poisoned);
static unsigned int pwm_task(unsigned int task, bool poisoned);
static unsigned int rtc_frequency_task(unsigned int task, bool poisoned);
static unsigned int rtc_phra_task(unsigned int task, bool poisoned);

const task_token_func_multi token_tasks[] = {
  {0, sram_task},
  {1, fpu_task},
  {2, dac_adc_task},
  {3, pwm_task},
  {4, rtc_frequency_task},
  {5, rtc_phra_task},
};

void generator_token(const char *operation, const char* nonce, const char** payloads);

int token_generate(int argc, char *argv[]) {
  char nonce[12];
  itoa(rand() % (0xFFFFFFFF), nonce, 10);
  char *payloads[total_num];
  // divide payloads
  #ifdef USE_STM32F103
  // there i sno malloc on STM32F103
  char t[10][100];
  #endif // USE_STM32F103
  for (int i = 0; i < total_num; i++) {
    #ifdef USE_STM32F103
    payloads[i] = t[i];
    #else
    payloads[i] = (char *)malloc(100*sizeof(char));;
    #endif // USE_STM32F103
    memset(payloads[i], 0, 100);
  }
  for (int i = 2; i < argc; i++) strcat(payloads[(i-2)%total_num], argv[i]);

  generator_token(argv[1], nonce, (const char**) payloads);

  #ifndef USE_STM32F103
  for (int i = 0; i < total_num; i++) free(payloads[i]);
  #endif // USE_STM32F103

  return 1;
};

static void message_mapping(const char *operation, const char* nonce, const char** payloads, unsigned int* tasks);

void generator_token(const char *operation, const char* nonce, const char** payloads) {
	// request information
	printf("\r\noperation: %s, nonce: %s, payloads:", operation, nonce);
	for (int i = 0; i < total_num; i++) {
		if (i != total_num - 1) printf("[%s], ", payloads[i]);
		else printf("[%s]\r\n", payloads[i]);
	}

	// message mapping
	unsigned int tasks[total_num];
	message_mapping(operation, nonce, payloads, tasks);

	// fingerprints generator && data poisoning
	int poisoned[total_num];
	int remain_num = used_num;
	for (int i = 0; i < total_num; i++) {
		if (rand() % (total_num - i) < remain_num) {
			poisoned[i] = 0;
			remain_num--;
		} else poisoned[i] = 1;
	}
	printf("tokens: ");
	for (int i = 0; i < total_num; i++) {
		int task_type = (tasks[i] >> 16) % (sizeof(token_tasks) / sizeof(task_token_func_multi));
		unsigned int fingerprint = 0;
		fingerprint = token_tasks[task_type].func(tasks[i], poisoned[i]);
		if (i != total_num - 1) printf("%u,", fingerprint);
		else printf("%u\r\n", fingerprint);
		// printf("task_type: %d, poisoned: %d, fingerprint: %u\r\n", task_type, poisoned[i], fingerprint);
	}
}


static unsigned int APHash(const char* str, unsigned int len) {
	unsigned int hash = 0xAAAAAAAA;
	unsigned int i    = 0;

	for(i = 0; i < len; str++, i++) {
		hash ^= ((i & 1) == 0) ? (  (hash <<  7) ^ (*str) * (hash >> 3)) :
															(~((hash << 11) + ((*str) ^ (hash >> 5))));
	}

	return hash;
}

static void message_mapping(const char *operation, const char* nonce, const char** payloads, unsigned int* tasks) {
	unsigned int digest = 0;
	for (int i = 0; i < total_num; i++) {
		char hash_str[100];

		memset(hash_str, 0, strlen(hash_str));
		memcpy(hash_str, operation, strlen(operation) + 1);
		strcat(hash_str, ",");
		strcat(hash_str, nonce);
		strcat(hash_str, ",");
		char digest_str[12];
		utoa(digest, (char*)digest_str, 10);
		strcat(hash_str, digest_str);
		unsigned int h1 = APHash(hash_str, strlen(hash_str));

		memset(hash_str, 0, strlen(hash_str));
		memcpy(hash_str, nonce, strlen(nonce) + 1);
		strcat(hash_str, ",");
		strcat(hash_str, payloads[i]);
		unsigned int h2 = APHash(hash_str, strlen(hash_str));

		memset(hash_str, 0, strlen(hash_str));
		memcpy(hash_str, nonce, strlen(nonce) + 1);
		strcat(hash_str, ",");
		strcat(hash_str, payloads[total_num - i - 1]);
		unsigned int h3 = APHash(hash_str, strlen(hash_str));

		char h1_str[12];
		utoa(h1, (char*)h1_str, 10);
		char h2_str[12];
		utoa(h2, (char*)h2_str, 10);
		char h3_str[12];
		utoa(h3, (char*)h3_str, 10);
		memset(hash_str, 0, strlen(hash_str));
		memcpy(hash_str, (const char*)h1_str, strlen(h1_str) + 1);
		strcat(hash_str, ",");
		strcat(hash_str, (const char*)h2_str);
		strcat(hash_str, ",");
		strcat(hash_str, (const char*)h3_str);
		digest = APHash(hash_str, strlen(hash_str));
		tasks[i] = digest;
	}
}

// different tasks
unsigned int sram_task(unsigned int task, bool poisoned) {
  extern int sram_start_address;
  int offset = task & 0xFFF;
  unsigned int result = *(volatile unsigned int*)(sram_start_address + offset * 4);
  result = result & 0xFFFF;
  if (poisoned) return result & (0xAAAAAAAA & rand() % 0xFFFFFFFF);
  else return result;
}

unsigned int fpu_task(unsigned int task, bool poisoned) {
  reset_timer_tick();
	int W = task & 0x3F;
	int H = (task >> 8) & 0x3F;
	double c_imag, c_real;
	double z_imag, z_real, y_imag, y_real;
	unsigned int last_tick = get_cur_tick();
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
	unsigned int result = get_cur_tick() - last_tick;
  if (poisoned) return (unsigned int)(result * (1.0 + 1.0 * (rand() % 13 + 8) / 100));
  else return result;
}

static unsigned int dac_adc_task(unsigned int task, bool poisoned) {
  int round = (task & 0x7F) + 10;
	int val = (task >> 8) % 4096;
	dac_init(DAC_OP_VALUE);
	adc_multi_channel_init();
	extern volatile uint16_t ADC_ConvertedValues[3];
  unsigned int result = 0;
	while (round --> 0) {
		if (val != dac_set_value(val)) {
			round++;
			continue;
		}
		adc_get_value(false);
    result += abs(ADC_ConvertedValues[1] - ADC_ConvertedValues[2]);
	}
	adc_multi_channel_stop();
	dac_stop(DAC_OP_VALUE);
  if (poisoned) return (unsigned int)(result * (1.0 + 1.0 * (rand() % 13 + 8) / 100));
  else return result;
};

static unsigned int pwm_task(unsigned int task, bool poisoned) {
  int wait_time = (task & 0xf) * 10 + 10;

  #ifdef USE_ESP32
  int clock_number = 0;
  int freqency = (((task >> 4) & 0x1) + 1) * 2500;
  int duty =  ((task >> 5) % 5000) + 16;
  int duty_resolution = 13;
  #endif // USE_ESP32

	#ifdef USE_STM32F103
  int clock_number = 0;
  int freqency = ((task >> 4) % 120) + 80;
  int duty =  ((task >> 8) % 600) + 50;
  int duty_resolution = 1500;
	#endif // USE_STM32F103

	#ifdef USE_KEIL
  int clock_number = 0;
  int freqency = ((task >> 4) % 120) + 80;
  int duty =  ((task >> 8) % 600) + 50;
  int duty_resolution = 13;
  #endif //USE_KEIL
	
	fp_pwm_init(clock_number, duty, freqency, duty_resolution, 0, 0);

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
	
	unsigned int result = record_voltage;
  if (poisoned) return (unsigned int)(result * (1.0 + 1.0 * (rand() % 13 + 8) / 100));
  else return result;
};

extern int previous_clock_source;
extern int previous_division;
extern int previous_adjustment;

static unsigned int rtc_frequency_task(unsigned int task, bool poisoned) {
  #ifdef USE_ESP32
  int wait_time = ((task) % 100) + 10;
	int clock_source = 0;
	int division = 2;
	int adjustment = 125;
  #endif // USE_ESP32

  #ifdef USE_STM32F103
  int wait_time = ((task) % 100) + 10;
	int clock_source = 0;
	int division = 2;
	int adjustment = 2;
	#endif // USE_STM32F103

  #ifdef USE_KEIL
  int wait_time = ((task) % 60) + 10;
	int clock_source = 0;
	int division = 2;
	int adjustment = 2;
  #endif //USE_KEIL

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

	unsigned int result = get_cur_tick() - last_tick;
  if (poisoned) return (unsigned int)(result * (1.0 + 1.0 * (rand() % 13 + 8) / 100));
  else return result;
};

static unsigned int rtc_phra_task(unsigned int task, bool poisoned) {
  #ifdef USE_ESP32
  int wait_time = ((task) % 100) + 10;
  int phase_mod = (task >> 8) % 20000 + 100;
	int clock_source = 0;
	int division = 2;
	int adjustment = 125;
  #endif // USE_ESP32

  #ifdef USE_STM32F103
  int wait_time = ((task) % 100) + 10;
  int phase_mod = (task >> 8) % 20000 + 100;
	int clock_source = 0;
	int division = 2;
	int adjustment = 2;
	#endif // USE_STM32F103

  #ifdef USE_KEIL
  int wait_time = ((task) % 60) + 10;
  int phase_mod = (task >> 8) % 20000 + 100;
	int clock_source = 0;
	int division = 2;
	int adjustment = 2;
  #endif //USE_KEIL

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
	unsigned int result = phase;
  if (poisoned) return (unsigned int)(result * (1.0 + 1.0 * (rand() % 13 + 8) / 100));
  else return result;
};
