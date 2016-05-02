import time

from neextractor import nltkextractor, stanfordextractor, nounextractor

t0 = time.time()
nltk = nltkextractor.extract()
elapsed_time0 = time.time() - t0

t1 = time.time()
stanford = stanfordextractor.extract()
elapsed_time1 = time.time() - t1

t2 = time.time()
noun = nounextractor.extract()
elapsed_time2 = time.time() - t2

print("No. of articles extracted using nltk: " + str(nltk) + " in " + str(elapsed_time0) + " secs.")
print("No. of articles extracted using stanford: " + str(stanford) + " in " + str(elapsed_time1) + " secs.")
print("No. of articles extracted using noun: " + str(noun) + " in " + str(elapsed_time2) + " secs.")