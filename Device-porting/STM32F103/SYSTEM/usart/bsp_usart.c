#include "sys.h"
#include "bsp_usart.h"	
#include "app_port.h"
#include "delay.h"
#include <stdint.h>
#include <stdio.h>
#if EN_USART1_RX	
#define RECV_BUF_SIZE	128
char recv_buf[RECV_BUF_SIZE];
volatile int recv_ndx_nxt = 0;
volatile int recv_ndx_cur = 0;


UART_HandleTypeDef UART1_Handler;

void uart_init(u32 bound)
{
	UART1_Handler.Instance=USART1;
	UART1_Handler.Init.BaudRate=bound;
	UART1_Handler.Init.WordLength=UART_WORDLENGTH_8B;
	UART1_Handler.Init.StopBits=UART_STOPBITS_1;
	UART1_Handler.Init.Parity=UART_PARITY_NONE;
	UART1_Handler.Init.HwFlowCtl=UART_HWCONTROL_NONE;
	UART1_Handler.Init.Mode=UART_MODE_TX_RX;
	HAL_UART_Init(&UART1_Handler);
	
	__HAL_UART_ENABLE_IT(&UART1_Handler, UART_IT_RXNE);
}

void HAL_UART_MspInit(UART_HandleTypeDef *huart)
{
	GPIO_InitTypeDef GPIO_Initure;
	
	if(huart->Instance==USART1)
	{
		__HAL_RCC_GPIOA_CLK_ENABLE();
		__HAL_RCC_USART1_CLK_ENABLE();
		__HAL_RCC_AFIO_CLK_ENABLE();
	
		GPIO_Initure.Pin=GPIO_PIN_9;
		GPIO_Initure.Mode=GPIO_MODE_AF_PP;
		GPIO_Initure.Pull=GPIO_PULLUP;
		GPIO_Initure.Speed=GPIO_SPEED_FREQ_HIGH;
		HAL_GPIO_Init(GPIOA,&GPIO_Initure);

		GPIO_Initure.Pin=GPIO_PIN_10;
		GPIO_Initure.Mode=GPIO_MODE_AF_INPUT;
		HAL_GPIO_Init(GPIOA,&GPIO_Initure);
		
		HAL_NVIC_EnableIRQ(USART1_IRQn);
		HAL_NVIC_SetPriority(USART1_IRQn,0,1);
	}
}

void USART1_IRQHandler(void)                	
{ 
	uint8_t Res;
	int i;
	do {
		HAL_UART_Receive(&UART1_Handler, &Res, 1, 1000);
		recv_buf[recv_ndx_nxt] = Res;
			i = (recv_ndx_nxt + 1) % RECV_BUF_SIZE;
			if (i != recv_ndx_cur) {
				recv_ndx_nxt = i;
			} else {
				printf("Usart ringbuffer overrun\n");
				show_error();
			}
	} while ((__HAL_UART_GET_FLAG(&UART1_Handler, UART_FLAG_RXNE) != RESET));
}

char usart_getchar(void) {
	char c = 0;
	while (recv_ndx_cur == recv_ndx_nxt) {delay_ms(20);};
	if (recv_ndx_cur != recv_ndx_nxt) {
		c = recv_buf[recv_ndx_cur];
		recv_ndx_cur = (recv_ndx_cur + 1) % RECV_BUF_SIZE;
	}
	return c;
}

 
void uart_putchar(char ch) {
	HAL_UART_Transmit(&UART1_Handler, (uint8_t *)&ch, 1, 0xFFFF);
}

void show_error(void) {
	printf("ERROR");
}

#pragma import(__use_no_semihosting)              
struct __FILE{ 
	int handle; 
}; 

FILE __stdout;
void _sys_exit(int x) 
{ 
	x = x; 
}

int fputc(int ch, FILE *f) {
	if (ch == '\n') {
		char lr = '\r';
		HAL_UART_Transmit(&UART1_Handler, (uint8_t *)&lr, 1, 0xFFFF);
	}
	HAL_UART_Transmit(&UART1_Handler, (uint8_t *)&ch, 1, 0xFFFF);
	return ch;
}
#endif	


