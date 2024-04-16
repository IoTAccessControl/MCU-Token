
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

//这里的引用没问题，重新使用clion打开文件就能正常使用
#include "fp_gen.h"
#include "token_gen.h"
#include "dev_reg.h"


#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof(arr[0]))

static int cmd_show_version(int argc, char *argv[]) {
	(void) argc;
	(void) argv;
	printf("Version %s!\n", VERSION);
	return 0;
}

static int cmd_start_data_collect(int argc, char *argv[]) {
	if (argc >= 4) {
		if (strcmp(argv[1], "STM32") == 0 || strcmp(argv[1], "ESP32S2") == 0) {
			// send_buf();
			return start_data_collect(argc, argv);
		}
	} else {
		DEBUG_LOG("Incorrect command args, Usage:\n \tfp_gen plat fp_type fp_round\n");
	}
	return 0;
}

static int cmd_generate_token(int argc, char *argv[]) {
	if (argc >= 2) {
		return token_generate(argc, argv);
	} else {
		DEBUG_LOG("Incorrect command args, Usage:\n \tfp_gen plat fp_type fp_round\n");
	}
	return 0;
}

static int cmd_dev_reg(int argc, char *argv[]) {
    return dev_reg(argc, argv);
}

static const sShellCommand s_shell_commands[] = {
	{"version", cmd_show_version, "Show Version Code"},
	{"fp_gen", cmd_start_data_collect, "fp_gen STM32. Generate fringerprint data for specific platforms."},
	{"token_gen", cmd_generate_token, "Generate token for the target command"},
    {"dev_reg", cmd_dev_reg, "Register the device"},
};

const sShellCommand *const g_shell_commands = s_shell_commands;
const size_t g_num_shell_commands = ARRAY_SIZE(s_shell_commands);
