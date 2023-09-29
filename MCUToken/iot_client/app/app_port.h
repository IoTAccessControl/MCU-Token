#ifndef APP_PORT_H_
#define APP_PORT_H_
#include <stdint.h>
#include <stdarg.h>
#include <stdbool.h>

#ifdef DEV_NRF52840
#define SYSCoreClock 64000000 // 64mhz

#elif defined(DEV_STM32L475)
#define SYSCoreClock 80000000 // 80mhz

#elif defined(DEV_STM32F429)
#define SYSCoreClock 180000000 // 180mhz

#else

#define SYSCoreClock 100000000 // 100mhz

#endif // DEV_NRF52840 Clock

// USE_KEIL -> STM32_HAL


// implemented by devices
char usart_getchar(void);
void uart_putchar(char ch);
// use LED to notify fault
void show_error(void);

// used in esp32
void task_sleep(void);

#endif
