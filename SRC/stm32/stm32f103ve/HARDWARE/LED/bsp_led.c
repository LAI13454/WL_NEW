#include "bsp_led.h"

void LED_Config(void){
    LED_1_CLK_ENABLE();
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.Pin = LED_1_PIN;
    GPIO_InitStructure.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStructure.Pull = GPIO_NOPULL;
    GPIO_InitStructure.Speed = GPIO_SPEED_FREQ_MEDIUM;
    HAL_GPIO_Init(LED_1_PORT,&GPIO_InitStructure);
    LED_1_PORT->BSRR = LED_1_PIN;
}