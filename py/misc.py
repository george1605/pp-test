# MULTIPROCESSING

from multiprocessing import Process
import time

def worker(name):
    for i in range(3):
        print(f"{name} -> {i}")
        time.sleep(1)

if __name__ == "__main__":
    p1 = Process(target=worker, args=("Process-1",))
    p2 = Process(target=worker, args=("Process-2",))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Done")

# THREADING 

import threading
import time

def worker(name):
    for i in range(3):
        print(f"{name} -> {i}")
        time.sleep(1)

t1 = threading.Thread(target=worker, args=("Thread-1",))
t2 = threading.Thread(target=worker, args=("Thread-2",))

t1.start()
t2.start()

t1.join()
t2.join()

# THREADING (WITH INHERITANCE FROM threading.Thread)

import threading
import time

class Worker(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        for i in range(3):
            print(f"{self.name} -> {i}")
            time.sleep(1)

t1 = Worker("Thread-A")
t2 = Worker("Thread-B")

t1.start()
t2.start()

t1.join()
t2.join()

print("Done")

print("Done")

