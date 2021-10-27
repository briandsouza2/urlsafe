import urllib.request
import random
import timeit
import time
import random
import string
import json
from multiprocessing import Process

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


lines = open('./data/hostname01_80/urls.txt').read().splitlines()
# read a random line from the test file

def timed_test():
    # send a string to force a look up for keys
    rand_str = get_random_string(2048)
    contents = urllib.request.urlopen(f"http://localhost:5000/urlinfo/2/hostname01_80/{rand_str}").read()
    response = json.loads(contents)
    assert(response['Blocked'] == False)

# Do a sanity check to make sure the server is running correctly
def sanity_test():
    start_time = time.time()
    myline =random.choice(lines)
    query = urllib.parse.quote(myline, safe='')
    contents = urllib.request.urlopen(f"http://localhost:5000/urlinfo/2/hostname01_80/{query}").read()
    response = json.loads(contents)
    assert(response['Blocked'] == True)
    end_time = time.time()
    print("Sanity: took this long to run: {}".format(end_time-start_time))

sanity_test()

def timeit_func():
    duration = timeit.timeit(timed_test, number=1000)
    print("Duration for Timed-Test-Set: ", duration)

def runInParallel(threads):
  proc = []
  for cnt in range(threads):
    p = Process(target=timeit_func)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

runInParallel(5)

