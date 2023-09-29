#include "sys.h"
#include "delay.h"
#include "bsp_usart.h"
#include "app_port.h"
#include "shell.h"
#include "main.h"
#include "iwdg.h"

// #define USE_STM32F103

int main(void) {
	HAL_Init();  
	Stm32_Clock_Init(RCC_PLL_MUL9);
	delay_init(72);
	uart_init(115200);
	wdg_init();
	run_shell_cli();
}
