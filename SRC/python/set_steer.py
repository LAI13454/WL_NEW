import sys
from spi_fun import SPI_FUN
spi_fun = SPI_FUN(0)
if len(sys.argv) == 3:
    if sys.argv[1] == '0':
        spi_fun.set_steer_turn(int(sys.argv[2]))
    if sys.argv[1] == '1':
        spi_fun.set_steer(1,int(sys.argv[2]))
    if sys.argv[1] == '2':
        spi_fun.set_steer(2,int(sys.argv[2]))
    if sys.argv[1] == '3':
        spi_fun.set_steer(3,int(sys.argv[2]))  
    if sys.argv[1] == '4':
        spi_fun.set_steer(4,int(sys.argv[2]))
    if sys.argv[1] == '5':
        spi_fun.set_steer(5,int(sys.argv[2]))
    if sys.argv[1] == '6':
        spi_fun.set_steer(6,int(sys.argv[2]))
    if sys.argv[1] == '10':
        spi_fun.set_steer(0,int(sys.argv[2]))
    if sys.argv[1] == '11':
        spi_fun.set_steer(7,int(sys.argv[2]))



