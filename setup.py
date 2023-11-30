import nltk
import gensim
from nltk.corpus import brown, stopwords
from nltk.stem.porter import PorterStemmer
from gensim.models import LsiModel, TfidfModel
from gensim.corpora import Dictionary
from gensim import similarities
import os

nltk.download('stopwords')

class ModelGeneration:
    def __init__(self, path,num_topics = None) -> None:
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        self.num_topics = 100 if num_topics is None else num_topics
        model, dictionary, index = self.generate_model(path)
        model.save("lsa_model")
        dictionary.save("lsa_dictionary")
        index.save("lsa_index")

    def preprocess(self, text):
        self.stemmer = PorterStemmer()
        stop_words = set(stopwords.words('english'))
        words = nltk.word_tokenize(text.lower())
        return [self.stemmer.stem(word) for word in words if word not in stop_words and word.isalpha()]

  
    def generate_model(self, corpus):
        processed_corpus = [self.preprocess(text) for text in corpus]
        dictionary = Dictionary(processed_corpus)
        bow_corpus = [dictionary.doc2bow(text) for text in processed_corpus]
        tfidf = TfidfModel(bow_corpus)
        corpus_tfidf = tfidf[bow_corpus]
        lsa_model = LsiModel(corpus_tfidf, id2word=dictionary, num_topics=self.num_topics)
        index = similarities.MatrixSimilarity(lsa_model[corpus_tfidf])
        return lsa_model, dictionary, index

def main():
    nltk.download('brown')
    brown_corpus = brown.sents()
    model_gen = ModelGeneration(brown_corpus)
    print("Model training and saving complete.")

if __name__ == "__main__":
    main()