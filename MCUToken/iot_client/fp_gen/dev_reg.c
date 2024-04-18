#include "dev_reg.h"
#include "utils.h"
#include "device_data.h"


//extern void dev_ini(char* device_id,char* product_order,char* device_secret);
extern device_instance deviceInstance;

int dev_reg(int argc, char *argv[]){
    (void) argc;
    (void) argv;
    printf("DEV_REG %s!\n", VERSION);
    dev_ini("2024031220451223","202403122045","device_secret");
	printf("Device_id %s: \n Produce_order: %s \n Device_secret: %s \n",deviceInstance.device_id,deviceInstance.product_order,deviceInstance.device_secret);
    return 0;
};
