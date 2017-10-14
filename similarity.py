import gensim, logging
# import time

# Rehurek, R.
# 2014, February 2
# Word2Vec Tutorial
# https://rare-technologies.com/word2vec-tutorial/
logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', \
    level = logging.INFO)

# McCormick, C.
# 2016, April 12
# Google's trained Word2Vec model in Python
# http://mccormickml.com/2016/04/12/googles-pretrained-word2vec-model-in-python/
# start = time.time()
model = gensim.models.Word2Vec.load_word2vec_format( \
    './GoogleNews-vectors-negative300.bin', binary = True)
# inter = time.time()
# print("TIME: %f" % (inter - start))

def getSim(wordOne, wordTwo):
    return model.n_similarity(wordOne, wordTwo)

def test():
    while True:
        w1 = input("Word 1: ")
        w2 = input("Word 2: ")
        try:
            print(getSim(w1, w2))
        except:
            print("Error. Try something else.")

# test()
