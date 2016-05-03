import time

from neextractor import nltkextractor, stanfordextractor, nounextractor

t0 = time.time()
# nltk = nltkextractor.extract()
elapsed_time0 = time.time() - t0

t1 = time.time()
# stanford = stanfordextractor.extract()
elapsed_time1 = time.time() - t1

t2 = time.time()
noun = nounextractor.extract()
elapsed_time2 = time.time() - t2

# print("No. of articles extracted using nltk: " + str(nltk) + " in " + str(elapsed_time0) + " secs.")
# print("No. of articles extracted using stanford: " + str(stanford) + " in " + str(elapsed_time1) + " secs.")
print("No. of articles extracted using noun: " + str(noun) + " in " + str(elapsed_time2) + " secs.")

#nltk 18005.4361069 secs - (300 mins, 5 hours)
#stanford 10564.88358 secs - (176 mins,2.9 hours)
#noun 398.54835 secs - (6.63 mins)