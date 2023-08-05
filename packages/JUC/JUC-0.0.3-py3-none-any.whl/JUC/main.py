#chr
#ord
import base64, time
from .calculateKey import *
from .exceptions import *

class Juc:
    def __init__(self, key):
        if key == '':
            raise InvalidKey('Cannot use an empty key')
        self.key = key
        self.keyCode = calculate(key)

    def crypt(self, text : bytes) -> str:
        now = int(time.time() * 1000000)
        return (''.join(
            str(hex(ord(code) * int(now / self.keyCode))) for code \
                in base64.b64encode(text).decode()
        ) + f'.{now}')

    def decrypt(self, text, decode : bool = False) -> str:
        string, now = getCString(text)
        result = base64.b64decode(''.join(
            chr(int(hexValue, 16) // int(now / self.keyCode)) for hexValue \
                in string.split('0x')[1:]
        ))
        return result.decode() if decode else result