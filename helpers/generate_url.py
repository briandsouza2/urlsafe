from random import choice
from string import ascii_uppercase

from itertools import repeat

import random
import string
import sys
import uuid
import os

NUM_HOSTS = 4
NUM_URLS = 10000
DATA_DIR = './data'

def f(n: int) -> str:
        return bytes(random.choices(string.ascii_lowercase.encode('ascii'),k=n)).decode('ascii')


for host_cnt in range(1, NUM_HOSTS+1):
        ctr = 0
        buffer = []
        for count in repeat(None, NUM_URLS):
                # create a random path
                path =  uuid.uuid4().hex + "?"
                query_string = "param000=val000"
                for param_count in range(1,100):
                        query_string = f"{query_string}&param{param_count:03}={f(10)}"
                uri = path + query_string
                buffer.append(uri+"\n")
                ctr = ctr + 1
                if not ctr % 10000:
                        # give an output so the user knows something is happening
                        print("URLs generated: ", ctr)
        sizebuff = sys.getsizeof(buffer)
        buffer.sort()
        
        datadir = os.path.join(DATA_DIR, f"hostname{host_cnt:02}_80")
        filename = os.path.join(datadir,"urls.txt")
        if not os.path.exists(datadir):
                os.makedirs(datadir)
        
        print("Writing file: ", filename)
        with open(filename,'w') as outfile:
                outfile.writelines(buffer)
