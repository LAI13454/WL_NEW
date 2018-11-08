/**
  ******************************************************************************
  * @file    stm32f1xx_it.c
  * @brief   Interrupt Service Routines.
  ******************************************************************************
  *
  * COPYRIGHT(c) 2018 STMicroelectronics
  *
  * Redistribution and use in source and binary forms, with or without modification,
  * are permitted provided that the following conditions are met:
  *   1. Redistributions of source code must retain the above copyright notice,
  *      this list of conditions and the following disclaimer.
  *   2. Redistributions in binary form must reproduce the above copyright notice,
  *      this list of conditions and the following disclaimer in the documentation
  *      and/or other materials provided with the distribution.
  *   3. Neither the name of STMicroelectronics nor the names of its contributors
  *      may be used to endorse or promote products derived from this software
  *      without specific prior written permission.
  *
  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
  * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
  * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
  * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
  * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
  * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
  * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
  * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
  *
  ******************************************************************************
  */
/* Includes ------------------------------------------------------------------*/
#include "stm32f1xx_hal.h"
#include "stm32f1xx.h"
#include "stm32f1xx_it.h"

/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/* External variables --------------------------------------------------------*/
extern SPI_HandleTypeDef hspi2;

/******************************************************************************/
/*            Cortex-M3 Processor Interruption and Exception Handlers         */ 
/******************************************************************************/

/**
* @brief This function handles Non maskable interrupt.
*/
void NMI_Handler(void)
{
  /* USER CODE BEGIN NonMaskableInt_IRQn 0 */

  /* USER CODE END NonMaskableInt_IRQn 0 */
  /* USER CODE BEGIN NonMaskableInt_IRQn 1 */

  /* USER CODE END NonMaskableInt_IRQn 1 */
}

/**
* @brief This function handles Hard fault interrupt.
*/
void HardFault_Handler(void)
{
  /* USER CODE BEGIN HardFault_IRQn 0 */

  /* USER CODE END HardFault_IRQn 0 */
  while (1)
  {
    /* USER CODE BEGIN W1_HardFault_IRQn 0 */
    /* USER CODE END W1_HardFault_IRQn 0 */
  }
  /* USER CODE BEGIN HardFault_IRQn 1 */

  /* USER CODE END HardFault_IRQn 1 */
}

/**
* @brief This function handles Memory management fault.
*/
void MemManage_Handler(void)
{
  /* USER CODE BEGIN MemoryManagement_IRQn 0 */

  /* USER CODE END MemoryManagement_IRQn 0 */
  while (1)
  {
    /* USER CODE BEGIN W1_MemoryManagement_IRQn 0 */
    /* USER CODE END W1_MemoryManagement_IRQn 0 */
  }
  /* USER CODE BEGIN MemoryManagement_IRQn 1 */

  /* USER CODE END MemoryManagement_IRQn 1 */
}

/**
* @brief This function handles Prefetch fault, memory access fault.
*/
void BusFault_Handler(void)
{
  /* USER CODE BEGIN BusFault_IRQn 0 */

  /* USER CODE END BusFault_IRQn 0 */
  while (1)
  {
    /* USER CODE BEGIN W1_BusFault_IRQn 0 */
    /* USER CODE END W1_BusFault_IRQn 0 */
  }
  /* USER CODE BEGIN BusFault_IRQn 1 */

  /* USER CODE END BusFault_IRQn 1 */
}

/**
* @brief This function handles Undefined instruction or illegal state.
*/
void UsageFault_Handler(void)
{
  /* USER CODE BEGIN UsageFault_IRQn 0 */

  /* USER CODE END UsageFault_IRQn 0 */
  while (1)
  {
    /* USER CODE BEGIN W1_UsageFault_IRQn 0 */
    /* USER CODE END W1_UsageFault_IRQn 0 */
  }
  /* USER CODE BEGIN UsageFault_IRQn 1 */

  /* USER CODE END UsageFault_IRQn 1 */
}

/**
* @brief This function handles System service call via SWI instruction.
*/
void SVC_Handler(void)
{
  /* USER CODE BEGIN SVCall_IRQn 0 */

  /* USER CODE END SVCall_IRQn 0 */
  /* USER CODE BEGIN SVCall_IRQn 1 */

  /* USER CODE END SVCall_IRQn 1 */
}

/**
* @brief This function handles Debug monitor.
*/
void DebugMon_Handler(void)
{
  /* USER CODE BEGIN DebugMonitor_IRQn 0 */

  /* USER CODE END DebugMonitor_IRQn 0 */
  /* USER CODE BEGIN DebugMonitor_IRQn 1 */

  /* USER CODE END DebugMonitor_IRQn 1 */
}

/**
* @brief This function handles Pendable request for system service.
*/
void PendSV_Handler(void)
{
  /* USER CODE BEGIN PendSV_IRQn 0 */

  /* USER CODE END PendSV_IRQn 0 */
  /* USER CODE BEGIN PendSV_IRQn 1 */

  /* USER CODE END PendSV_IRQn 1 */
}

/**
* @brief This function handles System tick timer.
*/
void SysTick_Handler(void)
{
  /* USER CODE BEGIN SysTick_IRQn 0 */

  /* USER CODE END SysTick_IRQn 0 */
  HAL_IncTick();
  HAL_SYSTICK_IRQHandler();
  /* USER CODE BEGIN SysTick_IRQn 1 */

  /* USER CODE END SysTick_IRQn 1 */
}

/******************************************************************************/
/* STM32F1xx Peripheral Interrupt Handlers                                    */
/* Add here the Interrupt Handlers for the used peripherals.                  */
/* For the available peripheral interrupt handler names,                      */
/* please refer to the startup file (startup_stm32f1xx.s).                    */
/******************************************************************************/

/**
* @brief This function handles SPI2 global interrupt.
*/
static uint8_t count =0;
void SPI2_IRQHandler(void)
{
  /* USER CODE BEGIN SPI2_IRQn 0 */
  extern uint16_t gray_data_final;
  extern uint16_t gray_data_two_final;
  extern uint16_t other_data_final;
  uint8_t other_status_final = 0x11;
  static bool start=false;
  static uint8_t data_use_r = 0x00;    //接受执行返回
  static uint8_t buf[5] = {0};
  static uint8_t tx_buf[2] = {0x01,0x02};
  
  if((SPI2->DR == 0xaa) && (start == false)){     //收到头0xaa
    start = true;
    count ++;
    SPI2->DR = other_status_final;                              //可替换成程序运行开关状态，发送在第二位
  }else if((start == true) && (count == 1)){      //收到控制位，代表后两位要发的东西
    buf[0] = SPI2->DR;
    SPI2->DR = other_status_final;
    count ++;
  }else if((start == true) && (count == 2)){      //收到高8位，发送控制位
    buf[1] = SPI2->DR;
    SPI2->DR = buf[0];
    count ++;
  }else if((start == true) && (count == 3)){      //收到低8位，发送数据位
    buf[2] = SPI2->DR;
    SPI2->DR = tx_buf[0];
    count ++;
  }else if((start == true) && (count == 4)){      //发送数据位
    SPI2->DR = tx_buf[1];
    count ++;
  }else if((start == true) && (count == 5)){      //发送数据校验
    SPI2->DR = (tx_buf[0] + tx_buf[1]) & 0xff;
    count ++;
  }else if((start == true) && (count == 6)){      //发送数据使用情况
    buf[3] = SPI2->DR;
    SPI2->DR = data_use_r;
    count ++;
  }else{
    count = 0;
    start = false;
  }

  uint8_t temp_num = 0xaa + buf[0] +buf[1] +buf[2];
  
  if(buf[0] == 0x21){
    tx_buf[0] = ((gray_data_final&0xff00)>>8);
    tx_buf[1] = (gray_data_final&0x00ff);
  }else if(buf[0] == 0x22){
    tx_buf[0] = ((gray_data_two_final&0xff00)>>8);
    tx_buf[1] = (gray_data_two_final&0x00ff);
  }else if((buf[0]&0xf0) == 0x50){
    uint16_t steer_temp = 0x00;
    switch(buf[0]){
      case 0x51:
        steer_temp = 0x01;
        //steer_temp = TIM3->CCR4 - 1500;
        tx_buf[0] = ((steer_temp&0xff00)>>8);
        tx_buf[1] = (steer_temp&0x00ff);
        break;
      case 0x52:
        steer_temp = 0x02;
        //steer_temp = TIM3->CCR3 - 1500;
        tx_buf[0] = ((steer_temp&0xff00)>>8);
        tx_buf[1] = (steer_temp&0x00ff);
        break;
      case 0x53:
        steer_temp = 0x03;
        //steer_temp = TIM3->CCR2 - 1500;
        tx_buf[0] = ((steer_temp&0xff00)>>8);
        tx_buf[1] = (steer_temp&0x00ff);
        break;
      case 0x54:
        steer_temp = 0x04;
        //steer_temp = TIM3->CCR1 - 1500;
        tx_buf[0] = ((steer_temp&0xff00)>>8);
        tx_buf[1] = (steer_temp&0x00ff);
        break;
      case 0x55:
        steer_temp = 0x05;
        //steer_temp = TIM2->CCR4 - 1500;
        tx_buf[0] = ((steer_temp&0xff00)>>8);
        tx_buf[1] = (steer_temp&0x00ff);
        break;
      case 0x56:
        steer_temp = 0x06;
        //steer_temp = TIM2->CCR3 - 1500;
        tx_buf[0] = ((steer_temp&0xff00)>>8);
        tx_buf[1] = (steer_temp&0x00ff);
        break;
      case 0x57:
        steer_temp = 0x07;
        //steer_temp = TIM2->CCR2 - 1500;
        tx_buf[0] = ((steer_temp&0xff00)>>8);
        tx_buf[1] = (steer_temp&0x00ff);
        break;
      case 0x58:
        steer_temp = 0x08;
        //steer_temp = TIM2->CCR1 - 1500;
        tx_buf[0] = ((steer_temp&0xff00)>>8);
        tx_buf[1] = (steer_temp&0x00ff);
        break;
    }
  }

  if(count == 1){
    data_use_r = 0;
  }
  if(temp_num == buf[3]){
    if((buf[0] == 0x05) && count == 5){
      int16_t temp = (buf[1]<<8 | buf[2]);
      if(temp >= 0){
        TIM1->CCR3 = temp;
        TIM1->CCR4 = 0;
        TIM1->CCR1 = temp;
        TIM1->CCR2 = 0;
      }else{
        TIM1->CCR3 = 0;
        TIM1->CCR4 = -temp;
        TIM1->CCR1 = 0;
        TIM1->CCR2 = -temp;
      }
      data_use_r = 1;
    }else if((buf[0] == 0x01) && count == 5){
      int16_t temp = (buf[1]<<8 | buf[2]);
      if(temp >= 0){
        TIM1->CCR3 = temp;
        TIM1->CCR4 = 0;
      }else{
        TIM1->CCR3 = 0;
        TIM1->CCR4 = -temp;
      }
      data_use_r = 1;
    }else if((buf[0] == 0x02) && count == 5){
      int16_t temp = (buf[1]<<8 | buf[2]);
      if(temp >= 0){
        TIM1->CCR1 = temp;
        TIM1->CCR2 = 0;
      }else{
        TIM1->CCR1 = 0;
        TIM1->CCR2 = -temp;
      }
      data_use_r = 1;
    }else if((buf[0] == 0x11) && count == 5){
      int16_t temp = (buf[1]<<8 | buf[2]);
      TIM3->CCR4 = 1500 + temp;
      data_use_r = 1;
    }else if((buf[0] == 0x12) && count == 5){
      int16_t temp = (buf[1]<<8 | buf[2]);
      TIM3->CCR3 = 1500 + temp;
      data_use_r = 1;
    }else if((buf[0] == 0x13) && count == 5){
      int16_t temp = (buf[1]<<8 | buf[2]);
      TIM3->CCR2 = 1500 + temp;
      data_use_r = 1;
    }else if((buf[0] == 0x14) && count == 5){
      int16_t temp = (buf[1]<<8 | buf[2]);
      TIM3->CCR1 = 1500 + temp;
      data_use_r = 1;
    }else if((buf[0] == 0x15) && count == 5){
      int16_t temp = (buf[1]<<8 | buf[2]);
      TIM2->CCR4 = 1500 + temp;
      data_use_r = 1;
    }else if((buf[0] == 0x16) && count == 5){
      int16_t temp = (buf[1]<<8 | buf[2]);
      TIM2->CCR3 = 1500 + temp;
      data_use_r = 1;
    }else if((buf[0] == 0x17) && count == 5){
      int16_t temp = (buf[1]<<8 | buf[2]);
      TIM2->CCR2 = 1500 + temp;
      data_use_r = 1;
    }else if((buf[0] == 0x18) && count == 5){
      int16_t temp = (buf[1]<<8 | buf[2]);
      TIM2->CCR1 = 1500 + temp;
      data_use_r = 1;
    }
  }
  /* USER CODE END SPI2_IRQn 0 */
  //HAL_SPI_IRQHandler(&hspi2);
  /* USER CODE BEGIN SPI2_IRQn 1 */
  /*if(buf[0] == 0x01){
    int16_t temp = (buf[1]<<8 | buf[2]);
    if(temp >= 0){
      TIM1->CCR3 = temp;
      TIM1->CCR4 = 0;
    }else{
      TIM1->CCR3 = 0;
      TIM1->CCR4 = -temp;
    }
  }else if(buf[0] == 0x02){
    int16_t temp = (buf[1]<<8 | buf[2]);
    if(temp >= 0){
      TIM1->CCR1 = temp;
      TIM1->CCR2 = 0;
    }else{
      TIM1->CCR1 = 0;
      TIM1->CCR2 = -temp;
    }
  }else if(buf[0] == 0x11){
    int16_t temp = (buf[1]<<8 | buf[2]);
    TIM3->CCR4 = 1500 + temp;
  }else if(buf[0] == 0x12){
    int16_t temp = (buf[1]<<8 | buf[2]);
    TIM3->CCR3 = 1500 + temp;
  }else if(buf[0] == 0x13){
    int16_t temp = (buf[1]<<8 | buf[2]);
    TIM3->CCR2 = 1500 + temp;
  }else if(buf[0] == 0x14){
    int16_t temp = (buf[1]<<8 | buf[2]);
    TIM3->CCR1 = 1500 + temp;
  }else if(buf[0] == 0x15){
    int16_t temp = (buf[1]<<8 | buf[2]);
    TIM2->CCR4 = 1500 + temp;
  }else if(buf[0] == 0x16){
    int16_t temp = (buf[1]<<8 | buf[2]);
    TIM2->CCR3 = 1500 + temp;
  }else if(buf[0] == 0x17){
    int16_t temp = (buf[1]<<8 | buf[2]);
    TIM2->CCR2 = 1500 + temp;
  }else if(buf[0] == 0x18){
    int16_t temp = (buf[1]<<8 | buf[2]);
    TIM2->CCR1 = 1500 + temp;
  }else if(buf[0] == 0x21){
    if(count == 4){
      SPI2->DR = ((gray_data_final&0xff00)>>8);
    }
    else if(count == 5){
      SPI2->DR = (gray_data_final&0x00ff);
    }
  }else if(buf[0] == 0x22){
    if(count == 4){
      SPI2->DR = ((gray_data_two_final&0xff00)>>8);
    }
    else if(count == 5){
      SPI2->DR = (gray_data_two_final&0x00ff);
    }
  }else if(buf[0] == 0x31){
    if(count == 4){
      SPI2->DR = ((other_data_final&0xff00)>>8);
    }
    else if(count == 5){
      SPI2->DR = (other_data_final&0x00ff);
    }
  }
  */
  /* USER CODE END SPI2_IRQn 1 */
}

/* USER CODE BEGIN 1 */

/* USER CODE END 1 */
/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
