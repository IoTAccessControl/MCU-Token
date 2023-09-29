// main of ESP32
#ifndef USE_ESP32
#define USE_ESP32
#endif


#include <stdio.h>
#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "driver/ledc.h"
#include "esp_rom_uart.h"
#include <errno.h>
#include <unistd.h>
#include "driver/uart.h"
#include "driver/gpio.h"

#include "app_port.h"
#include "shell.h"
#include "usart.h"
#include "esp_log.h"

/* watch dog */
void task_sleep(void) {
    vTaskDelay(10 / portTICK_PERIOD_MS);
}

char usart_getchar(void) {
    uint8_t ch = 0;
    while (1) {
        if (uart_read_bytes(UART_NUM_0, &ch, 1, 20 / portTICK_PERIOD_MS)) {
            return ch;
        }
        task_sleep();
    }
    return ch;
}


void uart_putchar(char ch) {
    uart_write_bytes(UART_NUM_0, &ch, 1);
}

void show_error() {
    ledc_set_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, 8191);
    ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0);
}

int _write(int file, char *ptr, int len)
{
	int i = len;

	if (file == STDOUT_FILENO || file == STDERR_FILENO) {
		shell_put_str((uint8_t *) ptr, len);
		return i;
	}
	errno = EIO;
	return -1;
}

void app_main(void)
{
    esp_log_level_set("*", ESP_LOG_ERROR);

    const int uart_num = UART_NUM_0;
    uart_config_t uart_config = {
        .baud_rate = 115200,		
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
    };
    uart_param_config(uart_num, &uart_config);
    uart_set_pin(uart_num , GPIO_NUM_43, GPIO_NUM_44, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    const int uart_buffer_size = (1024 * 2);
    uart_driver_install(uart_num , uart_buffer_size, 0, 0, NULL, 0);

    run_shell_cli();
}
