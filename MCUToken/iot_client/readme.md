The document describes the pipeline of our work with some important code fragments to help you understand MCU-Token. 

We use DAC/ADC on ESP32-S2 as an example. DAC/ADC. A digital-to-analog converter (DAC) can convert digital values to analog signals, such as voltage. Conversely, an analog-to-digital converter (ADC) performs the reverse function of converting analog signals to digital outputs. By generating multiple analog signals through the DAC, we can induce variations in the ADC’s output values and use these biases to uniquely identify devices.

#### Configuration

In the file "[app/defs.h](app/defs.h)" (line 8), define the macro `DEBUG` to enable the logging function `DEBUG_LOG`.
```c
#define DEBUG 
```

#### Hardware features extraction and fingerprints generation

1.DAC output the voltage. In the file "[app/dac.c](app/dac.c)" (line 101).

```c
uint32_t dac_set_value(int val){
	int prev_val = val;
	val %= 256;
	dac_init(DAC_OP_VALUE);
	/* GPIO 17*/
	ESP_ERROR_CHECK(dac_output_voltage(DAC_CHANNEL_1, val));
	/* GPIO 18*/
	ESP_ERROR_CHECK(dac_output_voltage(DAC_CHANNEL_2, val));
	return prev_val;
};
```

2.ADC read the voltage. In the file "[app/adc.c](app/adc.c)" (line 254).

```c
/* GPIO 16*/
adc2_get_raw(ADC2_CHANNEL_5, ADC_WIDTH_BIT_13, &raw_out);
voltage = esp_adc_cal_raw_to_voltage(raw_out, &adc2_chars);
ADC_ConvertedValues[0] = (volatile uint16_t)raw_out; // the raw data (e.g. 2979)
ADC_ConvertedValuesCorrected[0] = voltage; // voltage value (e.g. 1.2V)
```

3.Tips: how to change the used GPIOs. Sometimes the GPIOs are occupied and you may need alternative GPIOs.

You should modify the code in "[app/adc.c](app/adc.c)" as follows to replace GPIO19 with another GPIO.

Replace `GPIO_NUM_19` with other GPIO which is one of the ADC channel.

Replace `ADC2_CHANNEL_8` with other ADC channel.

Change the wire connection.

#### Data collection and preprocess

1.Data collection

Functions in `task_*.c` are used to data collection (e.g. "[fp_gen/task_voltage.c](fp_gen/task_voltage.c)" (line 22)).
```c
const task_func_multi voltage_tasks[] = {
	{0, dac_test},
	{1, adc_test},
	{2, dac_adc_test},
	{3, adc_ref_test},
	{4, pwm_voltage_test},
	{5, dac_adc_test_2},
	{6, get_trainset_testset},
};
```

The `send_package` function can send a package to the server. We send a special packet as
```c
typedef struct __attribute__((__packed__)) fp_event_simple {
	uint32_t eid_tid; // task_id type_id
	uint32_t result1; // result1 of task
	uint32_t result2; // result2 of task
} fp_evs;
```

Below is an example of collecting different voltage values. In the file "[fp_gen/task_voltage.c](fp_gen/task_voltage.c)" (line 209).
```c
int val = str2int(argv[4]); // output value of DAC
...
fp_evs ev;
ev.eid_tid = (TASK_ID) + (str2int(argv[2]) % 1000);
ev.result1 = (ADC_ConvertedValues[0] << 16) + ADC_ConvertedValues[1];
ev.result2 = ADC_ConvertedValues[2];
send_package((uint8_t *) &ev, sizeof(ev));
```

"[collect_data.py](../server/collect_data.py)" is used to collect these `fp_evs`s. The processed data is formatted as `id, result1, result2` (as shown in *.csv in "[raw_data](../server/raw_data/)"). We repeat a task several times to get enough data.

2.Data preprocess

There are only results in `*.csv`. The arguments used are predefined in `task_*.c`. We should add arguments information.

In the file "[fp_gen/task_voltage.c](fp_gen/task_voltage.c)" (line 240), we collect data for an ESP32S2 devices as follows
```c
// DAC/ADC task
// arguments are DAC output numbers [0,255]
// output are raw data and voltage data
for (int val = 0; val < 256; val++) {
	int2str(argv[4], val);
	dac_adc_test_2(argc, argv);
}

// PWM task
// arguments are duty, clock_source, frequency
// output is the voltage
for (int frequency = 2500; frequency < 6000; frequency += 2500) { // 2
	int2str(argv[6], frequency);
	for (int clock_source = 0; clock_source < 3; clock_source+=2) { // 2
		int2str(argv[4], clock_source);
		for (int duty = 16; duty < 8016; duty += 16) { // 500
			int2str(argv[5], duty);
			pwm_voltage_test(argc, argv);
			wdg_feed();
		}
	}
}
```

In the file "[dataProcess.py](../server/evaluation/dataProcess.py)" (line 585). The `esp32_format` corresponds to the task design and the `ESP32_*.csv` file in raw_data. 
```python
esp32_format = pd.DataFrame(columns=["arg1", "arg2", "arg3", "arg4"])
# DAC/ADC task, arg1 : output is voltage value or not
arg1 = list(np.array(list([0, 1]))) \\ 
 * len(range(0, 256, 1))
# PWM task, arg1 : duty
arg1 += list(range(16, 8016, 16)) \\
 * len(range(0, 3, 2)) * len(range(2500, 6000, 2500))
...
esp32_format["arg1"] = arg1
```

In this way, we preprocess the raw data and get a dataset.