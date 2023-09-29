#ifndef RTC_H_
#define RTC_H_

#include "defs.h"
#include "app_port.h"
#include "utils.h"

#ifdef USE_KEIL

#include "stm32f4xx.h"
#include "stm32f4xx_hal_rtc.h"
#include "stm32f4xx_hal_cortex.h"

// clock source
#define RTC_CLOCK_SOURCE_LSE
// #define RTC_CLOCK_SOURCE_LSI
// #define RTC_CLOCK_SOURCE_HSE

#define ASYNCHPREDIV         0X01
#define SYNCHPREDIV          0X01

#define RTC_H12_AMorPM			  RTC_HOURFORMAT12_AM
#define HOURS                     1          // 0~23
#define MINUTES                   1          // 0~59
#define SECONDS                   1          // 0~59

#define WEEKDAY                   1         // 1~7
#define DATE                      1         // 1~31
#define MONTH                     1         // 1~12
#define YEAR                      1         // 0~99

#define RTC_Format_BINorBCD  RTC_FORMAT_BIN

#define RTC_BKP_DRX          RTC_BKP_DR0

#define RTC_BKP_DATA         0X32F2

#endif // USE_KEIL

void rtc_setup(int clock_source, int division, int adjustment);
void rtc_set_time(void);
uint32_t rtc_get_second(void);

#endif // RTC_H_
