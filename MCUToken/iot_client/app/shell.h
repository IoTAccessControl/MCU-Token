#ifndef SHELL_H_
#define SHELL_H_

#include <stddef.h>

typedef struct ShellCommand {
	const char *command;
	int (*handler)(int argc, char *argv[]);
	const char *help;
} sShellCommand;

extern const sShellCommand *const g_shell_commands;
extern const size_t g_num_shell_commands;

void run_shell_cli(void);
void shell_printf(char *fmt, ...);

#endif
