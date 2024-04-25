//
// Created by admin on 2024/4/18.
//

#ifndef MCU_TOKEN_DEVICE_DATA_H
#define MCU_TOKEN_DEVICE_DATA_H
#include <string.h>
#include "app_port.h"
#include "shell.h"
#include "usart.h"

typedef struct {
    const char* device_id;      // 设备ID
    const char* product_order;  // 产品订单号
    char* device_secret;        // 设备密钥
} device_instance;


//extern device_instance deviceInstance;

//device initialization
void dev_ini(char* device_id,char* product_order,char* device_secret);

//void updateDeviceSecret(device_instance* dev);

#endif //MCU_TOKEN_DEVICE_DATA_H
