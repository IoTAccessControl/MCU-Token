#include "dac.h"

#if defined(USE_KEIL)

void dac_gpio_init(void);

GPIO_InitTypeDef GPIO_InitStruct;
void dac_gpio_init(void) {
	__GPIOA_CLK_ENABLE();
	/* DAC GPIO ---> PA5 */
	GPIO_InitStruct.Pin = GPIO_PIN_5;
	GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

	GPIO_InitStruct.Pin = GPIO_PIN_4;
	GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}

DAC_HandleTypeDef DAC_Config;

void dac_init(enum dac_op op) {
	// GPIO
	dac_gpio_init();

	// DAC_CLK
	DAC_ChannelConfTypeDef Channel_Config;
	__HAL_RCC_DAC_CLK_ENABLE();
	
	/* DAC Initialization */
	DAC_Config.Instance = DAC;
	HAL_DAC_Init(&DAC_Config);

	Channel_Config.DAC_Trigger = DAC_TRIGGER_SOFTWARE; //DAC_TRIGGER_T6_TRGO;
	Channel_Config.DAC_OutputBuffer = DAC_OUTPUTBUFFER_ENABLE;
	HAL_DAC_ConfigChannel(&DAC_Config, &Channel_Config, DAC_CHANNEL_2);

	Channel_Config.DAC_Trigger = DAC_TRIGGER_SOFTWARE; //DAC_TRIGGER_T6_TRGO;
	Channel_Config.DAC_OutputBuffer = DAC_OUTPUTBUFFER_ENABLE;
	HAL_DAC_ConfigChannel(&DAC_Config, &Channel_Config, DAC_CHANNEL_1);


	HAL_DAC_Start(&DAC_Config, DAC_CHANNEL_2);
	HAL_DAC_Start(&DAC_Config, DAC_CHANNEL_1);
}

void dac_stop(enum dac_op op) {
	HAL_DAC_SetValue(&DAC_Config, DAC_CHANNEL_2, DAC_ALIGN_12B_R, 0);
	HAL_DAC_SetValue(&DAC_Config, DAC_CHANNEL_1, DAC_ALIGN_12B_R, 0);

	HAL_DAC_Stop(&DAC_Config, DAC_CHANNEL_2);
	HAL_DAC_Stop(&DAC_Config, DAC_CHANNEL_1);

	HAL_DAC_DeInit(&DAC_Config);
	HAL_DAC_Init(&DAC_Config);

	__HAL_RCC_DAC_CLK_DISABLE();

	HAL_GPIO_DeInit(GPIOA, GPIO_PIN_5);
	HAL_GPIO_DeInit(GPIOA, GPIO_PIN_4);
};

uint32_t dac_set_value(int val) {
	// HAL_DAC_SetValue(&DAC_Config, DAC_CHANNEL_2, DAC_ALIGN_12B_R, val);
	// HAL_DAC_SetValue(&DAC_Config, DAC_CHANNEL_1, DAC_ALIGN_12B_R, val);
	__IO uint32_t tmp = 0UL;
	tmp = (uint32_t)DAC_Config.Instance;
	tmp += DAC_DHR12RD_ALIGNMENT(DAC_ALIGN_12B_R);
	uint16_t data = (uint16_t) val;
	*(__IO uint32_t *) tmp = data + (data << 16);
	HAL_DAC_Start(&DAC_Config, DAC_CHANNEL_2);
	HAL_DAC_Start(&DAC_Config, DAC_CHANNEL_1);

	return DAC->DOR1 == DAC->DOR2 ? DAC->DOR1 : 0xFFFFFFF;
};

#endif // USE_KEIL

#if defined(USE_ESP32)

#include "driver/dac.h"
#include <driver/adc.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"

void dac_init(enum dac_op op){
	dac_output_enable(DAC_CHANNEL_1);
	dac_output_enable(DAC_CHANNEL_2);
}

void dac_stop(enum dac_op op){
	ESP_ERROR_CHECK(dac_output_voltage(DAC_CHANNEL_1, 0));
	ESP_ERROR_CHECK(dac_output_voltage(DAC_CHANNEL_2, 0));
	dac_output_disable(DAC_CHANNEL_1);
	dac_output_disable(DAC_CHANNEL_2);
}

uint32_t dac_set_value(int val){
	int prev_val = val;

	val %= 256;
	dac_init(DAC_OP_VALUE);

	/* GPIO 17*/
	ESP_ERROR_CHECK(dac_output_voltage(DAC_CHANNEL_1, val));
	/* GPIO 18*/
	ESP_ERROR_CHECK(dac_output_voltage(DAC_CHANNEL_2, val));
	return prev_val;
};

#endif // end USE_ESP32

#if defined(USE_STM32F103)

#include "stm32f1xx_hal.h"
#include "stm32f1xx_hal_dac.h"
#include "stm32f1xx_hal_dac_ex.h"
#include "stm32f1xx_hal_adc.h"
#include "stm32f1xx_hal_spi.h"
// static DAC_HandleTypeDef DAC2_Handler;
// DAC is not exist on our STM32F103 board, we use external voltage as input.

static SPI_HandleTypeDef SPI2_Handler; 

void dac_init(enum dac_op op) {
}

void dac_stop(enum dac_op op) {
}

int adc_read_type = 0;
uint32_t dac_set_value(int val) {
	adc_read_type = val;
	return val;
}

#endif // USE_STM32F103
