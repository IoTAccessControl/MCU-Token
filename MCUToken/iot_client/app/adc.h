#ifndef _ADC_H
#define	_ADC_H

#if defined(USE_KEIL)
#include "stm32f4xx.h"
#include "stm32f4xx_hal_adc.h"
#include "utils.h"
#include "stm32f4xx_hal_dma.h"

#define RHEOSTAT_ADC                        ADC1
#define RHEOSTAT_ADC_CLK_ENABLE()           __ADC1_CLK_ENABLE()
#define RHEOSTAT_ADC_CHANNEL                ADC_CHANNEL_17

#define RHEOSTAT_NOFCHANEL      3

// PA4: DAC1
#define RHEOSTAT_ADC_GPIO_PORT1             GPIOA
#define RHEOSTAT_ADC_GPIO_PIN1              GPIO_PIN_4
#define RHEOSTAT_ADC_GPIO_CLK1_ENABLE()     __GPIOA_CLK_ENABLE()
#define RHEOSTAT_ADC_CHANNEL1               ADC_CHANNEL_4

// PA5：DAC2
#define RHEOSTAT_ADC_GPIO_PORT2             GPIOA
#define RHEOSTAT_ADC_GPIO_PIN2              GPIO_PIN_5
#define RHEOSTAT_ADC_GPIO_CLK2_ENABLE()     __GPIOA_CLK_ENABLE()
#define RHEOSTAT_ADC_CHANNEL2               ADC_CHANNEL_5

// CHANNEL17：V-ref
#define RHEOSTAT_ADC_GPIO_PORT3             GPIOC
#define RHEOSTAT_ADC_GPIO_PIN3              GPIO_PIN_5
#define RHEOSTAT_ADC_GPIO_CLK3_ENABLE()     __GPIOA_CLK_ENABLE()
#define RHEOSTAT_ADC_CHANNEL3               ADC_CHANNEL_17
   
// ADC1
#define RHEOSTAT_ADC                        ADC1
#define RHEOSTAT_ADC_CLK_ENABLE()           __ADC1_CLK_ENABLE()

// ADC DR
#define RHEOSTAT_ADC_DR_ADDR                ((uint32_t)ADC1+0x4c)

// ADC DMA
#define RHEOSTAT_ADC_DMA_CLK_ENABLE()       __DMA2_CLK_ENABLE()
#define RHEOSTAT_ADC_DMA_CHANNEL            DMA_CHANNEL_0
#define RHEOSTAT_ADC_DMA_STREAM             DMA2_Stream0

#endif

#if defined(USE_ESP32)
#include "driver/gpio.h"

#endif

#include "utils.h"


void adc_reference_init(void);
void adc_reference_stop(void);
void adc_multi_channel_init(void);
void adc_multi_channel_stop(void);
void adc_get_value(bool only_pwm);
void adc_get_ref_value(void);

#endif /* _ADC_H */
