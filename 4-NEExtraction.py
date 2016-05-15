import time

from neextractor import nltkextractor, stanfordextractor, nounextractor, subnltkextractor, substanfordextractor, subnounextractor

# t0 = time.time()
# nltk = nltkextractor.extract()
# elapsed_time0 = time.time() - t0

# t1 = time.time()
# stanford = stanfordextractor.extract()
# elapsed_time1 = time.time() - t1

# t2 = time.time()
# noun = nounextractor.extract()
# elapsed_time2 = time.time() - t2

# print("No. of articles extracted using nltk: " + str(nltk) + " in " + str(elapsed_time0) + " secs.")
# print("No. of articles extracted using stanford: " + str(stanford) + " in " + str(elapsed_time1) + " secs.")
# print("No. of articles extracted using noun: " + str(noun) + " in " + str(elapsed_time2) + " secs.")

#nltk 673.776299 secs - (11 mins)
#stanford 10564.88358 secs - (176 mins,2.9 hours)
#noun 398.54835 secs - (6.63 mins) NN NNS NNP NNPS
#proper nouns 98.47579 - (1.63 mins) NNP NNPS

# t3 = time.time()
# pnltk = subnltkextractor.extract(extract_type="paragraph")
# elapsed_time3 = time.time() - t3

# print("No. of articles whose paragrpahs extracted using nltk: " + str(pnltk) + " in " + str(elapsed_time3) + " secs.")
#nltk para 489.9895 secs

# t4 = time.time()
# snltk = subnltkextractor.extract(extract_type="sentence")
# elapsed_time4 = time.time() - t4

# print("No. of articles whose sentences extracted using nltk: " + str(snltk) + " in " + str(elapsed_time4) + " secs.")
# #nltk sent 576.45199585

# t5 = time.time()
# pstanford = substanfordextractor.extract(extract_type="paragraph")
# elapsed_time5 = time.time() - t5

# print("No. of articles whose paragraphs extracted using stanford: " + str(pstanford) + " in " + str(elapsed_time5) + " secs.")
# #stanford para No. of articles whose paragraphs extracted using stanford: 1023 in 95273.359895 secs. (1587 mins, 26.46 hours)

t6 = time.time()
sstanford = substanfordextractor.extract(extract_type="sentence")
elapsed_time6 = time.time() - t6

print("No. of articles whose sentences extracted using stanford: " + str(sstanford) + " in " + str(elapsed_time6) + " secs.")
#stanford sent 

# t7 = time.time()
# pnoun = subnounextractor.extract(extract_type="paragraph")
# elapsed_time7 = time.time() - t7

# print("No. of articles whose paragraphs extracted using noun: " + str(pnoun) + " in " + str(elapsed_time7) + " secs.")
# #noun para 208.247689009

# t8 = time.time()
# snoun = subnounextractor.extract(extract_type="sentence")
# elapsed_time8 = time.time() - t8

# print("No. of articles whose sentences extracted using noun: " + str(snoun) + " in " + str(elapsed_time8) + " secs.")
# #noun- sent 799.37001