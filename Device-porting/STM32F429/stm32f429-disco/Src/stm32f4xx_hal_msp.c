#include "main.h"

#include <stdint.h>
#include <stdio.h>

#include "app_port.h"


#define USART_REC_LEN  			200
#define EN_USART1_RX 			1

UART_HandleTypeDef UartHandle1;

void uart_init(uint32_t bound) {
	UartHandle1.Instance = USARTx;
	UartHandle1.Init.BaudRate = bound;
	UartHandle1.Init.WordLength = UART_WORDLENGTH_8B;
	UartHandle1.Init.StopBits = UART_STOPBITS_1;
	UartHandle1.Init.Parity = UART_PARITY_NONE;
	UartHandle1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
	UartHandle1.Init.Mode = UART_MODE_TX_RX;
	HAL_UART_Init(&UartHandle1);

	__HAL_UART_ENABLE_IT(&UartHandle1, UART_IT_RXNE);
	HAL_NVIC_EnableIRQ(USART1_IRQn);
	HAL_NVIC_SetPriority(USART1_IRQn, 3, 3);
}

void HAL_UART_MspInit(UART_HandleTypeDef *huart) {
	GPIO_InitTypeDef  GPIO_InitStruct;

	USARTx_TX_GPIO_CLK_ENABLE();
	USARTx_RX_GPIO_CLK_ENABLE();

	USARTx_CLK_ENABLE();

	GPIO_InitStruct.Pin       = USARTx_TX_PIN;
	GPIO_InitStruct.Mode      = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Pull      = GPIO_PULLUP;
	GPIO_InitStruct.Speed     = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Alternate = USARTx_TX_AF;

	HAL_GPIO_Init(USARTx_TX_GPIO_PORT, &GPIO_InitStruct);

	GPIO_InitStruct.Pin = USARTx_RX_PIN;
	GPIO_InitStruct.Alternate = USARTx_RX_AF;

	HAL_GPIO_Init(USARTx_RX_GPIO_PORT, &GPIO_InitStruct);
}


void HAL_UART_MspDeInit(UART_HandleTypeDef *huart) {
	USARTx_FORCE_RESET();
	USARTx_RELEASE_RESET();

	HAL_GPIO_DeInit(USARTx_TX_GPIO_PORT, USARTx_TX_PIN);
	HAL_GPIO_DeInit(USARTx_RX_GPIO_PORT, USARTx_RX_PIN);
}


// ringbuffer for read char
#define RECV_BUF_SIZE	256		/* Arbitrary buffer size */
char recv_buf[RECV_BUF_SIZE];
volatile int recv_ndx_nxt;		/* Next place to store */
volatile int recv_ndx_cur;		/* Next place to read */
void USART1_IRQHandler(void)
{
	uint8_t Res;
	int i;
	do {
		HAL_UART_Receive(&UartHandle1, &Res, 1, 1000);
		recv_buf[recv_ndx_nxt] = Res;
			i = (recv_ndx_nxt + 1) % RECV_BUF_SIZE;
			if (i != recv_ndx_cur) {
				recv_ndx_nxt = i;
				BSP_LED_Off(LED3);
			} else {
				printf("Usart ringbuffer overrun\n");
				HAL_UART_ErrorCallback(&UartHandle1);
			}
	} while ((__HAL_UART_GET_FLAG(&UartHandle1, UART_FLAG_RXNE) != RESET));
}

void HAL_UART_ErrorCallback(UART_HandleTypeDef *UartHandle)
{
  BSP_LED_On(LED3);
}

static uint32_t fac_us = 0;

void delay_init(uint8_t SYSCLK) {
	HAL_SYSTICK_CLKSourceConfig(SYSTICK_CLKSOURCE_HCLK);
	fac_us = SYSCLK;
}


void delay_us(int nus) {
	uint32_t ticks;
	uint32_t told, tnow, tcnt = 0;
	uint32_t reload = SysTick->LOAD;
	ticks = nus * fac_us;
	told = SysTick->VAL;

	while(1)
	{
		tnow = SysTick->VAL;

		if(tnow != told)
		{
			if(tnow < told)tcnt += told - tnow;
			else tcnt += reload - tnow + told;

			told = tnow;
			if(tcnt >= ticks)break;
		}
	}
}

void delay_ms(uint16_t nms)
{
	for(int i = 0; i < nms; i++) delay_us(1000);
}

// my usart
void uart_putchar(char ch) {
	HAL_UART_Transmit(&UartHandle1, (uint8_t *)&ch, 1, 0xFFFF);
}

char usart_getchar(void) {
	char	c = 0;

	while (recv_ndx_cur == recv_ndx_nxt);
	if (recv_ndx_cur != recv_ndx_nxt) {
		c = recv_buf[recv_ndx_cur];
		recv_ndx_cur = (recv_ndx_cur + 1) % RECV_BUF_SIZE;
	}

	return c;
}

#define PUTCHAR_PROTOTYPE int fputc(int ch, FILE *f)
PUTCHAR_PROTOTYPE
{
	if (ch == '\n') {
		char lr = '\r';
		HAL_UART_Transmit(&UartHandle1, (uint8_t *)&lr, 1, 0xFFFF);
	}
	HAL_UART_Transmit(&UartHandle1, (uint8_t *)&ch, 1, 0xFFFF);

	return ch;
}
