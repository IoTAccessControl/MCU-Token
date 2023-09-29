#include "app_port.h"

// should be override
__attribute__((weak)) char usart_getchar(void) {
	show_error();
#if !defined(USE_KEIL) && defined(SYS_CORTEX_M4)
	asm("bkpt");
#endif
	return 0;
}

__attribute__((weak)) void uart_putchar(char ch) {
	(void) ch;
	show_error();
#if !defined(USE_KEIL) && defined(SYS_CORTEX_M4)
	asm("bkpt");
#endif
}

__attribute__((weak)) void show_error(void) {}

__attribute__((weak)) void task_sleep(void) {}
