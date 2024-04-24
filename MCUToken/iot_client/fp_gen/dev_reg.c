#include "dev_reg.h"
#include "utils.h"
#include "device_data.h"
#include "shell.h"
#include "aes.h"

extern device_instance deviceInstance;

extern void shell_printf(char *fmt, ...);

int dev_reg(int argc, char *argv[]) {
    (void) argc;
    (void) argv;
    printf("DEV_REG %s!\n", VERSION);
    dev_ini("2024041916348888", "202403122045", "device_secret");
    printf("DeviceData:%s|%s|%s\n", deviceInstance.device_id, deviceInstance.product_order,
           deviceInstance.device_secret);

    // 初始化密钥和IV。实际使用中应保证安全地生成和存储这些值
    uint8_t key[16] = {
            0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,
            0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c
    };
    uint8_t iv[16] = {
            0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
            0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f
    };

    struct AES_ctx ctx;
    AES_init_ctx_iv(&ctx, key, iv);

    int dataSize = sizeof(deviceInstance);
    int paddedSize = dataSize + (16 - (dataSize % 16)) % 16;
    uint8_t buffer[paddedSize];
    memset(buffer, 0, paddedSize);
    memcpy(buffer, &deviceInstance, dataSize);

    // 加密数据
    AES_CBC_encrypt_buffer(&ctx, buffer, paddedSize);
    printf("Encrypted data:\n");
    for (int i = 0; i < paddedSize; i++) {
        printf("%02X ", buffer[i]);
    }
    printf("\n");

    // 重置IV，因为加密操作会改变它
    AES_init_ctx_iv(&ctx, key, iv);
    AES_CBC_decrypt_buffer(&ctx, buffer, paddedSize);

    printf("Decrypted data:\n");
    printf("Device ID: %s\n", ((device_instance*)buffer)->device_id);
    printf("Product Order: %s\n", ((device_instance*)buffer)->product_order);
    printf("Device Secret: %s\n", ((device_instance*)buffer)->device_secret);
		
		return 0;
}
