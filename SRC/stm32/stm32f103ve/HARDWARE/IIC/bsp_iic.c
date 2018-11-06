#include "bsp_iic.h"

void delay_us(uint8_t us){
	uint8_t i;
	for (i = 0; i < us * 4; i++);
}

static void USER_I2C_GPIO_Config(void)
{
	GPIO_InitTypeDef GPIO_InitStructure;
	USER_I2C_SCL_GPIO_ClK_ENABLE();
	USER_I2C_SDA_GPIO_ClK_ENABLE();
	GPIO_InitStructure.Pin = USER_I2C_SCL_GPIO_PIN;
	GPIO_InitStructure.Mode = GPIO_MODE_OUTPUT_PP;
	GPIO_InitStructure.Pull = GPIO_NOPULL;
	GPIO_InitStructure.Speed = GPIO_SPEED_FREQ_HIGH;
	HAL_GPIO_Init(USER_I2C_SCL_GPIO_PORT,&GPIO_InitStructure);
	GPIO_InitStructure.Pin = USER_I2C_SDA_GPIO_PIN;
	GPIO_InitStructure.Mode = GPIO_MODE_OUTPUT_OD;
	HAL_GPIO_Init(USER_I2C_SDA_GPIO_PORT,&GPIO_InitStructure);
}

void USER_I2C_Config(void)
{
	USER_I2C_GPIO_Config();
}

void USER_I2C_Start(void)
{
	USER_I2C_SDA_1();
	USER_I2C_SCL_1();
	delay_us(4);
	USER_I2C_SDA_0();
	delay_us(4);
	USER_I2C_SCL_0();
}

void USER_I2C_Stop(void)
{
	USER_I2C_SCL_0();
	USER_I2C_SDA_0();
	delay_us(4);
	USER_I2C_SCL_1();
	USER_I2C_SDA_1();
	delay_us(4);
}

uint8_t USER_I2C_Wait_Ack(void)
{
	uint8_t ucErrTime = 0;
	USER_I2C_SDA_1();
	delay_us(1);
	USER_I2C_SCL_1();
	delay_us(1);
	while(USER_I2C_SDA_READ())
	{
		ucErrTime ++;
		if(ucErrTime > 250)
		{
			USER_I2C_Stop();
			return 1;
		}
	}
	USER_I2C_SCL_0();
	return 0;
}

static void USER_I2C_Ack(void)
{
	USER_I2C_SCL_0();
	USER_I2C_SDA_0();
	delay_us(2);
	USER_I2C_SCL_1();
	delay_us(2);
	USER_I2C_SCL_0();
}

static void USER_I2C_NAck(void)
{
	USER_I2C_SCL_0();
	USER_I2C_SDA_1();
	delay_us(2);
	USER_I2C_SCL_1();
	delay_us(2);
	USER_I2C_SCL_0();
}



uint8_t USER_I2C_SendByte(uint8_t data)
{
	uint8_t i;
	USER_I2C_SCL_0();
	for(i=0;i<8;i++)
	{
		if(data&0x80)
			USER_I2C_SDA_1();
		else
			USER_I2C_SDA_0();
		data <<= 1;
		delay_us(2);
		USER_I2C_SCL_1();
		delay_us(2);
		USER_I2C_SCL_0();
		delay_us(2);
	}
	return USER_I2C_Wait_Ack();
}



uint8_t USER_I2C_ReadByte(uint8_t ack)
{
	uint8_t i,data;
	USER_I2C_SDA_1();
	USER_I2C_SCL_0();
	data = 0;
	for(i=0;i<8;i++)
	{
		USER_I2C_SCL_0();
		delay_us(2);
		USER_I2C_SCL_1();
		data <<= 1;
		if(USER_I2C_SDA_READ())
			data ++;
		delay_us(1);
	}
	if(!ack)
		USER_I2C_NAck();
	else
		USER_I2C_Ack();
	return data;
}

uint8_t USER_I2C_Write(uint8_t dev_addr,uint8_t reg_addr,uint8_t i2c_len,uint8_t * i2c_data_buf)
{
	uint8_t i,result = 0;
	USER_I2C_Start();
	result = USER_I2C_SendByte((dev_addr<<1) | I2C_WR);
	if(result)	return result;
	result = USER_I2C_SendByte(reg_addr);
	if(result)	return result;
	for(i=0;i<i2c_len;i++)
	{
		result = USER_I2C_SendByte(i2c_data_buf[i]);
		if(result)	return result;
	}
	USER_I2C_Stop();
	return 0;
}

uint8_t USER_I2C_Read(uint8_t dev_addr,uint8_t reg_addr,uint8_t i2c_len,uint8_t * i2c_data_buf)
{
	uint8_t result;
	USER_I2C_Start();
	result = USER_I2C_SendByte((dev_addr<<1) | I2C_WR);
	if(result)	return result;
	result = USER_I2C_SendByte(reg_addr);
	if(result)	return result;
	USER_I2C_Start();
	result = USER_I2C_SendByte((dev_addr<<1) | I2C_RD);
	if(result)	return result;
	while(i2c_len)
	{
		if(i2c_len == 1)
			*i2c_data_buf = USER_I2C_ReadByte(0);
		else
			*i2c_data_buf = USER_I2C_ReadByte(1);
		i2c_data_buf ++;
		i2c_len --;
	}
	USER_I2C_Stop();
	return 0;
}
