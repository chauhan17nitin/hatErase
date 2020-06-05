from threading import Thread
from time import sleep
var=[]

i=0
def some_func(var):
    print(var)
    
th = Thread(target=some_func,args=(var,))
th.start()

print(th.isAlive())

th.join()
print(th.isAlive())

def loop(q):
    while True:
        i = q.get()
        print(i)
    
from multiprocessing import Process, Queue

i = 1
q = Queue()
q.put(i)
p = Process(target=loop, args=(q, ))
p.start()

while True:
    i+=1
    q.put(i)
    sleep(1)
    

import time

def g():
    global a,b
    a=5
    b=9
    print(a,b)
print(a,b)