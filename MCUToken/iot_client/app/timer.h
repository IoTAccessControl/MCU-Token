#ifndef TIMER_H_
#define TIMER_H_

#include "defs.h"
#include "app_port.h"

void reset_timer_tick(void);
uint32_t get_cur_tick(void);
float tick_to_us(int tick);

#endif
