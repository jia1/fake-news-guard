import nltk
from nltk.corpus import stopwords
sentence = 'Obama speaks to the media in Illinois'.lower().split()
stopwords = nltk.corpus.stopwords.words('english')
filtered_sentence = [w for w in sentence if w not in stopwords]
print(filtered_sentence)
