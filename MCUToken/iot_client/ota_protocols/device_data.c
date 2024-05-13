//
// Created by admin on 2024/4/18.
//

#include "device_data.h"

device_instance deviceInstance;

void dev_ini(char* device_id,char* product_order,char* device_secret){
    deviceInstance.device_id=device_id;
    deviceInstance.product_order=product_order;
    deviceInstance.device_secret=device_secret;
};
