### Usage

support devices
> ESP32S2 ： https://www.espressif.com.cn/en/products/socs/esp32-s2
> 
> STM32F103C8 ： https://stm32-base.org/boards/STM32F103C8T6-Blue-Pill
> 
> STM32F429-Discovery ： https://www.st.com/en/evaluation-tools/stm32f4discovery.html

#### ESP32

1. Download ESP-IDF (version 4.4).

2. Come to the filedir "*Device-porting/ESP32/esp32s2*".

3. Build and download programs as below:
```
# Initialization
$ idf.py set-target esp32s2
$ idf.py menuconfig

# Compare
$ idf.py build

# Download
$ idf.py flash
```

4. Connect PINs with dupont wire as below:
> P5 -- P12
> P16 -- P17
> P18 -- P19

Besides, you should make sure the device connected with PC correctly and the USART work. 

#### STM32F103 && STM32F429

Open the keil project, compare and download programs directly.  

Also, you should make sure the device connected with PC correctly and the usart work. 

The PINs are connected as below.

STM32F103
> PA2 -- PB5

STM32F429
> PA5 -- PC7

If your GPIOs used below are occupied, you can refer to "[../MCUToken/iot_client/readme.md](../MCUToken/iot_client/readme.md)" to change the PINs used.

### Data collection && Token generation

If you have a real device and the wires are connected correctly, you can use the following commands (via the serial port) to collect data and generate tokens.

```bash
# token generation
# we limit the number of arguments to less than 10
token_gen {command} {payload_0} {payload_1} {...}

# for example (set temperature on a car)
token_gen SET_TEM SEAT1 25 SEAT2 26

# data collection
# FPU tasks
fp_gen STM32 11010 0 0
# RTC tasks
fp_gen STM32 14004 0 0 0 0 0 0 0
# DAC/ADC && PWM tasks
fp_gen STM32 13006 0 0 0 0 0 0 0
# SRAM tasks
fp_gen STM32 15001 0 0
# encryption
fp_gen STM32 16000 1
```

### Simulate in renode

We provide a simulation for STM32F429 based on the ReNode (https://renode.io/).

1.Make sure you have installed renode.

2.Follow the next steps and you can get a example of collecting RTC fingerprints. We suggest that you try generating tokens instead of collecting training data, as there are unknown bugs in the simulator. What's more, because the timer on the simulator is unless, so the results of the tasks are 0.

```bash
cd renode_emulate

... # open a renode bash
renode

include @scripts/single-node/stm32f4_discovery.resc 
sysbus LoadELF @STM32F429I-Discovery.axf
showAnalyzer usart1

start
# Token generate for one command
usart1 WriteLine "token_gen UNLOCK_DOOR"
usart1 WriteChar 10

usart1 WriteLine "token_gen SET_TEM SEAT1 25 SEAT2 26"
usart1 WriteChar 10

# FPU tasks
usart1 WriteLine "fp_gen STM32 11010 0 0"
usart1 WriteChar 10

# RTC tasks
usart1 WriteLine "fp_gen STM32 14004 0 0 0 0 0 0 0"
usart1 WriteChar 10
```

Tips:

- The clock task corresponds to the task in `MCUToken/iot_client/fp_gen/task_clock.c Line 363` and `MCUToken/server/tasks/task_clock.yaml`. 

- Unfortunately, Renode cannot read the MCU main frequency time, so the task execution result cannot be displayed normally. At the same time, the serial port in the simulator will be damaged after a task is executed. But these problems don't occur on real hardware.

### An example on ESP32S2

Here we give a running example on ESP32S2.

After flashing the firmwire, you can see initialization information as below.
```bash
  version: Show Version Code
  fp_gen: fp_gen STM32. Generate fringerprint data for specific platforms.
  token_gen: Generate token for the target command
$ 
```

Run `fp_gen STM32 11010 0 0` and you can get the log in your COM as below (the output are sequences of u8 so they are unreadable).
```bash
  version: Show Version Code
  fp_gen: fp_gen STM32. Generate fringerprint data for specific platforms.
  token_gen: Generate token for the target command
$ fp_gen STM32 13006 0 0 0 0 0 0 0
?□|?
?□l?
...
Finish Task: 3006
$ 
```

### Expand new devices

1. Complete basic development and ensure the usart work.

2. Implement the function *usart_getchar* and *uart_putchar*.
*usart_getchar* is used to get a byte from usart and *uart_putchar* is used to send a byte to usart.

3. Include files in dictionary "*../MCUToken/iot_client/app*" and "*../MCUToken/iot_client/fp_gen*". Implement the functions in files of "*../MCUToken/iot_client/app*". Different devices are controlled by using macros.
