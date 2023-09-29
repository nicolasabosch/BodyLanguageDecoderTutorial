import time

import time

startTime = time.time()
# do some work here

print(time.time())
while True:
    #print(int(time.time()*1000.0))
    nowTime = time.time()
    timeElapsed = nowTime - startTime