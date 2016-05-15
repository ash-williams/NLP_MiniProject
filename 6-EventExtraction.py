import time

from eventextractor import extractor, subextractor

articlecnt = 0

# t0 = time.time()
# articlecnt = extractor.extract()
# elapsed_time0 = time.time() - t0

# print("No. of articles read: " + str(articlecnt) + " in " + str(elapsed_time0) + " secs.")


# 705 articles with events - 10.707215 secs to complete

# t1 = time.time()
# paragraphcnt = subextractor.extract(scope="paragraph")
# elapsed_time1 = time.time() - t1

# print("No. of paragraphs read: " + str(paragraphcnt) + " in " + str(elapsed_time1) + " secs.")
# #348.026067972 secs.

t2 = time.time()
sentencecnt = subextractor.extract(scope="sentence")
elapsed_time2 = time.time() - t2

print("No. of sentences read: " + str(sentencecnt) + " in " + str(elapsed_time2) + " secs.")
#303.801126003 secs