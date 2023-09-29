#ifndef FLASH_INTERNAL_H
#define FLASH_INTERNAL_H

#include <utils.h>

#if defined(USE_KEIL)
#include "stm32f4xx.h"
#include <stm32f4xx_hal_flash.h>

/* Base address of the Flash sectors */
#define ADDR_FLASH_SECTOR_0     ((uint32_t)0x08000000) /* Base address of Sector 0, 16 Kbytes   */
#define ADDR_FLASH_SECTOR_1     ((uint32_t)0x08004000) /* Base address of Sector 1, 16 Kbytes   */
#define ADDR_FLASH_SECTOR_2     ((uint32_t)0x08008000) /* Base address of Sector 2, 16 Kbytes   */
#define ADDR_FLASH_SECTOR_3     ((uint32_t)0x0800C000) /* Base address of Sector 3, 16 Kbytes   */
#define ADDR_FLASH_SECTOR_4     ((uint32_t)0x08010000) /* Base address of Sector 4, 64 Kbytes   */
#define ADDR_FLASH_SECTOR_5     ((uint32_t)0x08020000) /* Base address of Sector 5, 128 Kbytes  */
#define ADDR_FLASH_SECTOR_6     ((uint32_t)0x08040000) /* Base address of Sector 6, 128 Kbytes  */
#define ADDR_FLASH_SECTOR_7     ((uint32_t)0x08060000) /* Base address of Sector 7, 128 Kbytes  */

#endif // USE_KEIL

// we do not implement flash fingerprint in our work.

void flash_write_test(uint32_t start_addr, uint32_t end_addr, uint32_t test_data);
void sram_write_test(uint32_t start_addr, uint32_t end_addr, uint32_t test_data);

#endif /* __INTERNAL_FLASH_H */
