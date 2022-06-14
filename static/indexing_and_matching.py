from scipy import spatial
import re
import string
from numpy.linalg import norm
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

import spacy


def get_similar_articles_TFIDF(q, documents, docInfo):
    vectorizer = TfidfVectorizer()
    result = []

    X = vectorizer.fit_transform(documents)

    # print(vectorizer.transform(documents_clean))

    X = X.T.toarray()

    df = pd.DataFrame(X, index=vectorizer.get_feature_names_out())
    print("query:", q)
    print("Berikut artikel dengan nilai cosine similarity tertinggi: ")

    q = [q]
    q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0], )
    # print(q_vec)
    sim = {}
    from scipy import spatial

    for i in range(df.columns.__len__()):
        sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)
    print("hello")
    # Sort the values
    sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
    print("sim_sorted", sim_sorted.__len__())
    print("sim_sorted", sim_sorted[0])
    for k, v in sim_sorted:
        if v != 0.0 and v > 0.0:
            result.append({"id": docInfo[k]['id'], "title": docInfo[k]["title"]})
            print("Nilai Similaritas:", v)
            print({"id": docInfo[k]['id'], "title": docInfo[k]["title"]})
            print()

    return result


def createVectorEmbadded(data):
    print("create vectors")
    if isinstance(data, list):

        nlp = spacy.load("en_core_web_sm")
        vectors = [nlp(doc).vector for doc in data]
        print("in list")
        return vectors
    elif isinstance(data, str):
        nlp = spacy.load("en_core_web_sm")
        q = nlp(data).vector
        print("in query")
        return q


test = [
    "mohammad",
    "kaddoumi",
    "mohammad kaddoumi",
    "mohammad kaddo"
]

inf = [
    {"id": 1, "title": "t1"},
    {"id": 2, "title": "t2"},
    {"id": 3, "title": "t3"},
    {"id": 4, "title": "t4"},
]
q = "mohammad kaddoumi"
import spacy

tp = []


# todo remove 3th argument and make the jsonlist global
def cosine_embedding(queryVector, vectorsList, docInfo):
    result = []
    sim = {}
    for i in range(len(vectorsList)):
        if len(queryVector) == len(vectorsList[i]):
            sim[i] = 1 - spatial.distance.cosine(vectorsList[i], queryVector)
        else:
            v1, v2 = equalize(vectorsList[i], queryVector)
            sim[i] = 1 - spatial.distance.cosine(v1, v2)
            # sim[i] = 1 - spatial.distance.cosine(norm(vectorsList[i]),norm( queryVector))
    sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
    print("test index")
    print("***********************")
    print(sim_sorted.__len__())

    for k, v in sim_sorted:

        if v > 0:
            result.append({"id": docInfo[k]['id'], "title": docInfo[k]["title"]})

            # print("Similaritas: ", v)
            # print(test[k])
    print(result.__len__())
    return result


import numpy


def addTime2Vector(vectros, timeStampList, isList):
    print("in add time to vec   ", len(vectros))
    if len(timeStampList) == 0:
        return vectros
    if isList == False:
        a = numpy.array(vectros)
        newArray = numpy.append(a, timeStampList[0]["stamped_dates"])
        return newArray
    else:
        newVectors = []
        for i, v in enumerate(vectros):
            for j, t in enumerate(timeStampList):
                if t["id"] == i:
                    a = numpy.array(vectros[i])
                    newArray = numpy.append(a, t["stamped_dates"])
                    newVectors.append(newArray)

    return newVectors


def equalize(v1, v2):
    if len(v1) > len(v2):
        while len(v1) != len(v2):
            v2 = numpy.append(v2, 0.0)
    else:
        while len(v1) != len(v2):
            v1 = numpy.append(v1, 0.0)

    return v1, v2
