import time

from translator import sewordlists, sewlmerge, subsewordlists, subsewlmerge

# t0 = time.time()
# nltk = sewordlists.translate("named_entities", "word_list")
# elapsed_time0 = time.time() - t0

# print("No. of articles translated using nltk: " + str(nltk) + " in " + str(elapsed_time0) + " secs.")

# t1 = time.time()
# stanford = sewordlists.translate("stanford_named_entities", "stanford_word_list")
# elapsed_time1 = time.time() - t1

# print("No. of articles translated using stanford: " + str(stanford) + " in " + str(elapsed_time1) + " secs.")

# t2 = time.time()
# noun = sewordlists.translate("noun_named_entities", "noun_word_list")
# elapsed_time2 = time.time() - t2

# print("No. of articles translated using noun: " + str(noun) + " in " + str(elapsed_time2) + " secs.")

# t3 = time.time()
# final = sewlmerge.merge()
# elapsed_time3 = time.time() - t3

# print("No. of words final: " + str(final) + " in " + str(elapsed_time3) + " secs.")


#nltk - 4388 words in 101 secs | 48 unique to this list only
#stanford - 4209 words in 91 secs | 227 unique to this list only

#noun - 13082 words in 1186 secs (20 mins) | 7870 unique to this list only
#final - 13398 words in 342 secs

#proper noun - 6231 words in ? secs | 1232 unique to this list only
#new final - 6760 words in 52.8 secs

# t0 = time.time()
# events = sewordlists.translate("event_entities", "event_word_list")
# elapsed_time0 = time.time() - t0

# print("No. of articles event translations: " + str(events) + " in " + str(elapsed_time0) + " secs.")

# t0 = time.time()
# pnltk = subsewordlists.translate("paragraph_named_entities", "paragraph_word_list", extract_type="paragraph")
# elapsed_time0 = time.time() - t0

# print("No. of Para nltk translations: " + str(pnltk) + " in " + str(elapsed_time0) + " secs.")
# #975 in 228 secs

# t0 = time.time()
# snltk = subsewordlists.translate("sentence_named_entities", "sentence_word_list", extract_type="sentence")
# elapsed_time0 = time.time() - t0

# print("No. of Sent nltk translations: " + str(snltk) + " in " + str(elapsed_time0) + " secs.")
# #975 in 253

# t0 = time.time()
# pnoun = subsewordlists.translate("paragraph_noun_named_entities", "paragraph_noun_word_list", extract_type="paragraph")
# elapsed_time0 = time.time() - t0

# print("No. of Para noun translations: " + str(pnoun) + " in " + str(elapsed_time0) + " secs.")
# #No. of Para noun translations: 6858 in 767.031598091 secs. 

# t0 = time.time()
# snoun = subsewordlists.translate("sentence_noun_named_entities", "sentence_noun_word_list", extract_type="sentence")
# elapsed_time0 = time.time() - t0

# print("No. of Sent noun translations: " + str(snoun) + " in " + str(elapsed_time0) + " secs.")
# #Sent noun translations: 13283 in 898.594938993 secs.     

# t0 = time.time()
# pnltk = subsewordlists.translate("paragraph_named_entities", "paragraph_word_list", extract_type="paragraph")
# elapsed_time0 = time.time() - t0

# print("No. of para nltk translations: " + str(pnltk) + " in " + str(elapsed_time0) + " secs.")
# # No. of para nltk translations: 5824 in 364.793810129 secs.  

# t0 = time.time()
# snltk = subsewordlists.translate("sentence_named_entities", "sentence_word_list", extract_type="sentence")
# elapsed_time0 = time.time() - t0

# print("No. of sent nltk translations: " + str(snltk) + " in " + str(elapsed_time0) + " secs.")
# #   No. of sent nltk translations: 10909 in 581.587208986 secs. 

# t0 = time.time()
# pstan = subsewordlists.translate("paragraph_stanford_named_entities", "paragraph_stanford_word_list", extract_type="paragraph")
# elapsed_time0 = time.time() - t0

# print("No. of para stan translations: " + str(pstan) + " in " + str(elapsed_time0) + " secs.")
# #   No. of para stan translations:  5128 in 269.809001923 secs.                                                                                              
                                                            
                                                            
t3 = time.time()
final = subsewlmerge.merge(scope="paragraph")
elapsed_time3 = time.time() - t3

print("No. of para words final: " + str(final) + " in " + str(elapsed_time3) + " secs.")
#No. of para words final: 6727 in 364.004263878 secs.