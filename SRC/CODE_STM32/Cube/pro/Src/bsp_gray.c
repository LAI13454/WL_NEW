#include "bsp_gray.h"


uint16_t get_gray(uint8_t num){
  uint16_t gray_data = 0x0000;
  switch(num){
    case 0:
      GRAY0_GPIO_Port->BRR |= GRAY0_Pin;
      GRAY1_GPIO_Port->BRR |= GRAY1_Pin;
      GRAY2_GPIO_Port->BRR |= GRAY2_Pin;
      GRAY3_GPIO_Port->BRR |= GRAY3_Pin;
      gray_data |= HAL_GPIO_ReadPin(GRAY4_GPIO_Port,GRAY4_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY5_GPIO_Port,GRAY5_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY6_GPIO_Port,GRAY6_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY7_GPIO_Port,GRAY7_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY8_GPIO_Port,GRAY8_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY9_GPIO_Port,GRAY9_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY10_GPIO_Port,GRAY10_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY11_GPIO_Port,GRAY11_Pin);
      gray_data = gray_data << 1;
      GRAY0_GPIO_Port->BSRR |= GRAY0_Pin;
      GRAY1_GPIO_Port->BRR |= GRAY1_Pin;
      GRAY2_GPIO_Port->BRR |= GRAY2_Pin;
      GRAY3_GPIO_Port->BRR |= GRAY3_Pin;
      gray_data |= HAL_GPIO_ReadPin(GRAY4_GPIO_Port,GRAY4_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY5_GPIO_Port,GRAY5_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY6_GPIO_Port,GRAY6_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY7_GPIO_Port,GRAY7_Pin);
      break;
    case 1:
      GRAY0_GPIO_Port->BSRR |= GRAY0_Pin;
      GRAY1_GPIO_Port->BSRR |= GRAY1_Pin;
      GRAY2_GPIO_Port->BRR |= GRAY2_Pin;
      GRAY3_GPIO_Port->BRR |= GRAY3_Pin;
      gray_data |= HAL_GPIO_ReadPin(GRAY4_GPIO_Port,GRAY4_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY5_GPIO_Port,GRAY5_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY6_GPIO_Port,GRAY6_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY7_GPIO_Port,GRAY7_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY8_GPIO_Port,GRAY8_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY9_GPIO_Port,GRAY9_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY10_GPIO_Port,GRAY10_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY11_GPIO_Port,GRAY11_Pin);
      break;
    case 2:
      GRAY0_GPIO_Port->BSRR |= GRAY0_Pin;
      GRAY1_GPIO_Port->BRR |= GRAY1_Pin;
      GRAY2_GPIO_Port->BRR |= GRAY2_Pin;
      GRAY3_GPIO_Port->BRR |= GRAY3_Pin;
      gray_data |= HAL_GPIO_ReadPin(GRAY8_GPIO_Port,GRAY8_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY9_GPIO_Port,GRAY9_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY10_GPIO_Port,GRAY10_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY11_GPIO_Port,GRAY11_Pin);
      gray_data = gray_data << 1;
      GRAY0_GPIO_Port->BRR |= GRAY0_Pin;
      GRAY1_GPIO_Port->BSRR |= GRAY1_Pin;
      GRAY2_GPIO_Port->BRR |= GRAY2_Pin;
      GRAY3_GPIO_Port->BRR |= GRAY3_Pin;
      gray_data |= HAL_GPIO_ReadPin(GRAY4_GPIO_Port,GRAY4_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY5_GPIO_Port,GRAY5_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY6_GPIO_Port,GRAY6_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY7_GPIO_Port,GRAY7_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY8_GPIO_Port,GRAY8_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY9_GPIO_Port,GRAY9_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY10_GPIO_Port,GRAY10_Pin);
      gray_data = gray_data << 1;
      gray_data |= HAL_GPIO_ReadPin(GRAY11_GPIO_Port,GRAY11_Pin);
      break;
  }
  return gray_data;
}

uint16_t get_other(void){
  uint16_t other_data = 0x0000;
  other_data |= HAL_GPIO_ReadPin(RED_GPIO_Port,RED_Pin);
  return other_data;
}
