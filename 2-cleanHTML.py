import time

from cleaner import htmlcleaner

t0 = time.time()
cleaned = htmlcleaner.clean()
elapsed_time = time.time() - t0

print("No. of articles cleaned: " + str(cleaned) + " in " + str(elapsed_time) + " secs.")