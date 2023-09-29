#include "sys.h"


void Stm32_Clock_Init(u32 PLL)
{
    HAL_StatusTypeDef ret = HAL_OK;
    RCC_OscInitTypeDef RCC_OscInitStructure; 
    RCC_ClkInitTypeDef RCC_ClkInitStructure;
    
    RCC_OscInitStructure.OscillatorType=RCC_OSCILLATORTYPE_HSE;
    RCC_OscInitStructure.HSEState=RCC_HSE_ON;                  
	RCC_OscInitStructure.HSEPredivValue=RCC_HSE_PREDIV_DIV1;
    RCC_OscInitStructure.PLL.PLLState=RCC_PLL_ON;	
    RCC_OscInitStructure.PLL.PLLSource=RCC_PLLSOURCE_HSE;
    RCC_OscInitStructure.PLL.PLLMUL=PLL;
    ret=HAL_RCC_OscConfig(&RCC_OscInitStructure);
	
    if(ret!=HAL_OK) while(1);
    
    RCC_ClkInitStructure.ClockType=(RCC_CLOCKTYPE_SYSCLK|RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2);
    RCC_ClkInitStructure.SYSCLKSource=RCC_SYSCLKSOURCE_PLLCLK;
    RCC_ClkInitStructure.AHBCLKDivider=RCC_SYSCLK_DIV1;				
    RCC_ClkInitStructure.APB1CLKDivider=RCC_HCLK_DIV2; 				
    RCC_ClkInitStructure.APB2CLKDivider=RCC_HCLK_DIV1; 				
    ret=HAL_RCC_ClockConfig(&RCC_ClkInitStructure,FLASH_LATENCY_2);
		
    if(ret!=HAL_OK) while(1);
}

#ifdef  USE_FULL_ASSERT
void assert_failed(uint8_t* file, uint32_t line)
{ 
	while (1)
	{
	}
}
#endif
void WFI_SET(void)
{
	__ASM volatile("wfi");		  
}
void INTX_DISABLE(void)
{		  
	__ASM volatile("cpsid i");
}
void INTX_ENABLE(void)
{
	__ASM volatile("cpsie i");		  
}
__asm void MSR_MSP(u32 addr) 
{
    MSR MSP, r0
    BX r14
}
