from time import sleep
from random import randint


def square(x, dic={}):
    sleep(randint(0, 50))
    return {'square': x ** 2,
            'bytes': b'bytes \x00\x01\x02\x03 return 123'}
