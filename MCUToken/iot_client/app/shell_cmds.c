
#include <stddef.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdint.h>
#include <string.h>

#include "utils.h"
#include "shell.h"
#include "defs.h"
// avoid the circle depencies
//explore here to add new function
#include "dev_reg.h"


#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof(arr[0]))


static int cmd_dev_reg(int argc, char *argv[]) {
    return dev_reg(argc, argv);
}

static const sShellCommand s_shell_commands[] = {
    {"dev_reg", cmd_dev_reg, "Register the device"},
};

const sShellCommand *const g_shell_commands = s_shell_commands;
const size_t g_num_shell_commands = ARRAY_SIZE(s_shell_commands);
