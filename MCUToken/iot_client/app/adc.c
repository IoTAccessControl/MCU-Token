#include "adc.h"

#if defined(USE_KEIL)

// Converted results
volatile uint16_t ADC_ConvertedValues[3]={0};
volatile uint16_t ADC_ConvertedValuesCorrected[3]={0};
volatile uint16_t ADC_ConvertedValue = 0;

DMA_HandleTypeDef DMA_Init_Handle;
ADC_HandleTypeDef ADC_Handle;
ADC_ChannelConfTypeDef ADC_Config;

void adc_reference_init(void) {
  RHEOSTAT_ADC_DMA_CLK_ENABLE();
  DMA_Init_Handle.Instance = RHEOSTAT_ADC_DMA_STREAM;
  DMA_Init_Handle.Init.Direction = DMA_PERIPH_TO_MEMORY;
  DMA_Init_Handle.Init.PeriphInc = DMA_PINC_DISABLE;
  DMA_Init_Handle.Init.MemInc = DMA_MINC_ENABLE;
  DMA_Init_Handle.Init.PeriphDataAlignment = DMA_PDATAALIGN_HALFWORD;
  DMA_Init_Handle.Init.MemDataAlignment = DMA_MDATAALIGN_HALFWORD;
  DMA_Init_Handle.Init.Mode = DMA_CIRCULAR;
  DMA_Init_Handle.Init.Priority = DMA_PRIORITY_HIGH;
  DMA_Init_Handle.Init.FIFOMode = DMA_FIFOMODE_DISABLE;
  DMA_Init_Handle.Init.FIFOThreshold = DMA_FIFO_THRESHOLD_HALFFULL;
  DMA_Init_Handle.Init.MemBurst = DMA_MBURST_SINGLE;
  DMA_Init_Handle.Init.PeriphBurst = DMA_PBURST_SINGLE;
  DMA_Init_Handle.Init.Channel = RHEOSTAT_ADC_DMA_CHANNEL;
  HAL_DMA_Init(&DMA_Init_Handle);

  HAL_DMA_Start (&DMA_Init_Handle,RHEOSTAT_ADC_DR_ADDR,(uint32_t)&ADC_ConvertedValue,1);
  RHEOSTAT_ADC_CLK_ENABLE();
  ADC_Handle.Instance = RHEOSTAT_ADC;
  ADC_Handle.Init.ClockPrescaler = ADC_CLOCKPRESCALER_PCLK_DIV4;
  ADC_Handle.Init.Resolution = ADC_RESOLUTION_12B;
  ADC_Handle.Init.ScanConvMode = DISABLE;
  ADC_Handle.Init.ContinuousConvMode = ENABLE;
  ADC_Handle.Init.DiscontinuousConvMode = DISABLE;
  ADC_Handle.Init.NbrOfDiscConversion   = 0;
  ADC_Handle.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE;
  ADC_Handle.Init.DataAlign = ADC_DATAALIGN_RIGHT;
  ADC_Handle.Init.NbrOfConversion = 1;
  ADC_Handle.Init.DMAContinuousRequests = ENABLE;
  ADC_Handle.Init.EOCSelection          = DISABLE;
  HAL_ADC_Init(&ADC_Handle);

  ADC_Config.Channel      = RHEOSTAT_ADC_CHANNEL;
  ADC_Config.Rank         = 1;
  ADC_Config.SamplingTime = ADC_SAMPLETIME_56CYCLES;
  ADC_Config.Offset       = 0;
  HAL_ADC_ConfigChannel(&ADC_Handle, &ADC_Config);

  HAL_ADC_Start_DMA(&ADC_Handle, (uint32_t*)&ADC_ConvertedValue, 1);
};

void adc_reference_stop(void) {
  HAL_ADC_Stop(&ADC_Handle);
  HAL_ADC_DeInit(&ADC_Handle);
  __ADC1_CLK_DISABLE();

  HAL_ADC_Stop_DMA(&ADC_Handle);
  HAL_DMA_Abort(&DMA_Init_Handle);
  __DMA2_CLK_DISABLE();
}

void adc_multi_channel_init(void) {
  GPIO_InitTypeDef GPIO_InitStructure;

  RHEOSTAT_ADC_GPIO_CLK1_ENABLE();  
  GPIO_InitStructure.Pin = RHEOSTAT_ADC_GPIO_PIN1;
  GPIO_InitStructure.Mode = GPIO_MODE_ANALOG;	    
  GPIO_InitStructure.Pull = GPIO_PULLDOWN;
  HAL_GPIO_Init(RHEOSTAT_ADC_GPIO_PORT1, &GPIO_InitStructure);
  

  RHEOSTAT_ADC_GPIO_CLK2_ENABLE();    
  GPIO_InitStructure.Pin = RHEOSTAT_ADC_GPIO_PIN2;
  GPIO_InitStructure.Mode = GPIO_MODE_ANALOG;	    
  GPIO_InitStructure.Pull = GPIO_PULLDOWN;
  HAL_GPIO_Init(RHEOSTAT_ADC_GPIO_PORT2, &GPIO_InitStructure);
  

  RHEOSTAT_ADC_GPIO_CLK3_ENABLE();
  GPIO_InitStructure.Pin = RHEOSTAT_ADC_GPIO_PIN3;
  GPIO_InitStructure.Mode = GPIO_MODE_ANALOG;	    
  GPIO_InitStructure.Pull = GPIO_PULLDOWN;
  HAL_GPIO_Init(RHEOSTAT_ADC_GPIO_PORT3, &GPIO_InitStructure);


  RHEOSTAT_ADC_DMA_CLK_ENABLE();
  DMA_Init_Handle.Instance = RHEOSTAT_ADC_DMA_STREAM;
  DMA_Init_Handle.Init.Direction = DMA_PERIPH_TO_MEMORY;	
  DMA_Init_Handle.Init.PeriphInc = DMA_PINC_DISABLE;
  DMA_Init_Handle.Init.MemInc = DMA_MINC_ENABLE;
  DMA_Init_Handle.Init.PeriphDataAlignment = DMA_PDATAALIGN_HALFWORD;
  DMA_Init_Handle.Init.MemDataAlignment = DMA_MDATAALIGN_HALFWORD;
  DMA_Init_Handle.Init.Mode = DMA_CIRCULAR;
  DMA_Init_Handle.Init.Priority = DMA_PRIORITY_HIGH;
  DMA_Init_Handle.Init.FIFOMode = DMA_FIFOMODE_DISABLE;
  DMA_Init_Handle.Init.FIFOThreshold = DMA_FIFO_THRESHOLD_HALFFULL;
  DMA_Init_Handle.Init.MemBurst = DMA_MBURST_SINGLE;
  DMA_Init_Handle.Init.PeriphBurst = DMA_PBURST_SINGLE;
  DMA_Init_Handle.Init.Channel = RHEOSTAT_ADC_DMA_CHANNEL;

  HAL_DMA_Init(&DMA_Init_Handle); 
  HAL_DMA_Start(&DMA_Init_Handle,RHEOSTAT_ADC_DR_ADDR,(uint32_t)&ADC_ConvertedValues,RHEOSTAT_NOFCHANEL);

  RHEOSTAT_ADC_CLK_ENABLE();

  ADC_Handle.Instance = RHEOSTAT_ADC;
  ADC_Handle.Init.ClockPrescaler = ADC_CLOCKPRESCALER_PCLK_DIV4;
  ADC_Handle.Init.Resolution = ADC_RESOLUTION_12B;
  ADC_Handle.Init.ScanConvMode = ENABLE;
  ADC_Handle.Init.ContinuousConvMode = ENABLE;
  ADC_Handle.Init.DiscontinuousConvMode = DISABLE;
  ADC_Handle.Init.NbrOfDiscConversion   = 0;
  ADC_Handle.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE;
  ADC_Handle.Init.DataAlign = ADC_DATAALIGN_RIGHT;
  ADC_Handle.Init.NbrOfConversion = RHEOSTAT_NOFCHANEL;
  ADC_Handle.Init.DMAContinuousRequests = ENABLE;
  ADC_Handle.Init.EOCSelection          = DISABLE;
  HAL_ADC_Init(&ADC_Handle);

  ADC_Config.Channel      = RHEOSTAT_ADC_CHANNEL1;
  ADC_Config.Rank         = 1;    
  ADC_Config.SamplingTime = ADC_SAMPLETIME_3CYCLES;
  ADC_Config.Offset       = 0;
  HAL_ADC_ConfigChannel(&ADC_Handle, &ADC_Config);
  
  ADC_Config.Channel      = RHEOSTAT_ADC_CHANNEL2;
  ADC_Config.Rank         = 2;
  ADC_Config.SamplingTime = ADC_SAMPLETIME_3CYCLES;
  ADC_Config.Offset       = 0;
  HAL_ADC_ConfigChannel(&ADC_Handle, &ADC_Config);

  ADC_Config.Channel      = RHEOSTAT_ADC_CHANNEL3;
  ADC_Config.Rank         = 3;    	
  ADC_Config.SamplingTime = ADC_SAMPLETIME_3CYCLES;
  ADC_Config.Offset       = 0;
  HAL_ADC_ConfigChannel(&ADC_Handle, &ADC_Config);

  HAL_ADC_Start_DMA(&ADC_Handle, (uint32_t*)&ADC_ConvertedValues,1);
}

void adc_multi_channel_stop(void) {
  HAL_ADC_Stop(&ADC_Handle);
  HAL_ADC_DeInit(&ADC_Handle);
  __ADC1_CLK_DISABLE();

  HAL_ADC_Stop_DMA(&ADC_Handle);
  HAL_DMA_DeInit(&DMA_Init_Handle);
  __DMA2_CLK_DISABLE();
}

void adc_get_value(bool only_pwm) {
  ADC_ConvertedValuesCorrected[0] = 3.3 * 1000 * ADC_ConvertedValues[0] / 4096;
  ADC_ConvertedValuesCorrected[1] = 3.3 * 1000 * ADC_ConvertedValues[1] / 4096;
  ADC_ConvertedValuesCorrected[2] = 3.3 * 1000 * ADC_ConvertedValues[2] / 4096;
}

void adc_get_ref_value(void) {}

#endif


#if defined(USE_ESP32)

#include "dac.h"

static esp_adc_cal_characteristics_t adc2_chars;
volatile uint16_t ADC_ConvertedValues[3]={0};
volatile uint16_t ADC_ConvertedValuesCorrected[3]={0};
volatile uint16_t ADC_ConvertedValue = 0;

void adc_reference_init(void) {
  esp_err_t ret;

	ret = esp_adc_cal_check_efuse(ESP_ADC_CAL_VAL_EFUSE_TP);
	if (ret == ESP_ERR_NOT_SUPPORTED) {
			printf("Calibration scheme not supported, skip software calibration");
	} else if (ret == ESP_ERR_INVALID_VERSION) {
			printf("eFuse not burnt, skip software calibration");
	} else if (ret == ESP_OK) {
			esp_adc_cal_characterize(ADC_UNIT_2, ADC_ATTEN_DB_11, ADC_WIDTH_BIT_13, 0, &adc2_chars);
	} else {
			printf("Invalid arg");
	}

  gpio_reset_pin(GPIO_NUM_11);
  gpio_set_direction(GPIO_NUM_11, GPIO_MODE_OUTPUT);
  gpio_set_level(GPIO_NUM_11, 0);
  gpio_set_level(GPIO_NUM_11, 1);

  adc_vref_to_gpio(ADC_UNIT_2, GPIO_NUM_11);
  // https://www.esp32.com/viewtopic.php?t=17155
};

void adc_reference_stop(void) {
  gpio_reset_pin(GPIO_NUM_11);
  gpio_set_direction(GPIO_NUM_11, GPIO_MODE_OUTPUT);
  gpio_set_level(GPIO_NUM_11, 0);
  gpio_reset_pin(GPIO_NUM_11);
};

void adc_get_ref_value(void) {
  int raw_out;
	int voltage;
  
  /* GPIO 11*/
  adc2_get_raw(ADC2_CHANNEL_0, ADC_WIDTH_BIT_13, &raw_out);
	voltage = esp_adc_cal_raw_to_voltage(raw_out, &adc2_chars);
	ADC_ConvertedValue = (volatile uint16_t)voltage;
}

void adc_multi_channel_init(void){
  esp_err_t ret;

	ret = esp_adc_cal_check_efuse(ESP_ADC_CAL_VAL_EFUSE_TP);
	if (ret == ESP_ERR_NOT_SUPPORTED) {
			printf("Calibration scheme not supported, skip software calibration");
	} else if (ret == ESP_ERR_INVALID_VERSION) {
			printf("eFuse not burnt, skip software calibration");
	} else if (ret == ESP_OK) {
			esp_adc_cal_characterize(ADC_UNIT_2, ADC_ATTEN_DB_11, ADC_WIDTH_BIT_13, 0, &adc2_chars);
	} else {
			printf("Invalid arg");
	}

  gpio_reset_pin(GPIO_NUM_12);
  gpio_reset_pin(GPIO_NUM_16);
  gpio_reset_pin(GPIO_NUM_19);

  gpio_set_direction(GPIO_NUM_16, GPIO_MODE_INPUT);
  gpio_set_direction(GPIO_NUM_19, GPIO_MODE_INPUT);
  gpio_set_direction(GPIO_NUM_12, GPIO_MODE_INPUT);

	adc2_config_channel_atten(ADC2_CHANNEL_5, ADC_ATTEN_DB_11);
	adc2_config_channel_atten(ADC2_CHANNEL_8, ADC_ATTEN_DB_11);
  adc2_config_channel_atten(ADC2_CHANNEL_1, ADC_ATTEN_DB_11);
};

void adc_multi_channel_stop(void){
  gpio_set_direction(GPIO_NUM_16, GPIO_MODE_OUTPUT);
  gpio_set_level(GPIO_NUM_16, 0);
  gpio_set_direction(GPIO_NUM_19, GPIO_MODE_OUTPUT);
  gpio_set_level(GPIO_NUM_19, 0);
  gpio_set_direction(GPIO_NUM_12, GPIO_MODE_OUTPUT);
  gpio_set_level(GPIO_NUM_12, 0);
  gpio_reset_pin(GPIO_NUM_16);
  gpio_reset_pin(GPIO_NUM_19);
  gpio_reset_pin(GPIO_NUM_12);
};

void adc_get_value(bool only_pwm) {
  int raw_out;
	int voltage = 0;

  /* GPIO 12*/
  adc2_get_raw(ADC2_CHANNEL_1, ADC_WIDTH_BIT_13, &raw_out);
	voltage = esp_adc_cal_raw_to_voltage(raw_out, &adc2_chars);
	ADC_ConvertedValues[2] = (volatile uint16_t)raw_out;
  ADC_ConvertedValuesCorrected[2] = voltage;
  if (only_pwm) return;

  /* GPIO 16*/
  adc2_get_raw(ADC2_CHANNEL_5, ADC_WIDTH_BIT_13, &raw_out);
	voltage = esp_adc_cal_raw_to_voltage(raw_out, &adc2_chars);
	ADC_ConvertedValues[0] = (volatile uint16_t)raw_out;
  ADC_ConvertedValuesCorrected[0] = voltage;

  /* GPIO 19*/
  adc2_get_raw(ADC2_CHANNEL_8, ADC_WIDTH_BIT_13, &raw_out);
	voltage = esp_adc_cal_raw_to_voltage(raw_out, &adc2_chars);
	ADC_ConvertedValues[1] = (volatile uint16_t)raw_out;
  ADC_ConvertedValuesCorrected[1] = voltage;
}
#endif // USE_ESP32

#if defined(USE_STM32F103)

#include "stm32f1xx_hal.h"
#include "stm32f1xx_hal_adc.h"
#include "stm32f1xx_hal_gpio.h"

volatile uint16_t ADC_ConvertedValues[3]={0};
volatile uint16_t ADC_ConvertedValuesCorrected[3]={0};
volatile uint16_t ADC_ConvertedValue = 0;
ADC_HandleTypeDef ADC1_Handler;

void adc_reference_init(void) {
  __HAL_RCC_ADC1_CLK_ENABLE();

  RCC_PeriphCLKInitTypeDef ADC_CLKInit;
	
	ADC_CLKInit.PeriphClockSelection=RCC_PERIPHCLK_ADC;
	ADC_CLKInit.AdcClockSelection=RCC_ADCPCLK2_DIV6;
	HAL_RCCEx_PeriphCLKConfig(&ADC_CLKInit);
	
  ADC1_Handler.Instance=ADC1;
  ADC1_Handler.Init.DataAlign=ADC_DATAALIGN_RIGHT;
  ADC1_Handler.Init.ScanConvMode=DISABLE;
  ADC1_Handler.Init.ContinuousConvMode=DISABLE;
  ADC1_Handler.Init.NbrOfConversion=1;
  ADC1_Handler.Init.DiscontinuousConvMode=DISABLE;
  ADC1_Handler.Init.NbrOfDiscConversion=0;
  ADC1_Handler.Init.ExternalTrigConv=ADC_SOFTWARE_START;
  HAL_ADC_Init(&ADC1_Handler);

  HAL_ADCEx_Calibration_Start(&ADC1_Handler);	
};

void adc_reference_stop(void) {
  HAL_ADC_Stop(&ADC1_Handler);
  HAL_ADC_DeInit(&ADC1_Handler);
  __HAL_RCC_ADC1_CLK_DISABLE();
};

void adc_get_ref_value(void) {
  ADC_ChannelConfTypeDef ADC1_ChanConf;
  ADC1_ChanConf.Channel=ADC_CHANNEL_VREFINT;
  ADC1_ChanConf.Rank=1;
  ADC1_ChanConf.SamplingTime=ADC_SAMPLETIME_239CYCLES_5;   
  HAL_ADC_ConfigChannel(&ADC1_Handler,&ADC1_ChanConf);
  HAL_ADC_Start(&ADC1_Handler);
  HAL_ADC_PollForConversion(&ADC1_Handler,10);
	ADC_ConvertedValue = HAL_ADC_GetValue(&ADC1_Handler);	
  HAL_ADC_Stop(&ADC1_Handler);
};

void adc_multi_channel_init(void) {
  GPIO_InitTypeDef GPIO_Initure;
  __HAL_RCC_ADC1_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();

  GPIO_Initure.Pin=GPIO_PIN_0;
  GPIO_Initure.Mode=GPIO_MODE_ANALOG;
  GPIO_Initure.Pull=GPIO_PULLDOWN;
  HAL_GPIO_Init(GPIOA,&GPIO_Initure);

  GPIO_Initure.Pin=GPIO_PIN_1;
  GPIO_Initure.Mode=GPIO_MODE_ANALOG;
  GPIO_Initure.Pull=GPIO_PULLDOWN;
  HAL_GPIO_Init(GPIOA,&GPIO_Initure);

  GPIO_Initure.Pin=GPIO_PIN_2;
  GPIO_Initure.Mode=GPIO_MODE_ANALOG;
  GPIO_Initure.Pull=GPIO_PULLDOWN;
  HAL_GPIO_Init(GPIOA,&GPIO_Initure);

  RCC_PeriphCLKInitTypeDef ADC_CLKInit;
	
	ADC_CLKInit.PeriphClockSelection=RCC_PERIPHCLK_ADC;
	ADC_CLKInit.AdcClockSelection=RCC_ADCPCLK2_DIV6;
	HAL_RCCEx_PeriphCLKConfig(&ADC_CLKInit);
	
  ADC1_Handler.Instance=ADC1;
  ADC1_Handler.Init.DataAlign=ADC_DATAALIGN_RIGHT;
  ADC1_Handler.Init.ScanConvMode=DISABLE;
  ADC1_Handler.Init.ContinuousConvMode=DISABLE;
  ADC1_Handler.Init.NbrOfConversion=1;
  ADC1_Handler.Init.DiscontinuousConvMode=DISABLE;
  ADC1_Handler.Init.NbrOfDiscConversion=0;
  ADC1_Handler.Init.ExternalTrigConv=ADC_SOFTWARE_START;
  HAL_ADC_Init(&ADC1_Handler);

  HAL_ADCEx_Calibration_Start(&ADC1_Handler);
};

void adc_multi_channel_stop(void) {
  HAL_ADC_Stop(&ADC1_Handler);
  HAL_ADC_DeInit(&ADC1_Handler);
  __HAL_RCC_ADC1_CLK_DISABLE();
};

extern int adc_read_type;
void adc_get_value(bool only_pwm) {
  ADC_ChannelConfTypeDef ADC1_ChanConf;
  ADC1_ChanConf.Channel=ADC_CHANNEL_2;
  ADC1_ChanConf.Rank=1;
  ADC1_ChanConf.SamplingTime=ADC_SAMPLETIME_1CYCLE_5;      
  HAL_ADC_ConfigChannel(&ADC1_Handler,&ADC1_ChanConf); 
  HAL_ADC_Start(&ADC1_Handler);
  HAL_ADC_PollForConversion(&ADC1_Handler,10);
	ADC_ConvertedValues[2] = HAL_ADC_GetValue(&ADC1_Handler);	
  HAL_ADC_Stop(&ADC1_Handler);
  ADC_ConvertedValuesCorrected[2] = 3.3 * 1000 * ADC_ConvertedValues[2] / 4096;

  if (only_pwm) return;

  if (adc_read_type % 1024 == 0) ADC1_ChanConf.Channel=ADC_CHANNEL_VREFINT;
  else ADC1_ChanConf.Channel=ADC_CHANNEL_0; 
  ADC1_ChanConf.Rank=1;
  ADC1_ChanConf.SamplingTime=ADC_SAMPLETIME_1CYCLE_5;
  HAL_ADC_ConfigChannel(&ADC1_Handler,&ADC1_ChanConf);
  HAL_ADC_Start(&ADC1_Handler);
  HAL_ADC_PollForConversion(&ADC1_Handler,10);
	ADC_ConvertedValues[0] = HAL_ADC_GetValue(&ADC1_Handler);	 
  HAL_ADC_Stop(&ADC1_Handler);

  if (adc_read_type % 1024 == 0) ADC1_ChanConf.Channel=ADC_CHANNEL_VREFINT;
  else ADC1_ChanConf.Channel=ADC_CHANNEL_1; 
  ADC1_ChanConf.Rank=1;
  ADC1_ChanConf.SamplingTime=ADC_SAMPLETIME_1CYCLE_5;      
  HAL_ADC_ConfigChannel(&ADC1_Handler,&ADC1_ChanConf);
  HAL_ADC_Start(&ADC1_Handler);
  HAL_ADC_PollForConversion(&ADC1_Handler,10);
	ADC_ConvertedValues[1] = HAL_ADC_GetValue(&ADC1_Handler);	
  HAL_ADC_Stop(&ADC1_Handler);
  
  ADC_ConvertedValuesCorrected[0] = 3.3 * 1000 * ADC_ConvertedValues[0] / 4096;
  ADC_ConvertedValuesCorrected[1] = 3.3 * 1000 * ADC_ConvertedValues[1] / 4096;
};

#endif // USE_STM32F103
