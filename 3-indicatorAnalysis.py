import time

from analyser import indicatorstats

t0 = time.time()
analysed = indicatorstats.analyse()
elapsed_time = time.time() - t0

print("No. of articles analysed: " + str(analysed) + " in " + str(elapsed_time) + " secs.")