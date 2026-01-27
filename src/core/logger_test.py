# import sys
from logger import get_logger

logger = get_logger("LoggerTest")

print("mulai")
logger.info("mulai")

print("hitung")
a=1
b=2
c = a+b
print(c)

try:
    d = a+"c"
except Exception as e:
    logger.error(e)
logger.info("Program selesai")
print("mulai selesai")