#include "led/bsp_led.h"   

void LED_GPIO_Config(void)
{
    GPIO_InitTypeDef  GPIO_InitStruct;

    LED1_GPIO_CLK_ENABLE();
    LED2_GPIO_CLK_ENABLE();
    LED3_GPIO_CLK_ENABLE();
												   
    GPIO_InitStruct.Pin = LED1_PIN;	
    GPIO_InitStruct.Mode  = GPIO_MODE_OUTPUT_PP;  
    GPIO_InitStruct.Pull  = GPIO_PULLUP;
    GPIO_InitStruct.Speed = GPIO_SPEED_HIGH; 

    HAL_GPIO_Init(LED1_GPIO_PORT, &GPIO_InitStruct);	
														   
    GPIO_InitStruct.Pin = LED2_PIN;	
    HAL_GPIO_Init(LED2_GPIO_PORT, &GPIO_InitStruct);	
														   
    GPIO_InitStruct.Pin = LED3_PIN;	
    HAL_GPIO_Init(LED3_GPIO_PORT, &GPIO_InitStruct);	

    LED_RGBOFF;
}
