#pragma once

// adc
#include <ads1115.h>
#define MY_PINBASE 2222
#define ch0 MY_PINBASE + 0
#define ch1 MY_PINBASE + 1
#define ch2 MY_PINBASE + 2
#define ch3 MY_PINBASE + 3

void init_adc(void);

void init_adc(void)
{
    ads1115Setup(MY_PINBASE, 0x48);
    return;
}