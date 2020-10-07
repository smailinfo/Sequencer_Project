import threading
import time

for _ in range(20):
    time.sleep(3)
    print("\n", threading.currentThread().getName())
    print("current thread", threading.current_thread())
    print("active threads ", threading.active_count())
