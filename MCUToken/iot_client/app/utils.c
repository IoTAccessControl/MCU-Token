#include "utils.h"
#include <stdarg.h>
#include <string.h>

#ifdef DEBUG

extern void log_print_porting(const char *fmt, va_list *args);

void debug_log(const char *fmt, ...) {
	va_list args;
	va_start(args, fmt);
	log_print_porting(fmt, &args);
	va_end(args);
}

#else
void debug_log(const char *fmt, ...) {}
#endif // end DEBUG

int str2int(char *str) {
	int val = 0;
	for (const char *c = str; *c != '\0'; c++) {
		val *= 10;
		val += *c - '0';
	}
	return val;
};

int byte2int(uint8_t *buf, int len) {
	int val = 0;
	for (int i = 0; i < len; i++) {
		val *= 256;
		val += (int) buf[i];
	}
	return val;
};

void dump_bin(uint8_t *data, int len) {
	DEBUG_LOG("dump bin:\n");
	for (int i = 0; i < len; i++) {
		DEBUG_LOG("\\x%02x", data[i]);
	}
	DEBUG_LOG("\n");
}

uint32_t little_endian_16_bit(uint32_t val) {
	return ((val & 0xFFFF0000) >> 16) | ((val & 0x0000FFFF) << 16);
}

void str_split(char *src,const char *separator,char **dest,int *num) {
     char *pNext;
     int count = 0;
     if (src == NULL || strlen(src) == 0) {
		return;
	 }

     if (separator == NULL || strlen(separator) == 0) {
		return;
	 }
	char *strtok(char *str, const char *delim);
    pNext = strtok(src,separator);
    while(pNext != NULL) {
        *dest++ = pNext;
        ++count;
        pNext = strtok(NULL,separator);
    }
    *num = count;
}

int count_bit(int num) {
	int count = 0;
	while (num) {
		count += 1;
		num = num >> 1;
	}
	return count;
};

#if defined(USE_KEIL) || defined(USE_STM32F103)
//function to reverse a string
void reverse(char str[], int length) {
	int start;
	int end = length -1;
	for(start = 0; start < end; ++start, --end) {
		const char ch = str[start];
		str[start] = str[end];
		str[end] = ch;
	}
}

//Implemented own itoa function
char* itoa(int num, char* str, int base) {
	int i = 0;
	char isNegNum = 0;
	/*Handle 0 explicitly, 
		otherwise empty string is printed for 0 */
	if (num == 0) {
		str[i++] = '0';
		str[i] = '\0';
	}
	else {
		// In library itoa function -ve numbers handled only with
		// base 10. SO here we are also following same concept
		if ((num < 0) && (base == 10)) {
			isNegNum = 1;
			num = -num; // make num positive
		}
		// Process individual digits
		do {
			const int rem = (num % base);
			str[i++] = (rem > 9)? ((rem-10) + 'a') : (rem + '0');
			num = num/base;
		} while (num != 0);
		// If number is negative, append '-'
		if (isNegNum){
			str[i++] = '-';
		}
		// Append string terminator
		str[i] = '\0';
		// Reverse the string
		reverse(str, i);
	}
	return str;
}

char* utoa(unsigned int num, char* str, int base) {
	int i = 0;
	/*Handle 0 explicitly, 
		otherwise empty string is printed for 0 */
	if (num == 0) {
		str[i++] = '0';
		str[i] = '\0';
	}
	else {
		// Process individual digits
		do {
			const unsigned int rem = (num % base);
			str[i++] = (rem > 9)? ((rem-10) + 'a') : (rem + '0');
			num = num/base;
		} while (num != 0);
		// Append string terminator
		str[i] = '\0';
		// Reverse the string
		reverse(str, i);
	}
	return str;
}
#endif // USE_KEIL
