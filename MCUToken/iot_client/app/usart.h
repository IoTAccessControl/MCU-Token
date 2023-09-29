#ifndef USART_H_
#define USART_H_
#include <stdint.h>
#include <stdarg.h>
#include <stdbool.h>

// usart shell support
char shell_get_char(void);
void shell_put_str(const uint8_t *buf, int len);

// usart log print
void log_print_porting(const char *fmt, va_list *args);

// usart data transfer
enum DataType {
	PKT_LOG = 1,
	PKT_DATA,
};

void usart_reset(void);
/*
	@param: ty
	@param: buf
	@param: len
	@param: change_line, '\n' -> '\r\n'
*/
void uasrt_send_pkt(int ty, const uint8_t *buf, int len, bool change_line);

#endif
