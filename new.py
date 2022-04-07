from concurrent.futures import process
from unittest import result
from pandas import array
import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from time import sleep
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
import ru_core_news_md

TAGS = ["Акции", "Политика", "Бизнес"]
STOPWORDS = stopwords.words("russian")

def stopwords_processing(sentences:array) -> array:
    
    results = []

    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        filtered = [word for word in words if word not in STOPWORDS]
        filtered = " ".join(filtered)
        results.append(filtered)
    
    return results

def stem_processing(sentences:array) -> array:
    
    results = []
    nlp = ru_core_news_md.load()

    with open("./sentences.txt", "w", encoding = "utf-8") as file:
        for sentence in sentences:
            file.write(sentence)
            file.write("\n")
    
    text = open("./sentences.txt", encoding = "utf-8").read()
    document = nlp(text)

    sentence = []
    for token in document:
        if str(token) == "\n":
            results.append(" ".join(sentence))
            sentence = []
        else:
            sentence.append(str(token.lemma_))

    return results


def get_text(tags:array) -> array:
    #get all the titles of news for given tags
    rbc_news = sum([BeautifulSoup(requests.get(f'https://www.rbc.ru/tags/?tag={tag}').content,
    "lxml").find_all("span", {"class" : "search-item__title"}) for tag in tags], [])
    titles = [i.text for i in rbc_news]

    return titles

def pre_processing(titles:array):

    #all sentences to lowercase
    titles = [i.lower() for i in titles]

    #remove all unneccessary words
    titles = stopwords_processing(titles)

    #lemmatization for entire corpus
    titles = stem_processing(titles)

    return titles

def analysis(titles:array):

    shit = ['"', ',', '-', '<', '>', ':']

    opened_titles = sum([sentence.split() for sentence in titles], [])
    opened_titles = [word for word in opened_titles if
                    word not in shit]

    frequency = FreqDist(opened_titles)
    common = frequency.most_common(20)
    print(common)




def main():
    titles = get_text(tags = TAGS)
    titles = pre_processing(titles = titles)
    analysis(titles = titles)


if __name__ == "__main__":
    main()