#ifndef __BSP_UART_RECEIVE_H
#define __BSP_UART_RECEIVE_H

#include "main.h"
#include "stm32f1xx_hal.h"
#include "stm32f1xx_hal_usart.h"
#include "stm32f1xx_hal_gpio_ex.h"

#define UART_GPIO_CLK_ENABLE()      __HAL_RCC_GPIOB_CLK_ENABLE()
#define UART_GPIO_PORT              GPIOB
#define UART_GPIO_PIN               GPIO_PIN_7

#define UARTx                       USART1
#define UART_CLK_ENABLE()           __HAL_RCC_USART1_CLK_ENABLE()

void UART_Receive_Config(void);

#endif