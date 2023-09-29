#include "iwdg.h"

#ifdef USE_KEIL

#include "stm32f4xx.h"
#include "stm32f4xx_hal_iwdg.h"

IWDG_HandleTypeDef IWDG_Handle;

void wdg_init(void) {
	uint8_t prv = IWDG_PRESCALER_256;
	uint16_t rlv = 1875;
	IWDG_Handle.Instance = IWDG;
	IWDG_Handle.Init.Prescaler = prv;
	IWDG_Handle.Init.Reload = rlv;

	HAL_IWDG_Init(&IWDG_Handle);
	__HAL_IWDG_START(&IWDG_Handle);
}
void wdg_feed(void){
	HAL_IWDG_Refresh(&IWDG_Handle);
}

#endif // USE_KEIL

#ifdef USE_ESP32

#include "esp_task_wdt.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

void esp_task_wdt_isr_user_handler() {
    esp_restart();
}

void wdg_init(void) {
	esp_task_wdt_init(10, false);
	esp_task_wdt_add(NULL);
}

void wdg_feed(void) {
	esp_task_wdt_reset();
	vTaskDelay(10 / portTICK_PERIOD_MS);
}

#endif // USE_ESP32

#if defined(USE_STM32F103)

#include "stm32f1xx.h"
#include "stm32f1xx_hal_iwdg.h"

static IWDG_HandleTypeDef IWDG_Handler;

void wdg_init(void) {
	IWDG_Handler.Instance=IWDG;
	IWDG_Handler.Init.Prescaler=IWDG_PRESCALER_256;
	IWDG_Handler.Init.Reload=500*60;
	HAL_IWDG_Init(&IWDG_Handler);
	HAL_IWDG_Start(&IWDG_Handler);
}

void wdg_feed(void) {
	HAL_IWDG_Refresh(&IWDG_Handler);
}

#endif // USE_STM32F103

