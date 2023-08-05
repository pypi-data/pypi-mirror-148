import time
from threading import Thread

COUNT = 50000000


def count_down(number):
    while number > 0:
        number -= 1


t1 = Thread(target=count_down, args=(COUNT//2,))
t2 = Thread(target=count_down, args=(COUNT//2,))

start = time.time()
t1.start()
t2.start()
t1.join()
t2.join()
end = time.time()

print(f'Time taking with multiple threads: {end - start}')