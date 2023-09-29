#include "rtc.h"

#if defined(USE_KEIL)
RTC_HandleTypeDef Rtc_Handle;

void rtc_setup(int clock_source, int division, int adjustment)  {
  RCC_OscInitTypeDef        RCC_OscInitStruct;
	RCC_PeriphCLKInitTypeDef  PeriphClkInitStruct;

	Rtc_Handle.Instance = RTC;
	Rtc_Handle.Init.AsynchPrediv = division;
	Rtc_Handle.Init.SynchPrediv  = adjustment;
	Rtc_Handle.Init.HourFormat   = RTC_HOURFORMAT_24;

	__HAL_RCC_PWR_CLK_ENABLE();
	HAL_PWR_EnableBkUpAccess();

	if (clock_source == 0) {
		RCC_OscInitStruct.OscillatorType =  RCC_OSCILLATORTYPE_LSI | RCC_OSCILLATORTYPE_LSE;
		RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
		RCC_OscInitStruct.LSIState = RCC_LSI_ON;
		RCC_OscInitStruct.LSEState = RCC_LSE_OFF;
		HAL_RCC_OscConfig(&RCC_OscInitStruct);

		PeriphClkInitStruct.PeriphClockSelection = RCC_PERIPHCLK_RTC;
		PeriphClkInitStruct.RTCClockSelection = RCC_RTCCLKSOURCE_LSI;
		HAL_RCCEx_PeriphCLKConfig(&PeriphClkInitStruct);
	} else if (clock_source == 1) {
		RCC_OscInitStruct.OscillatorType =  RCC_OSCILLATORTYPE_LSI | RCC_OSCILLATORTYPE_LSE;
		RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
		RCC_OscInitStruct.LSEState = RCC_LSE_ON;
		RCC_OscInitStruct.LSIState = RCC_LSI_OFF;
		HAL_RCC_OscConfig(&RCC_OscInitStruct);
		PeriphClkInitStruct.PeriphClockSelection = RCC_PERIPHCLK_RTC;
		PeriphClkInitStruct.RTCClockSelection = RCC_RTCCLKSOURCE_LSE;
		HAL_RCCEx_PeriphCLKConfig(&PeriphClkInitStruct);
	} else if (clock_source == 2) {
		RCC_OscInitStruct.OscillatorType =  RCC_OSCILLATORTYPE_HSE;
		RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
		RCC_OscInitStruct.LSEState = RCC_LSE_ON;
		RCC_OscInitStruct.LSIState = RCC_LSI_OFF;
		HAL_RCC_OscConfig(&RCC_OscInitStruct);
		PeriphClkInitStruct.PeriphClockSelection = RCC_PERIPHCLK_RTC;
		PeriphClkInitStruct.RTCClockSelection = RCC_RTCCLKSOURCE_HSE_DIV4;
		HAL_RCCEx_PeriphCLKConfig(&PeriphClkInitStruct);
	}

	__HAL_RCC_RTC_ENABLE();

	HAL_RTC_WaitForSynchro(&Rtc_Handle);

	if (HAL_RTC_Init(&Rtc_Handle) != HAL_OK)
	{
    DEBUG_LOG("\n\r RTC init fail \r\n");
	}
}

void rtc_set_time(void) {
  RTC_DateTypeDef  RTC_DateStructure;
  RTC_TimeTypeDef  RTC_TimeStructure;

	RTC_TimeStructure.TimeFormat = RTC_H12_AMorPM;
	RTC_TimeStructure.Hours = HOURS;
	RTC_TimeStructure.Minutes = MINUTES;
	RTC_TimeStructure.Seconds = SECONDS;
  HAL_RTC_SetTime(&Rtc_Handle,&RTC_TimeStructure, RTC_FORMAT_BIN);

	RTC_DateStructure.WeekDay = WEEKDAY;
	RTC_DateStructure.Date = DATE;
	RTC_DateStructure.Month = MONTH;
	RTC_DateStructure.Year = YEAR;
  HAL_RTC_SetDate(&Rtc_Handle,&RTC_DateStructure, RTC_FORMAT_BIN);

  HAL_RTCEx_BKUPWrite(&Rtc_Handle,RTC_BKP_DRX, RTC_BKP_DATA);
}

uint32_t rtc_get_second(void) {
  RTC_TimeTypeDef RTC_TimeStructure;
  HAL_RTC_GetTime(&Rtc_Handle, &RTC_TimeStructure, RTC_FORMAT_BIN);
	(void)RTC->DR;
  return (uint8_t)RTC_TimeStructure.Seconds;
}

#endif // end USE_KEIL

#if defined(USE_ESP32)

#include <stdlib.h>
#include <stdio.h>
#include <sys/time.h>
#include <unistd.h>
#include <soc/rtc_cntl_reg.h>
#include "soc/rtc.h"
#include "soc/rtc_periph.h"

void rtc_setup(int clock_source, int division, int adjustment) {
	rtc_clk_fast_freq_set(RTC_FAST_FREQ_8M); //RTC_SLOW_FREQ_RTC
	REG_SET_FIELD(RTC_CNTL_REG, RTC_CNTL_SCK_DCAP, adjustment);
	REG_SET_FIELD(RTC_CNTL_CLK_CONF_REG, RTC_CNTL_CK8M_DFREQ, adjustment);
	rtc_clk_divider_set(division);
	if (clock_source == 0) {
		rtc_clk_32k_enable(true);
		rtc_clk_slow_freq_set(RTC_SLOW_FREQ_RTC);
	} else if (clock_source == 1) {
		rtc_clk_8m_enable(true, true);
		rtc_clk_slow_freq_set(RTC_SLOW_FREQ_8MD256);
	}
	return;
};

void rtc_set_time(void){
	return;
};

uint32_t rtc_get_second(void){
  // ESP32's clock source is choosen in menuconfig
  SET_PERI_REG_MASK(RTC_CNTL_TIME_UPDATE_REG, RTC_CNTL_TIME_UPDATE);
  uint32_t t = READ_PERI_REG(RTC_CNTL_TIME0_REG);
  return t;
};


#endif // end USE_ESP32

#if defined(USE_STM32F103)

#include "stm32f1xx_hal.h"
#include "stm32f1xx_hal_rtc.h"
#include "stm32f1xx_hal_rcc.h"

static RTC_HandleTypeDef RTC_Handler;

void rtc_setup(int clock_source, int division, int adjustment) {
	RCC_OscInitTypeDef RCC_OscInitStruct;
	RCC_PeriphCLKInitTypeDef PeriphClkInitStruct;

	__HAL_RCC_PWR_CLK_ENABLE();
	HAL_PWR_EnableBkUpAccess();
	__HAL_RCC_BKP_CLK_ENABLE();
	
	RCC_OscInitStruct.OscillatorType=RCC_OSCILLATORTYPE_LSE;
	RCC_OscInitStruct.PLL.PLLState=RCC_PLL_NONE;
	RCC_OscInitStruct.LSEState=RCC_LSE_ON;
	
	if (clock_source == 0) {
		RCC_OscInitStruct.OscillatorType=RCC_OSCILLATORTYPE_LSI;
		RCC_OscInitStruct.LSIState=RCC_LSI_ON;
		HAL_RCC_OscConfig(&RCC_OscInitStruct);
		__HAL_RCC_RTC_CONFIG(RCC_RTCCLKSOURCE_LSI);
	} else if (clock_source == 1) {
		HAL_RCC_OscConfig(&RCC_OscInitStruct);
		PeriphClkInitStruct.PeriphClockSelection=RCC_PERIPHCLK_RTC;
		PeriphClkInitStruct.RTCClockSelection=RCC_RTCCLKSOURCE_LSE;
		HAL_RCCEx_PeriphCLKConfig(&PeriphClkInitStruct);
	}
	__HAL_RCC_RTC_ENABLE();

	RTC_Handler.Instance = RTC; 
	RTC_Handler.Init.AsynchPrediv=division + adjustment;
	HAL_RTC_Init(&RTC_Handler);
}

void rtc_set_time(void) {
	if(HAL_RTCEx_BKUPRead(&RTC_Handler,RTC_BKP_DR1)!=0X5050){
		
    RCC->APB1ENR|=1<<28;
    RCC->APB1ENR|=1<<27;
		PWR->CR|=1<<8;
		
		RTC->CRL|=1<<4;
		RTC->CNTL=0;
		RTC->CNTH=0;
		RTC->CRL&=~(1<<4);
		while(!(RTC->CRL&(1<<5)));

		HAL_RTCEx_BKUPWrite(&RTC_Handler,RTC_BKP_DR1, 0X5050);
	}
}

uint32_t rtc_get_second(void) {
	return (uint32_t)RTC->CNTL;
}

#endif // USE_STM32F103

