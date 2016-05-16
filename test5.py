# import string
# import nltk
# import time

# from settings import db
# from nltk.corpus import wordnet

# db = db.getDB()

# def checkSynonyms(word):
#     # from nltk.corpus import wordnet
#     syns = wordnet.synsets(word)
    
#     results = []
#     for syn in syns:
#         for l in syn.lemmas():
#             # print l.name()
#             res = db.final_word_list.find_one({"word": l.name()})
#             if res:
#                 for url in res['urls']:
#                     if url not in results:
#                         results += [url]
#     return results



# q = "coffee"


# words = nltk.word_tokenize(q)

# results_plain = []

# # for w in words:
# #     w = w.lower()
# #     res = db.final_word_list.find_one({"word": w})
# #     if res:
# #         for url in res['urls']:
# #             if url not in results_plain:
# #                 results_plain += [url]

# # print results_plain
# # print len(results_plain)

# t0 = time.time()
# results = []
# for w in words:
#     w = w.lower()
#     res = db.final_word_list.find_one({"word": w})
#     if res:
#         for url in res['urls']:
#             if url not in results:
#                 results += [url]
#     synonym_results = checkSynonyms(w)
#     for r in synonym_results:
#         if r not in results:
#             results += [r]
# elapsed = time.time() - t0

# print results
# print len(results)
# print elapsed 

# #in func: 3.22, 3.25, 3.53, 2.63, 2.99
# #ou func: 3.82, 3.32, 3.82, 3.31, 3.66
# #ou func: 3.16, 4.48, 4.86, 3.43, 4.29

# # results += [u'http://www.joelonsoftware.com/items/2006/02/10.html', u'http://www.joelonsoftware.com/items/2006/08/01.html', u'http://www.joelonsoftware.com/articles/FB4.5.html']

# #search for duplicate
# for res in results:
#     flag = False
#     w1 = res
#     for r in results:
#         if r == w1:
#             if flag:
#                 print "Duplicate", r
#             else:
#                 flag = True

# java:58, with syns:121
# joel:186, with syns: 186

# print words
# print len(words)

# syns = wordnet.synsets(words[8])

# print syns
# print syns[0].name()
# print syns[0].lemmas()[0].name()
# print syns[0].definition()
# print syns[0].examples()

# synonyms = []
# antonyms = []

# for syn in syns:
#     for l in syn.lemmas():
#         synonyms.append(l.name())
#         if l.antonyms():
#             antonyms.append(l.antonyms()[0].name())

# print synonyms
# print antonyms


# w1 = wordnet.synset("IT.n.01")
# w2 = wordnet.synset("information_technology.n.01")

# print(w1.wup_similarity(w2))

num_of_results = 10
page_size = 3

results_list = [0,1,2,3,4,5,6,7,8,9]

#page 1 = 0 - 29
#page 2 = 30 - 59
#page 3 = 60 - 89

rlist = [results_list[i:i+page_size] for i in range(0, num_of_results, page_size)]

print rlist


