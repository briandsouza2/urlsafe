from random import choice
from string import ascii_uppercase

from itertools import repeat

import random
import string
import sys

def f(n: int) -> str:
        return bytes(random.choices(string.ascii_uppercase.encode('ascii'),k=n)).decode('ascii')


ctr = 0
buffer = []
for count in repeat(None, 100000):
    buffer.append(f(2048)+ "\n")
    ctr = ctr + 1
    if not ctr % 1000:
        print(ctr)

sizebuff = sys.getsizeof(buffer)
print("Size of buffer:", sizebuff)
print("Sorting")
buffer.sort()
print("Done Sorting")
with open('/tmp/teststrings.txt','w') as outfile:
        outfile.writelines(buffer)
