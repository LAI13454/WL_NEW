#ifndef __BSP_IIC_H
#define __BSP_IIC_H

#include "main.h"
#include "stm32f1xx_hal.h"

#define USER_I2C_SCL_GPIO_ClK_ENABLE()		__HAL_RCC_GPIOC_CLK_ENABLE()
#define USER_I2C_SCL_GPIO_PORT	            GPIOC
#define USER_I2C_SCL_GPIO_PIN		        GPIO_PIN_4
#define USER_I2C_SDA_GPIO_ClK_ENABLE()	    __HAL_RCC_GPIOC_CLK_ENABLE()
#define USER_I2C_SDA_GPIO_PORT	            GPIOC
#define USER_I2C_SDA_GPIO_PIN		        GPIO_PIN_13

#define USER_I2C_SCL_1()		USER_I2C_SCL_GPIO_PORT->BSRR = USER_I2C_SCL_GPIO_PIN
#define USER_I2C_SCL_0()		USER_I2C_SCL_GPIO_PORT->BRR = USER_I2C_SCL_GPIO_PIN
#define USER_I2C_SDA_1()		USER_I2C_SDA_GPIO_PORT->BSRR = USER_I2C_SDA_GPIO_PIN
#define USER_I2C_SDA_0()		USER_I2C_SDA_GPIO_PORT->BRR = USER_I2C_SDA_GPIO_PIN

#define USER_I2C_SDA_READ()		((USER_I2C_SDA_GPIO_PORT->IDR&USER_I2C_SDA_GPIO_PIN) != 0)

#define I2C_WR	0
#define I2C_RD	1

void USER_I2C_Config(void);
uint8_t USER_I2C_Write(uint8_t dev_addr,uint8_t reg_addr,uint8_t i2c_len,uint8_t * i2c_data_buf);
uint8_t USER_I2C_Read(uint8_t dev_addr,uint8_t reg_addr,uint8_t i2c_len,uint8_t * i2c_data_buf);

void USER_I2C_Start(void);
void USER_I2C_Stop(void);
uint8_t USER_I2C_Wait_Ack(void);
uint8_t USER_I2C_SendByte(uint8_t data);
uint8_t USER_I2C_ReadByte(uint8_t ack);
#endif
