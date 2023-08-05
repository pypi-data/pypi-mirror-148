# Single thread example

import time
COUNT = 50000000


def count_down(n):
    while n > 0:
        n -= 1


start = time.time()
count_down(COUNT)
end = time.time()

print(f'Time taken in seconds {end - start}')


