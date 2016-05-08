import time

from translator import sewordlists, sewlmerge

# t0 = time.time()
# nltk = sewordlists.translate("named_entities", "word_list")
# elapsed_time0 = time.time() - t0

# print("No. of articles translated using nltk: " + str(nltk) + " in " + str(elapsed_time0) + " secs.")

# t1 = time.time()
# stanford = sewordlists.translate("stanford_named_entities", "stanford_word_list")
# elapsed_time1 = time.time() - t1

# print("No. of articles translated using stanford: " + str(stanford) + " in " + str(elapsed_time1) + " secs.")

t2 = time.time()
noun = sewordlists.translate("noun_named_entities", "noun_word_list")
elapsed_time2 = time.time() - t2

print("No. of articles translated using noun: " + str(noun) + " in " + str(elapsed_time2) + " secs.")

t3 = time.time()
final = sewlmerge.merge()
elapsed_time3 = time.time() - t3

print("No. of words final: " + str(final) + " in " + str(elapsed_time3) + " secs.")


#nltk - 4388 words in 101 secs | 48 unique to this list only
#stanford - 4209 words in 91 secs | 227 unique to this list only

#noun - 13082 words in 1186 secs (20 mins) | 7870 unique to this list only
#final - 13398 words in 342 secs

#proper noun - 6231 words in ? secs | 1232 unique to this list only
#new final - 6760 words in 52.8 secs
