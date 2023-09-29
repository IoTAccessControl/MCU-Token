#include "pwm.h"

#ifdef USE_ESP32

#include "driver/ledc.h"

#define LEDC_TIMER              LEDC_TIMER_0
#define LEDC_MODE               LEDC_LOW_SPEED_MODE
#define LEDC_OUTPUT_IO          (5) // Define the output GPIO
static int LEDC_CHANNEL = 0;
#define LEDC_DUTY_RES           LEDC_TIMER_13_BIT // Set duty resolution to 13 bits
#define LEDC_DUTY               (4096) // Set duty to 50%. ((2 ** 13) - 1) * 50% = 4095
#define LEDC_FREQUENCY          (5000) // Frequency in Hertz. Set frequency at 5 kHz

void fp_pwm_init(int clock_source_number, int duty, int frequency, int duty_resolution, int timer, int channel) {
  gpio_reset_pin(LEDC_OUTPUT_IO);
  gpio_set_direction(LEDC_OUTPUT_IO, GPIO_MODE_OUTPUT);
  gpio_set_level(LEDC_OUTPUT_IO, 0);

  LEDC_CHANNEL = channel;
  
  ledc_timer_config_t ledc_timer = {
    .speed_mode       = LEDC_LOW_SPEED_MODE,
    .timer_num        = timer,
    .duty_resolution  = duty_resolution,
    .freq_hz          = frequency,
    .clk_cfg          = LEDC_AUTO_CLK
  };

  ledc_timer.clk_cfg = clock_source_number;

  ledc_timer_config(&ledc_timer);
  // Prepare and then apply the LEDC PWM channel configuration
  ledc_channel_config_t ledc_channel = {
    .speed_mode     = LEDC_LOW_SPEED_MODE,
    .channel        = channel,
    .timer_sel      = timer,
    .intr_type      = LEDC_INTR_DISABLE,
    .gpio_num       = LEDC_OUTPUT_IO,
    .duty           = duty,
    .hpoint         = 0
  };
  ledc_channel_config(&ledc_channel);
}

void fp_pwm_stop() {
  gpio_reset_pin(LEDC_OUTPUT_IO);
  gpio_set_direction(LEDC_OUTPUT_IO, GPIO_MODE_OUTPUT);
  gpio_set_level(LEDC_OUTPUT_IO, 0);
  gpio_reset_pin(LEDC_OUTPUT_IO);
  ledc_stop(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL, 0);
}

#endif // USE_ESP32

#ifdef USE_KEIL
#include "stm32f4xx.h"
#include "pwm.h"
#include "stm32f4xx_hal_def.h"
#include "stm32f4xx_hal_tim.h"
#include "stm32f4xx_hal_tim_ex.h"
#include "stm32f429xx.h"
#include "stm32f4xx_hal_gpio.h"
#include "stm32f4xx_hal_gpio_ex.h"

#define ADVANCE_TIM           				TIM8
#define ADVANCE_TIM_CLK_ENABLE()  			__TIM8_CLK_ENABLE()

/* TIM8 channel1 */
#define ADVANCE_OCPWM_PIN           		GPIO_PIN_7            
#define ADVANCE_OCPWM_GPIO_PORT     		GPIOC                      
#define ADVANCE_OCPWM_GPIO_CLK_ENABLE() 	__GPIOC_CLK_ENABLE()
#define ADVANCE_OCPWM_AF					GPIO_AF3_TIM8

/* TIM8 */
#define ADVANCE_BKIN_PIN              		GPIO_PIN_6              
#define ADVANCE_BKIN_GPIO_PORT        		GPIOA                      
#define ADVANCE_BKIN_GPIO_CLK_ENABLE()  	__GPIOA_CLK_ENABLE()
#define ADVANCE_BKIN_AF						GPIO_AF3_TIM8

TIM_HandleTypeDef  TIM_TimeBaseStructure;
TIM_OC_InitTypeDef TIM_OCInitStructure;
GPIO_InitTypeDef GPIO_InitStructure;

__IO uint16_t ChannelPulse = 500;

static void TIMx_GPIO_Config(void) 
{
	ADVANCE_OCPWM_GPIO_CLK_ENABLE();
	ADVANCE_BKIN_GPIO_CLK_ENABLE(); 
										   
	GPIO_InitStructure.Pin = ADVANCE_OCPWM_PIN;	
	GPIO_InitStructure.Mode = GPIO_MODE_AF_PP;    
	GPIO_InitStructure.Pull = GPIO_PULLUP;
	GPIO_InitStructure.Speed = GPIO_SPEED_HIGH; 	
	GPIO_InitStructure.Alternate = ADVANCE_OCPWM_AF;
	HAL_GPIO_Init(ADVANCE_OCPWM_GPIO_PORT, &GPIO_InitStructure);	

	GPIO_InitStructure.Pin = ADVANCE_BKIN_PIN;	
	GPIO_InitStructure.Alternate = ADVANCE_BKIN_AF;	
	HAL_GPIO_Init(ADVANCE_BKIN_GPIO_PORT, &GPIO_InitStructure);
}

static void TIM_Mode_Config(int clock_source_number, int duty, int frequency, int duty_resolution, int timer, int channel)
{
	TIM_BreakDeadTimeConfigTypeDef TIM_BDTRInitStructure;
	ADVANCE_TIM_CLK_ENABLE(); 
	TIM_TimeBaseStructure.Instance = ADVANCE_TIM;
	TIM_TimeBaseStructure.Init.Period = 1000-1;
	TIM_TimeBaseStructure.Init.Prescaler = frequency-1;
	TIM_TimeBaseStructure.Init.ClockDivision=TIM_CLOCKDIVISION_DIV1;
	TIM_TimeBaseStructure.Init.CounterMode=TIM_COUNTERMODE_UP;
	TIM_TimeBaseStructure.Init.RepetitionCounter=0;
	HAL_TIM_PWM_Init(&TIM_TimeBaseStructure);

	TIM_OCInitStructure.OCMode = TIM_OCMODE_PWM1;
	TIM_OCInitStructure.Pulse = ChannelPulse;
	TIM_OCInitStructure.OCPolarity = TIM_OCPOLARITY_HIGH;
	TIM_OCInitStructure.OCNPolarity = TIM_OCNPOLARITY_HIGH;
	TIM_OCInitStructure.OCIdleState = TIM_OCIDLESTATE_SET;
	TIM_OCInitStructure.OCNIdleState = TIM_OCNIDLESTATE_RESET;
	HAL_TIM_PWM_ConfigChannel(&TIM_TimeBaseStructure,&TIM_OCInitStructure,TIM_CHANNEL_2);

	TIM_BDTRInitStructure.OffStateRunMode = TIM_OSSR_ENABLE;
	TIM_BDTRInitStructure.OffStateIDLEMode = TIM_OSSI_ENABLE;
	TIM_BDTRInitStructure.LockLevel = TIM_LOCKLEVEL_1;
	TIM_BDTRInitStructure.DeadTime = 11;
	TIM_BDTRInitStructure.BreakState = TIM_BREAK_ENABLE;
	TIM_BDTRInitStructure.BreakPolarity = TIM_BREAKPOLARITY_LOW;
	TIM_BDTRInitStructure.AutomaticOutput = TIM_AUTOMATICOUTPUT_ENABLE;
	HAL_TIMEx_ConfigBreakDeadTime(&TIM_TimeBaseStructure, &TIM_BDTRInitStructure);

	HAL_TIM_PWM_Start(&TIM_TimeBaseStructure, TIM_CHANNEL_2);
}

extern TIM_HandleTypeDef TIM_TimeBaseStructure;

void fp_pwm_init(int clock_source_number, int duty, int frequency, int duty_resolution, int timer, int channel) {
	TIMx_GPIO_Config();	
	TIM_Mode_Config(clock_source_number, duty, frequency, duty_resolution, timer, channel);
  __HAL_TIM_SetCompare(&TIM_TimeBaseStructure, TIM_CHANNEL_2, duty);
}

void fp_pwm_stop(void) {
	HAL_TIM_PWM_Stop(&TIM_TimeBaseStructure,TIM_CHANNEL_2);
	HAL_TIM_PWM_DeInit(&TIM_TimeBaseStructure);
	HAL_GPIO_DeInit(ADVANCE_OCPWM_GPIO_PORT, ADVANCE_OCPWM_PIN);
	HAL_GPIO_DeInit(ADVANCE_BKIN_GPIO_PORT, ADVANCE_BKIN_PIN);
}

#endif // USE_KEIL

#if defined(USE_STM32F103)

#include "stm32f1xx_hal.h"
#include "stm32f1xx_hal_tim.h"
#include "stm32f1xx_hal_tim_ex.h"

TIM_HandleTypeDef 	TIM3_Handler;
TIM_OC_InitTypeDef 	TIM3_CH2Handler;

void fp_pwm_init(int clock_source_number, int duty, int frequency, int duty_resolution, int timer, int channel){
	__HAL_RCC_TIM3_CLK_ENABLE();
	__HAL_AFIO_REMAP_TIM3_PARTIAL();
	__HAL_RCC_GPIOB_CLK_ENABLE();
	
	GPIO_InitTypeDef GPIO_Initure;

	GPIO_Initure.Pin=GPIO_PIN_5;
	GPIO_Initure.Mode=GPIO_MODE_AF_PP;
	GPIO_Initure.Pull=GPIO_PULLDOWN;
	GPIO_Initure.Speed=GPIO_SPEED_HIGH;
	HAL_GPIO_Init(GPIOB,&GPIO_Initure); 	

	TIM3_Handler.Instance=TIM3;
	TIM3_Handler.Init.Prescaler=frequency;
	TIM3_Handler.Init.CounterMode=TIM_COUNTERMODE_UP;
	TIM3_Handler.Init.Period=duty_resolution;
	TIM3_Handler.Init.ClockDivision=TIM_CLOCKDIVISION_DIV1;
	HAL_TIM_PWM_Init(&TIM3_Handler);

	TIM3_CH2Handler.OCMode=TIM_OCMODE_PWM1;
	TIM3_CH2Handler.Pulse=duty;
	TIM3_CH2Handler.OCPolarity=TIM_OCPOLARITY_HIGH; 
	HAL_TIM_PWM_ConfigChannel(&TIM3_Handler,&TIM3_CH2Handler,TIM_CHANNEL_2);

	HAL_TIM_PWM_Start(&TIM3_Handler,TIM_CHANNEL_2);
};

void TIM3_IRQHandler(void) {
  HAL_TIM_IRQHandler(&TIM3_Handler);
}

void fp_pwm_stop(void){
	HAL_TIM_PWM_Stop(&TIM3_Handler,TIM_CHANNEL_2);
	HAL_TIM_PWM_DeInit(&TIM3_Handler);
	HAL_GPIO_DeInit(GPIOA, GPIO_PIN_5);
};

#endif // USE_STM32F103
