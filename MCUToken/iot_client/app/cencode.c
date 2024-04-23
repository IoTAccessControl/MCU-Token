//
// Created by admin on 2024/4/23.
//

#include "cencode.h"

static const char* BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

void base64_init_encodestate(base64_encodestate* state) {
    state->step = 0;
    state->result = 0;
    state->stepcount = 0;
}

char base64_encode_value(char value_in) {
    if (value_in > 63) return '=';
    return BASE64_CHARS[value_in];
}

int base64_encode_block(const char* plaintext_in, int length_in, char* code_out, base64_encodestate* state) {
    const char* plainchar = plaintext_in;
    const char* const plaintextend = plaintext_in + length_in;
    char* codechar = code_out;
    char result;
    char fragment;

    result = state->result;

    switch (state->step) {
        while (1) {
            case 0:
                if (plainchar == plaintextend) {
                    state->result = result;
                    state->step = 0;
                    return codechar - code_out;
                }
            fragment = *plainchar++;
            result = (fragment & 0x0fc) >> 2;
            *codechar++ = base64_encode_value(result);
            result = (fragment & 0x003) << 4;
            case 1:
                if (plainchar == plaintextend) {
                    state->result = result;
                    state->step = 1;
                    return codechar - code_out;
                }
            fragment = *plainchar++;
            result |= (fragment & 0x0f0) >> 4;
            *codechar++ = base64_encode_value(result);
            result = (fragment & 0x00f) << 2;
            case 2:
                if (plainchar == plaintextend) {
                    state->result = result;
                    state->step = 2;
                    return codechar - code_out;
                }
            fragment = *plainchar++;
            result |= (fragment & 0x0c0) >> 6;
            *codechar++ = base64_encode_value(result);
            result  = (fragment & 0x03f) >> 0;
            *codechar++ = base64_encode_value(result);
            break;
        }
    }
    // Control should not reach here
    return codechar - code_out;
}

int base64_encode_blockend(char* code_out, base64_encodestate* state) {
    char* codechar = code_out;
    switch (state->step) {
        case 1:
            *codechar++ = base64_encode_value(state->result);
            *codechar++ = '=';
            *codechar++ = '=';
            break;
        case 2:
            *codechar++ = base64_encode_value(state->result);
            *codechar++ = '=';
            break;
    }
    return codechar - code_out;
}