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

# t4 = time.time()
# snltk = subnltkextractor.extract(extract_type="sentence")
# elapsed_time4 = time.time() - t4

# print("No. of articles whose sentences extracted using nltk: " + str(snltk) + " in " + str(elapsed_time4) + " secs.")
# #nltk sent 1023 in 2634.18762803 secs.

from settings import db

db = db.getDB()

nltk = db.word_list.find({}, {"word":1, "_id":0})
stanford = db.stanford_word_list.find({}, {"word":1, "_id":0})
noun = db.noun_word_list.find({}, {"word":1, "_id":0})

nltk_list = []
stan_list = []
noun_list = []

for n in nltk:
    nltk_list += [n['word']]

for s in stanford:
    stan_list += [s['word']]

for n in noun:
    noun_list += [n['word']]
    

nltk_stanford = list(set(nltk_list) & set(stan_list))
nltk_noun = list(set(nltk_list) & set(noun_list))
stanford_noun = list(set(stan_list) & set(noun_list))
nltk_stanford_noun = list(set(nltk_list) & set(stan_list) & set(noun_list))

nltk_size = len(nltk_list)
stan_size = len(stan_list)
noun_size = len(noun_list)

print nltk_list
print nltk_stanford

nl_st_size = len(nltk_stanford) 
nl_no_size = len(nltk_noun) 
st_no_size = len(stanford_noun)
nl_st_no_size = len(nltk_stanford_noun) 

values = [nltk_size, stan_size, noun_size, nl_st_size, nl_no_size, st_no_size, nl_st_no_size]

print values