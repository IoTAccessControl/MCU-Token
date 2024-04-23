//
// Created by admin on 2024/4/23.
//

#include "cdecode.h"

int base64_decode_value(char value_in) {
    static const char decoding[] = {62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1,
                                    -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
                                    22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
                                    37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51};
    static const char *decodingBase = decoding - 43;
    if (value_in < 43) {
        return -1;
    }
    return decodingBase[value_in];
}

void base64_init_decodestate(base64_decodestate *state) {
    state->step = 0;
    state->plainchar = 0;
}

int base64_decode_block(const char *code_in, const int length_in, char *plaintext_out, base64_decodestate *state) {
    const char *codechar = code_in;
    char *plainchar = plaintext_out;
    char fragment;

    *plainchar = state->plainchar;

    switch (state->step) {
        while (1) {
            case 0:
                do {
                    if (codechar == code_in + length_in) {
                        state->step = 0;
                        state->plainchar = *plainchar;
                        return plainchar - plaintext_out;
                    }
                    fragment = (char) base64_decode_value(*codechar++);
                } while (fragment < 0);
            *plainchar = (fragment & 0x03f) << 2;
            case 1:
                do {
                    if (codechar == code_in + length_in) {
                        state->step = 1;
                        state->plainchar = *plainchar;
                        return plainchar - plaintext_out;
                    }
                    fragment = (char) base64_decode_value(*codechar++);
                } while (fragment < 0);
            *plainchar++ |= (fragment & 0x030) >> 4;
            *plainchar = (fragment & 0x00f) << 4;
            case 2:
                do {
                    if (codechar == code_in + length_in) {
                        state->step = 2;
                        state->plainchar = *plainchar;
                        return plainchar - plaintext_out;
                    }
                    fragment = (char) base64_decode_value(*codechar++);
                } while (fragment < 0);
            *plainchar++ |= (fragment & 0x03c) >> 2;
            *plainchar = (fragment & 0x003) << 6;
            case 3:
                do {
                    if (codechar == code_in + length_in) {
                        state->step = 3;
                        state->plainchar = *plainchar;
                        return plainchar - plaintext_out;
                    }
                    fragment = (char) base64_decode_value(*codechar++);
                } while (fragment < 0);
            *plainchar++ |= (fragment & 0x03f);
        }
    }
    // Control should not reach here
    return plainchar - plaintext_out;
}