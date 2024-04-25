//
// Created by admin on 2024/4/24.
//

#ifndef MCU_TOKEN_BASE64_H
#define MCU_TOKEN_BASE64_H
#include <stdint.h>

extern const char base64_chars[];

extern int base64_index(char c);

void base64_encode(const uint8_t *input, int input_len, char *output);

void base64_decode(const char *input, uint8_t *output, int input_len);
#endif //MCU_TOKEN_BASE64_H
