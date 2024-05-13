//50 times aes for power consuming test
//
//#include <stdlib.h>
//#include "dev_reg.h"
//#include "utils.h"
//#include "device_data.h"
//#include "shell.h"
//#include "aes.h"
//#include "base64.h"
//
//
//extern device_instance deviceInstance;
//
//extern void shell_printf(char *fmt, ...);
//
//int dev_reg(int argc, char *argv[]) {
//    (void) argc;
//    (void) argv;
//    printf("DEV_REG Executing ........\n");
//    dev_ini("2024041916348888", "202403122045", "device_secret");
////    printf("DeviceData:%s|%s|%s\n", deviceInstance.device_id, deviceInstance.product_order,
////           deviceInstance.device_secret);
//
//    // 初始化密钥和IV。实际使用中应保证安全地生成和存储这些值
//    uint8_t key[16] = {
//            0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,
//            0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c
//    };
//    uint8_t iv[16] = {
//            0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
//            0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f
//    };
//
//    //秘钥初始化
//    struct AES_ctx ctx;
//    AES_init_ctx_iv(&ctx, key, iv);
//
//    //开始执行加密解密循环50次
//    printf("Encrypt and decrypt. execute 50 times:\n");
//    for (int i = 0; i < 50; i++) {
//        //填充数据
//        int dataSize = sizeof(deviceInstance);
//        int paddedSize = dataSize + (16 - (dataSize % 16)) % 16;
//        //uint8_t buffer[paddedSize];
//        uint8_t *buffer = (uint8_t *) malloc(paddedSize);
//        memset(buffer, 0, paddedSize);
//        memcpy(buffer, &deviceInstance, dataSize);
//
//        if (i == 0) {
//            //输出byte类型的device信息
//            printf("Device data in binary fmt:\n");
//            for (int i = 0; i < paddedSize; i++) {
//                printf("0x%02X,", buffer[i]);
//            }
//            printf("\n");
//        }
//
//        //加密，加密数据 ctx密码本 buffer被加密的输入输出s
//        AES_CBC_encrypt_buffer(&ctx, buffer, paddedSize);
//        //利用buffer_copy进行加解密操作避免出现buffer乱码情况
//        uint8_t *buffer_copy = (uint8_t *) malloc(paddedSize);
//        memcpy(buffer_copy, buffer, paddedSize);
//
//        //编码，对buffer_copy进行base64编码
//        int base64_length = 4 * ((paddedSize + 2) / 3);  // 计算Base64编码长度
//        char *base64data = malloc(base64_length + 1); // 分配内存，加1为终结符'\0'
//        //将buffer_copy编码为base64data,base64data(string)为输出
//        base64_encode(buffer_copy, paddedSize, base64data);
//
//        if (i == 0) {
//            printf("Encoded Base64 data:%s\n", base64data);
//        }
//
//        //解码
//        uint8_t *decoded_data = malloc(paddedSize); // 分配内存以存储解码后的数据
//        base64_decode(base64data, decoded_data, base64_length); // 解码，decoded_data为输出
//
//        //解密
//        // 重置IV，因为加密操作会改变它
//        AES_init_ctx_iv(&ctx, key, iv);
//        //使用decoded_data进行解密
//        AES_CBC_decrypt_buffer(&ctx, decoded_data, paddedSize);
//        printf("Current excuted times : %d   ", i);
//        free(buffer);
//        free(decoded_data);
//        free(base64data);
//        free(buffer_copy);
//    }
//    printf("-----------------------50 times excuted-----------------------");
//    return 0;
//}
