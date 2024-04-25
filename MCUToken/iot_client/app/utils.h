#ifndef UTILS_H_
#define UTILS_H_

#include <stdio.h>
#include <stdint.h>
#include "device_data.h"
#include "defs.h"

void debug_log(const char *fmt, ...);

// defined in defs.h
#ifdef DEBUG
#define DEBUG_LOG(...)								\
do {												\
	debug_log(__VA_ARGS__);							\
} while (0)
#else
#define DEBUG_LOG(...) do {} while(0)
#endif // end DEBUG

/*
Used in the debug of evaluation functions. Defined in defs.h
*/
#ifdef USE_TEST_LOG
#define TEST_LOG(...)								\
do {												\
	debug_log(__VA_ARGS__);							\
} while (0)
#else
#define TEST_LOG(...) do {} while(0)
#endif // end TEST_LOG

#ifdef USE_FP_LOG
#define FP_LOG(...)								\
do {												\
	debug_log(__VA_ARGS__);							\
} while (0)
#else
#define FP_LOG(...) do {} while(0)
#endif // end TEST_LOG


#define int2str(s, n) \
char t[10]; \
itoa((n), (char*)t, 10); \
s = t

char* itoa(int num, char* str, int base);
char* utoa(unsigned int num, char* str, int base);
int str2int(char *str);
int byte2int(uint8_t *buf, int len); // little_edian
int count_bit(int num);

void str_split(char *src,const char *separator,char **dest,int *num);

void dump_bin(uint8_t *data, int len);

uint32_t little_endian_16_bit(uint32_t val);

#endif
