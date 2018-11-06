#ifndef __BSP_LED_H
#define __BSP_LED_H

#include "main.h"
#include "stm32f1xx_hal.h"

#define LED_1_CLK_ENABLE()       __HAL_RCC_GPIOB_CLK_ENABLE()
#define LED_1_PORT              GPIOB
#define LED_1_PIN               GPIO_PIN_0
#define LED_1_ON                LED_1_PORT->BRR = LED_1_PIN
#define LED_1_OFF               LED_1_PORT->BSRR = LED_1_PIN
#define LED_1_TOGGLE            LED_1_PORT->ODR ^= LED_1_PIN

void LED_Config(void);

#endif
