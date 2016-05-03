import time

from translator import sewordlists, sewlmerge

t0 = time.time()
nltk = sewordlists.translate("named_entities", "word_list")
elapsed_time0 = time.time() - t0

t1 = time.time()
stanford = sewordlists.translate("stanford_named_entities", "stanford_word_list")
elapsed_time1 = time.time() - t1

t2 = time.time()
noun = sewordlists.translate("noun_named_entities", "noun_word_list")
elapsed_time2 = time.time() - t2

t3 = time.time()
final = sewlmerge.merge()
elapsed_time3 = time.time() - t3

print("No. of words extracted using nltk: " + str(nltk) + " in " + str(elapsed_time0) + " secs.")
print("No. of words extracted using stanford: " + str(stanford) + " in " + str(elapsed_time1) + " secs.")
print("No. of words extracted using noun: " + str(noun) + " in " + str(elapsed_time2) + " secs.")
print("No. of words final: " + str(final) + " in " + str(elapsed_time3) + " secs.")
