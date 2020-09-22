import queue

q1 = queue.Queue(10) # the max size is 10      FIFO
#q1 = queue.LifoQueue(10) #    LIFO


q1.put(1)
q1.put(2)
q1.put(3)
q1.put(4)
q1.put(5)
q1.put(6)
q1.put(7)
q1.put(8)
q1.put(9)
q1.put(10)
print(q1.get())
q1.put(11)



print(q1.get())
print(q1.get())
print(q1.get())
print(q1.get())
print(q1.get())
print(q1.get())
