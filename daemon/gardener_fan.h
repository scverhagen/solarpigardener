#pragma once

#define pin_fan 0

void init_fan(void);
void gardener_fan_on(void);
void gardener_fan_off(void);

void init_fan(void)
{
    pinMode(pin_fan, OUTPUT);
    digitalWrite(pin_fan, LOW);
}

void gardener_fan_on(void)
{
    digitalWrite(pin_fan, HIGH);
}

void gardener_fan_off(void)
{
    digitalWrite(pin_fan, LOW);
}
