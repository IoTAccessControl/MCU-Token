#include "flash_internal.h"
#include "timer.h"
#include "app_port.h"
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#if defined(USE_KEIL)

int sram_start_address = 0x20000000;

#define FLASH_TEST_DATA ((uint32_t)0x88152340)

static uint32_t get_sector(uint32_t address);

void flash_write_test(uint32_t start_addr, uint32_t end_addr, uint32_t test_data) {
	uint32_t first_sector, number_of_sectors, address = 0;
	uint32_t sector_error = 0;

	FLASH_EraseInitTypeDef EraseInitStruct;

	first_sector = get_sector(start_addr);
	number_of_sectors = get_sector(end_addr) - first_sector + 1;

	HAL_FLASH_Unlock();

	EraseInitStruct.TypeErase     = FLASH_TYPEERASE_SECTORS;
	EraseInitStruct.VoltageRange  = FLASH_VOLTAGE_RANGE_3;
	EraseInitStruct.Sector        = first_sector;
	EraseInitStruct.NbSectors     = number_of_sectors;

	// erase
	if (HAL_FLASHEx_Erase(&EraseInitStruct, &sector_error) != HAL_OK) {
		while (HAL_FLASHEx_Erase(&EraseInitStruct, &sector_error) != HAL_OK) {
			DEBUG_LOG("RETRY ERROR IN ERASE\n");
		}
	}

	// write
	address = start_addr;
	while (address < end_addr) {
		if (HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD, address, test_data) == HAL_OK) {
		  address += 4;
		}
		else {
		  DEBUG_LOG("ERROR IN WRITE: 0x%x\n", address);
		  break;
		}
	}

	HAL_FLASH_Lock();
}

void sram_write_test(uint32_t start_addr, uint32_t end_addr, uint32_t test_data) {
	for (uint32_t address = start_addr; address <= end_addr; address += 4) {
		memcpy((void *) start_addr,(void *) test_data, 4 * sizeof(uint32_t));

	}
}

static uint32_t get_sector(uint32_t address) {
  uint32_t sector = 0;

  if((address < ADDR_FLASH_SECTOR_1) && (address >= ADDR_FLASH_SECTOR_0)) {
    sector = FLASH_SECTOR_0;
  }
  else if((address < ADDR_FLASH_SECTOR_2) && (address >= ADDR_FLASH_SECTOR_1)) {
    sector = FLASH_SECTOR_1;
  }
  else if((address < ADDR_FLASH_SECTOR_3) && (address >= ADDR_FLASH_SECTOR_2)) {
    sector = FLASH_SECTOR_2;
  }
  else if((address < ADDR_FLASH_SECTOR_4) && (address >= ADDR_FLASH_SECTOR_3)) {
    sector = FLASH_SECTOR_3;
  }
  else if((address < ADDR_FLASH_SECTOR_5) && (address >= ADDR_FLASH_SECTOR_4)) {
    sector = FLASH_SECTOR_4;
  }
  else if((address < ADDR_FLASH_SECTOR_6) && (address >= ADDR_FLASH_SECTOR_5)) {
    sector = FLASH_SECTOR_5;
  }
  else if((address < ADDR_FLASH_SECTOR_7) && (address >= ADDR_FLASH_SECTOR_6)) {
    sector = FLASH_SECTOR_6;
  }
  else {
    sector = FLASH_SECTOR_7;
  }
  return sector;
}
#endif // USE_KEIL

#if defined(USE_ESP32)


int flash_start_address = 0x40080000;
int sram_start_address = 0x3FFD0000;

void flash_write_test(uint32_t start_addr, uint32_t end_addr, uint32_t test_data) {
}

void sram_write_test(uint32_t start_addr, uint32_t end_addr, uint32_t test_data) {

}
#endif // USE_ESP32

#if defined(USE_STM32F103)

int flash_start_address = 0x40080000;
int sram_start_address = 0x20000000;

void flash_write_test(uint32_t start_addr, uint32_t end_addr, uint32_t test_data) {
}

void sram_write_test(uint32_t start_addr, uint32_t end_addr, uint32_t test_data) {

}

#endif // USE_STM32F103

