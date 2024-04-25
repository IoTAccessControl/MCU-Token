//
// Created by admin on 2024/4/24.
//

#include "base64.h"

const char base64_chars[] =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        "0123456789+/";

void base64_encode(const uint8_t *input, int input_len, char *output) {
    int i = 0, j = 0;
    uint8_t arr_3[3];
    uint8_t arr_4[4];
    const uint8_t *current = input;
    while (input_len--) {
        arr_3[i++] = *current++;
        if (i == 3) {
            arr_4[0] = (arr_3[0] & 0xfc) >> 2;
            arr_4[1] = ((arr_3[0] & 0x03) << 4) + ((arr_3[1] & 0xf0) >> 4);
            arr_4[2] = ((arr_3[1] & 0x0f) << 2) + ((arr_3[2] & 0xc0) >> 6);
            arr_4[3] = arr_3[2] & 0x3f;

            for (i = 0; i < 4; i++)
                output[j++] = base64_chars[arr_4[i]];
            i = 0;
        }
    }

    if (i) {
        for (int k = i; k < 3; k++)
            arr_3[k] = '\0';

        arr_4[0] = (arr_3[0] & 0xfc) >> 2;
        arr_4[1] = ((arr_3[0] & 0x03) << 4) + ((arr_3[1] & 0xf0) >> 4);
        arr_4[2] = ((arr_3[1] & 0x0f) << 2) + ((arr_3[2] & 0xc0) >> 6);
        arr_4[3] = arr_3[2] & 0x3f;

        for (int k = 0; k < i + 1; k++)
            output[j++] = base64_chars[arr_4[k]];

        while (i++ < 3)
            output[j++] = '=';
    }

    output[j] = '\0';
}

int base64_index(char c) {
    if (c >= 'A' && c <= 'Z') return c - 'A';
    if (c >= 'a' && c <= 'z') return c - 'a' + 26;
    if (c >= '0' && c <= '9') return c - '0' + 52;
    if (c == '+') return 62;
    if (c == '/') return 63;
    return -1;  // 对于非法字符或'='，返回-1
}

void base64_decode(const char *input, uint8_t *output, int input_len) {
    int i = 0, j = 0;
    int in_ = 0;
    uint8_t char_array_4[4], char_array_3[3];

    while (in_ < input_len && input[in_] != '=') {
        // Skip invalid characters
        if (input[in_] && base64_index(input[in_]) != -1) {
            char_array_4[i++] = input[in_]; in_++;
            if (i == 4) {
                for (i = 0; i < 4; i++)
                    char_array_4[i] = base64_index(char_array_4[i]);

                char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
                char_array_3[1] = ((char_array_4[1] & 0x0F) << 4) + ((char_array_4[2] & 0x3C) >> 2);
                char_array_3[2] = ((char_array_4[2] & 0x03) << 6) + char_array_4[3];

                for (i = 0; (i < 3); i++)
                    output[j++] = char_array_3[i];
                i = 0;
            }
        } else {
            in_++; // Skip invalid character
        }
    }

    if (i) {
        for (int k = 0; k < i; k++)
            char_array_4[k] = base64_index(char_array_4[k]);

        char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
        if (i > 2) char_array_3[1] = ((char_array_4[1] & 0x0F) << 4) + ((char_array_4[2] & 0x3C) >> 2);

        for (int k = 0; (k < i - 1); k++)
            output[j++] = char_array_3[k];
    }
}
