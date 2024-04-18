#include <string.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdbool.h>

#include "app_port.h"
#include "shell.h"
#include "usart.h"

// receive buffer from USART
//extern int usart_read_buf(unsigned char *buf, int len);

#define SHELL_BUFFER_SIZE 128
#define SHELL_PROMPT "$ "
#define SHELL_FOR_EACH_COMMAND(command) \
	for (const sShellCommand *command = g_shell_commands; \
		command < &g_shell_commands[g_num_shell_commands]; \
		++command)
#define USART_BUFFER_SIZE 1024

static bool exit_shell;

static struct shell_context {
	uint32_t rx_pos;
	char rx_buffer[SHELL_BUFFER_SIZE];
} shell_cli;

//typedef struct {
//    uint32_t rx_pos;
//    char rx_buffer[USART_BUFFER_SIZE];
//} usart_context;

static void cli_print_help(void);

static inline void shell_echo_str(const char *str) {
	shell_put_str((const uint8_t *) str, strlen(str));
}

static void shell_printf(char *fmt, ...) {
	static char log_buf[256];
	va_list args;
	va_start(args, fmt);
	vsnprintf(log_buf, sizeof(log_buf) - 1, fmt, args);
	shell_echo_str(log_buf);
	
	va_end(args);
}

static inline char shell_last_char(void) {
	return shell_cli.rx_buffer[shell_cli.rx_pos - 1];
}

static void shell_dispatch_cmd(int argc, char *argv[]) {
	if (strcmp(argv[0], "q") == 0) {
		exit_shell = true;
		shell_printf("Exit shell mode!\n");
		return;
	}

	if (strcmp(argv[0], "h") == 0 || strcmp(argv[0], "help") == 0) {
		cli_print_help();
		return;
	}

	const sShellCommand *cmd = NULL;
	SHELL_FOR_EACH_COMMAND(command) {
		if (strcmp(command->command, argv[0]) == 0) {
			cmd = command;
		}
	}

	if (cmd != NULL) {
		cmd->handler(argc, argv);
	} else {
		shell_printf("Command not find: %s argc: %d\n", argv[0], argc);
	}
}

// shell implementation
static void shell_process(void) {
	if (shell_last_char() != '\n' && shell_last_char() != '\r') {
		return;
	}
	//echo input to shell 
	shell_put_str((const uint8_t *) shell_cli.rx_buffer, shell_cli.rx_pos);

	int argc = 0;
	const int max_args = 10;
	char *argv[max_args];
	char *next_arg = NULL;
	for (uint32_t i = 0; i < shell_cli.rx_pos && argc < max_args; i++) {
		char * cur = &shell_cli.rx_buffer[i];
		if (*cur == '\n' || *cur == ' ' || i == shell_cli.rx_pos - 1) {
			*cur = '\0';
			if (next_arg) {
				argv[argc++] = next_arg;
				next_arg = NULL;
			}
		} else if (next_arg == NULL){
			next_arg = cur;
		}
	}

	if (argc > 0) {
		shell_dispatch_cmd(argc, argv);
	}

	memset(&shell_cli, 0, sizeof(shell_cli));
	shell_echo_str(SHELL_PROMPT);
}

static void shell_receive_char(char c) {
	if (shell_cli.rx_pos >= SHELL_BUFFER_SIZE) {
		memset(&shell_cli, 0, sizeof(shell_cli));
		return;
	}
	uart_putchar(c);

	// ignore \r and automatically covert \n to \r\n when printing
	if (c == '\r') return;

	// backspace
	if (c == '\b') {
		shell_cli.rx_buffer[--shell_cli.rx_pos] = '\0';
		return;
	}

	shell_cli.rx_buffer[shell_cli.rx_pos++] = c;
	shell_process();
}

static void cli_print_help(void) {
	shell_printf("uDeFi Cli Commands: \n");
	SHELL_FOR_EACH_COMMAND(command) {
		shell_printf("  %s: %s\n", command->command, command->help);
	}
}

void run_shell_cli(void) {
	memset(&shell_cli, 0, sizeof(shell_cli));

	cli_print_help();

	shell_echo_str(SHELL_PROMPT);
	exit_shell = false;
	while (!exit_shell) {
		char c = shell_get_char();
		shell_receive_char(c);
	}
}

//read from usart implemention

//usart_context context;
//
//usart_context* usart_read_buf(usart_context* ctx,int len) {
//    if (ctx == NULL || len > USART_BUFFER_SIZE) {
//        return NULL; // Error handling: null pointer or buffer too small
//    }
//
//    ctx->rx_pos = 0;
//    int ch;
//    for (int i = 0; i < len; ++i) {
//        ch = usart_getchar(); // Assuming usart_getchar() returns -1 on error
//        if (ch == -1) {
//            break; // Handle read error or no more data
//        }
//        ctx->rx_buffer[ctx->rx_pos++] = (char)ch;
//    }
//
//    return ctx;
//}

