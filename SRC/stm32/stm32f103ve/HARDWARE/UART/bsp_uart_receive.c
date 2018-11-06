#include "bsp_uart_receive.h"
void UART_Receive_Config(void){
    UART_GPIO_CLK_ENABLE();
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.Pin = UART_GPIO_PIN;
    GPIO_InitStructure.Mode = GPIO_MODE_AF_INPUT;
    GPIO_InitStructure.Pull = GPIO_NOPULL;
    GPIO_InitStructure.Speed = GPIO_SPEED_FREQ_HIGH;
    HAL_GPIO_Init(UART_GPIO_PORT,&GPIO_InitStructure);

    UART_CLK_ENABLE();
    __HAL_RCC_AFIO_CLK_ENABLE();
    //__HAL_AFIO_REMAP_SWJ_NOJTAG();
    __HAL_AFIO_REMAP_USART1_ENABLE();
    
    USART_HandleTypeDef USART_HandleStructure;
    USART_HandleStructure.Instance = UARTx;
    USART_HandleStructure.Init.BaudRate = 115200;
    USART_HandleStructure.Init.WordLength = USART_WORDLENGTH_8B;
    USART_HandleStructure.Init.StopBits = USART_STOPBITS_1;
    USART_HandleStructure.Init.Parity = USART_PARITY_NONE;
    USART_HandleStructure.Init.Mode = USART_MODE_RX;
    if(HAL_USART_Init(&USART_HandleStructure) == HAL_OK){
    }
    UARTx->CR1 |= 0x4000;
}