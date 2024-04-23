//
// Created by admin on 2024/4/23.
//

#ifndef MCU_TOKEN_CDECODE_H
#define MCU_TOKEN_CDECODE_H

#include <stddef.h>


// Base64解码状态结构体
typedef struct {
    int step;
    char plainchar;
} base64_decodestate;

void base64_init_decodestate(base64_decodestate *state);

int base64_decode_block(const char *code_in, const int length_in, char *plaintext_out, base64_decodestate *state);

#endif //MCU_TOKEN_CDECODE_H
