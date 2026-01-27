# import sys
from logger import get_logger

logger = get_logger("LoggerTest")

print("mulai")

print("hitung")
a=1
b=2
c = a+b
print(c)

try:
    d = a+"c"
except:
    logger.info("error d")
logger.info("mulai")
print("mulai selesai")