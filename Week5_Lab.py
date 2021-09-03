import time
import random
import sys

interval = 10
sleep_time = 1

print(sys.argv)

if len(sys.argv) > 1:
	interval = int(sys.argv[1])
	if len(sys.argv) > 2:
		sleep_time = int(sys.argv[2])

start_time = time.time()
current_time = start_time

while current_time < start_time + interval:
	current_time = time.time()
	data = random.random()
	print(current_time, data)
	time.sleep(sleep_time)
# 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
