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

def test_array():
    start_time = time.time()
    myline =random.choice(lines)
    contents = urllib.request.urlopen(f"http://localhost:5000/urlinfo/1/hostname1_443/{myline}").read()
    print(contents)
    end_time = time.time()
    print("Array: took this long to run: {}".format(end_time-start_time))
    
def test_set():
    start_time = time.time()
    #myline =random.choice(lines)
    contents = urllib.request.urlopen(f"http://localhost:5000/urlinfo/2/hostname1_443/{rand_str}").read()
    end_time = time.time()
    print("Set: took this long to run: {}".format(end_time-start_time))

# warm up the cache
contents = urllib.request.urlopen(f"http://localhost:5000/urlinfo/1/hostname:port/{rand_str}").read()

duration = timeit.timeit(test_set, number=10)
print("Duration for Set: ", duration)

duration = timeit.timeit(test_array, number=10)
print("Duration for Array: ", duration)
