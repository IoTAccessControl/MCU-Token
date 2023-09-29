#include "usart.h"
#include <stdio.h>
#include <string.h>
#include "app_port.h"

char shell_get_char(void) {
	return usart_getchar();
}

void shell_put_str(const uint8_t *buf, int len) {
	uasrt_send_pkt(PKT_LOG, buf, len, true);
}

void log_print_porting(const char *fmt, va_list *args) {
	char buf[256] = {0};
	vsprintf(buf, fmt, *args);
	//vprintf(fmt, *args);
	uasrt_send_pkt(PKT_LOG, (uint8_t *) buf, strlen(buf), true);
}

void usart_reset(void) {
	for (int i = 0; i < 20; i++) {
		uart_putchar(0);
	}
}

void uasrt_send_pkt(int ty, const uint8_t *buf, int len, bool change_line) {
	int pos = 0;
	while (len > 255) {
		uasrt_send_pkt(ty, buf + pos, (char) 255, change_line);
		len -= 255;
		pos += 255;
	}

	buf = buf + pos;
	uart_putchar((char) ty);

	if (change_line) { // need to transfer /n to /r/n
		int add_lrln = 0;
		for (int i = 0; i < len; i++) {
			if (buf[i] == '\n') {
				add_lrln++;
			}
		}

		uart_putchar((char) len + add_lrln);
		for (int i = 0; i < len; i++) {
			if (buf[i] == '\n') {
				uart_putchar('\r');
			}
			uart_putchar(buf[i]);
		}
	} else {
		uart_putchar((uint8_t) len);
		for (int i = 0; i < len; i++) {
			uart_putchar(buf[i]);
		}
	}
}
