#include "timer.h"
#include <stdbool.h>

// static bool profiler_is_init = false;
static uint32_t ticks_per_us = 1000;

#ifdef DEV_NRF52840
#define SYSCoreClock 64000000 // 64mhz

#elif defined(DEV_STM32L475)
#define SYSCoreClock 80000000 // 80mhz

#elif defined(DEV_STM32F429)
#define SYSCoreClock 180000000 // 180mhz

#else
#define SYSCoreClock 100000000 // 100mhz
#endif // DEV_NRF52840

#ifdef SYS_CORTEX_M4

#define COREDEBUG_DEMCR  (volatile uint32_t *) (0xE000EDFC)
#define DWT_CTRL (volatile uint32_t *) (0xE0001000) // page e156
#define DWT_CYCCNT (volatile uint32_t *) (0xE0001004) // page e156
#define MSK_DEMCR_TRCENA (1 << 24) // page 464
#define MSK_DWT_CYCCNTENA (1 << 0) // page e159

static inline void dwt_init(void) {
	ticks_per_us = SYSCoreClock / 1000000;
	*COREDEBUG_DEMCR |= MSK_DEMCR_TRCENA;
	*DWT_CYCCNT = 0;
	*DWT_CTRL |= MSK_DWT_CYCCNTENA;
}

// static inline void dwt_deinit(void) {
// 	*DWT_CTRL &= ~MSK_DWT_CYCCNTENA;
// 	*DWT_CYCCNT = 0;
// 	*COREDEBUG_DEMCR &= ~MSK_DEMCR_TRCENA;
// }

static inline uint32_t dwt_get_counter(void) {
	return *DWT_CYCCNT;
}

#endif // SYS_CORTEX_M4

#if defined(USE_ESP32)

#include <stdlib.h>
#include <stdio.h>
#include <sys/time.h>
#include <unistd.h>
#include "soc/systimer_reg.h"
#include "utils.h"

static inline void dwt_init() {
	*(unsigned int*)SYSTIMER_CONF_REG |= SYSTIMER_CLK_EN_M;
	*(unsigned int*)SYSTIMER_LOAD_LO_REG = 0;
	*(unsigned int*)SYSTIMER_LOAD_HI_REG = 0;
	*(unsigned int*)SYSTIMER_LOAD_REG |= SYSTIMER_TIMER_LOAD_M;
	*(unsigned int*)SYSTIMER_UPDATE_REG |= SYSTIMER_TIMER_UPDATE_M;
	while(!((*(unsigned int*)SYSTIMER_UPDATE_REG) & SYSTIMER_TIMER_VALUE_VALID_M));
}

// static inline void dwt_deinit() {
// }

static inline uint32_t dwt_get_counter() {
	*(unsigned int*)SYSTIMER_UPDATE_REG |= SYSTIMER_TIMER_UPDATE_M;
	while(!((*(unsigned int*)SYSTIMER_UPDATE_REG) & SYSTIMER_TIMER_VALUE_VALID_M));
	if ((*(unsigned int*)SYSTIMER_VALUE_HI_REG) != 0) {
		printf("ERROR IN Timer!\n");
		return 0;
	}
	return  *(unsigned int*)SYSTIMER_VALUE_LO_REG;
	// struct timeval tv_now;
	// gettimeofday(&tv_now, NULL);
	// uint32_t time_us = (uint32_t)tv_now.tv_sec * 1000000L + (uint32_t)tv_now.tv_usec;
	// return time_us;
}
#endif // USE_ESP32

#ifdef USE_STM32F103

#define COREDEBUG_DEMCR  (volatile uint32_t *) (0xE000EDFC)
#define DWT_CTRL (volatile uint32_t *) (0xE0001000) // page e156
#define DWT_CYCCNT (volatile uint32_t *) (0xE0001004) // page e156
#define MSK_DEMCR_TRCENA (1 << 24) // page 464
#define MSK_DWT_CYCCNTENA (1 << 0) // page e159

static inline void dwt_init(void) {
	*COREDEBUG_DEMCR |= MSK_DEMCR_TRCENA;
	*DWT_CYCCNT = 0;
	*DWT_CTRL |= MSK_DWT_CYCCNTENA;
}

// static inline void dwt_deinit(void) {
// 	*DWT_CTRL &= ~MSK_DWT_CYCCNTENA;
// 	*DWT_CYCCNT = 0;
// 	*COREDEBUG_DEMCR &= ~MSK_DEMCR_TRCENA;
// }

static inline uint32_t dwt_get_counter(void) {
	return *DWT_CYCCNT;
}
#endif //USE_STM32F103

void reset_timer_tick(void) {
	dwt_init();
}

uint32_t get_cur_tick(void) {
	return dwt_get_counter();
}

float tick_to_us(int tick) {
	return tick / (float) ticks_per_us;
}
