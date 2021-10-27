from random import choice
from string import ascii_uppercase

from itertools import repeat

import random
import string
import sys
import uuid

def f(n: int) -> str:
        return bytes(random.choices(string.ascii_lowercase.encode('ascii'),k=n)).decode('ascii')


ctr = 0
buffer = []
for count in repeat(None, 100000):
        # create a random path
        path =  uuid.uuid4().hex + "/"
        query_string = ""
        for param_count in range(1,100):
                query_string = f"{query_string}&param{param_count}={f(10)}"
        uri = path + query_string
        buffer.append(uri+"\n")
        ctr = ctr + 1
        if not ctr % 1000:
                print(ctr)

sizebuff = sys.getsizeof(buffer)
print("Size of buffer:", sizebuff)
print("Sorting")
buffer.sort()
print("Done Sorting")
with open('/tmp/urls.txt','w') as outfile:
        outfile.writelines(buffer)
