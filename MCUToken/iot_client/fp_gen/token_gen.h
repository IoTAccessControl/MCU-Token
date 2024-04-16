#ifndef _TOKEN_GEN_
#define _TOKEN_GEN_

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

int token_generate(int argc, char *argv[]);
void generator_token(const char *operation, const char* nonce, const char** payloads);

typedef unsigned int (*task_token_func)(unsigned int, bool);

typedef struct task_token_func_multi {
	int tid;
	task_token_func func;
} task_token_func_multi;


#endif // _TOKEN_GEN_
