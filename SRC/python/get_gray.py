from spi_fun import SPI_FUN
import time
spi_fun = SPI_FUN(0)
while True:
    print(spi_fun.get_gray(),end='\r')
    time.sleep(0.5)
