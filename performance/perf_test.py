import urllib.request
import random
import timeit
import time
import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


rand_str = get_random_string(2048)

lines = open('../data/hostname1_443/urls.txt').read().splitlines()
# read a random line from the test file

def test_set():
    start_time = time.time()
    myline =random.choice(lines)
    #import pdb; pdb.set_trace()
    query = urllib.parse.quote(myline, safe='')
    contents = urllib.request.urlopen(f"http://localhost:5000/urlinfo/2/hostname1_443/{query}").read()
    end_time = time.time()
    print("Set: took this long to run: {}".format(end_time-start_time))

duration = timeit.timeit(test_set, number=100)
print("Duration for Set: ", duration)

