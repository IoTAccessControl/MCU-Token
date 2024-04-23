//
// Created by admin on 2024/4/23.
//

#ifndef MCU_TOKEN_CENCODE_H
#define MCU_TOKEN_CENCODE_H

#include <stddef.h>

// Base64编码状态结构体
typedef struct {
    int step;
    char result;
    int stepcount;
} base64_encodestate;

void base64_init_encodestate(base64_encodestate *state);

char base64_encode_value(char value_in);

int base64_encode_block(const char *plaintext_in, int length_in, char *code_out, base64_encodestate *state);

int base64_encode_blockend(char *code_out, base64_encodestate *state);

#endif //MCU_TOKEN_CENCODE_H
