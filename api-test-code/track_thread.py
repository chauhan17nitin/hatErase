from threading import Thread
from streaming import Start_stream
from time import sleep

th = Thread(target=Start_stream)
th.start()

while(1):
    sleep(5)
    print('d')