import time

# from neextractor import nltkextractor, stanfordextractor, nounextractor, subnltkextractor, substanfordextractor, subnounextractor

# t7 = time.time()
# pnoun = subnounextractor.extract(extract_type="paragraph")
# elapsed_time7 = time.time() - t7

# print("No. of articles whose paragraphs extracted using noun: " + str(pnoun) + " in " + str(elapsed_time7) + " secs.")
# # #noun para 738.014050961 (12.3 mins)

# import nltk
# text = "The short answer is that the open source tools are kind of raw. They're dune buggies. Powerful, yes, and sufficient for a college project, but as it turns out, people buy Cadillacs, not dune buggies, to drive around in, because they like to have windshield wipers, 14-way power adjustable seats, and a way to start the engine from twenty feet away. Just in case you live in a Hollywood movie and the ignition has been hooked up to a bomb."

# words = nltk.word_tokenize(text)
# tagged = nltk.pos_tag(words)

# print tagged

# for item in tagged:
#     if item[1] in ["NNP","NNPS"]:
#         word = item[0]
        
#         print word


from neextractor import nltkextractor, stanfordextractor, nounextractor, subnltkextractor, substanfordextractor, subnounextractor

# t3 = time.time()
# pnltk = subnltkextractor.extract(extract_type="paragraph")
# elapsed_time3 = time.time() - t3

# print("No. of articles whose paragrpahs extracted using nltk: " + str(pnltk) + " in " + str(elapsed_time3) + " secs.")
# # #nltk para  2928.23112106 

t4 = time.time()
snltk = subnltkextractor.extract(extract_type="sentence")
elapsed_time4 = time.time() - t4

print("No. of articles whose sentences extracted using nltk: " + str(snltk) + " in " + str(elapsed_time4) + " secs.")
#nltk sent 1023 in 2634.18762803 secs.