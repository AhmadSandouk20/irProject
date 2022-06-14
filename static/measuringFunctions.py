# import pandas as pd
# import wikipedia
# articles=['Data Science','Artificial intelligence','European Central Bank','Swimming']
# wiki_lst=[]
# title=[]
# for article in articles:
#    print("loading content: ",article)
#    # print(wikipedia.page(article).content)
#    wiki_lst.append(wikipedia.page(article).content)
#    title.append(article)
# print("examine content")
# from sklearn.feature_extraction.text import TfidfVectorizer
# vectorizer = TfidfVectorizer(stop_words={'english'})
#
# X = vectorizer.fit_transform(wiki_lst)
# print(X)
# import matplotlib.pyplot as plt
# from sklearn.cluster import KMeans
# Sum_of_squared_distances = []
# K = range(2,4)
# print(K)
# for k in K:
#    km = KMeans(n_clusters=k, max_iter=200, n_init=10)
#    km = km.fit(X)
#    Sum_of_squared_distances.append(km.inertia_)
# # plt.plot(K, Sum_of_squared_distances, 'bx-')
# # plt.xlabel('k')
# # plt.ylabel('Sum_of_squared_distances')
# # plt.title('Elbow Method For Optimal k')
# # plt.show()
# true_k = 6
# model = KMeans(n_clusters=true_k, init='k-means++', max_iter=200, n_init=10)
# model.fit(X)
# labels=model.labels_
# wiki_cl=pd.DataFrame(list(zip(title,labels)),columns=['title','cluster'])
# print(wiki_cl.sort_values(by=['cluster']))
#
#
#
# from wordcloud import WordCloud
# result={'cluster':labels,'wiki':wiki_lst}
# result=pd.DataFrame(result)
# for k in range(0,true_k):
#    s=result[result.cluster==k]
#    text=s['wiki'].str.cat(sep=' ')
#    text=text.lower()
#    text=' '.join([word for word in text.split()])
#    wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
#    print('Cluster: {}'.format(k))
#    print('Titles')
#    titles=wiki_cl[wiki_cl.cluster==k]['title']
#    print(titles.to_string(index=False))
#    plt.figure()
#    plt.imshow(wordcloud, interpolation="bilinear")
#    plt.axis("off")
#    plt.show()
from static.create_dictionary import loadDataSet
from static.files_handler import get_list, readJSON
from static.indexing_and_matching import createVectorEmbadded, cosine_embedding, get_similar_articles_TFIDF
from static.text_preprocessing import process_text


def getQueries(path):
    file = open(path, 'r')
    docTemp = file.read().strip().split(".I ")
    docTemp = filter(None, docTemp)
    result = []
    if path.__contains__("cacm"):
        for v in docTemp:
            if v.__contains__(".A"):
                result.append(str(v[v.index(".W") + 2:v.index(".A")]).strip())
            else:
                result.append(str(v[v.index(".W") + 2:v.index(".N")]).strip())
    elif path.__contains__("CISI"):

        for v in docTemp:
            if v.__contains__(".A"):
                if v.__contains__(".B"):
                    result.append(str(v[v.index(".W") + 2:v.index(".B")]).strip())
                else:
                    result.append(str(v[v.index(".W") + 2:]).strip())
            elif v.__contains__(".B"):
                result.append(str(v[v.index(".W") + 2:v.index(".B")]).strip())
            else:
                result.append(str(v[v.index(".W") + 2:]).strip())
    return result




def loadAnswers(path):
    true_result = {}

    q_id = 0
    file = open(path, "r")
    lines = file.readlines()
    for line in lines:

        if path.__contains__("cacm"):
            q_id = line.strip()[0:line.strip().index(" ")]
            temp = line.strip()[line.strip().index(" "):].strip()
            q_ans = temp.strip()[0:temp.index(" ")].strip()

            if true_result.get(q_id) is None:

                true_result[q_id] = [int(q_ans)]

            else:

                tlist = true_result.get(q_id)
                tlist.append(int(q_ans))
                true_result[q_id] = tlist

        elif path.__contains__("CISI"):
            q_id = line.strip()[0:line.strip().index(" ")]
            # print("q_id", q_id, "end")
            temp = line.strip()[line.strip().index(" "):].strip()
            q_ans=temp[0:temp.index('\t')].strip()

            if true_result.get(q_id) is None:

                true_result[q_id] = [int(q_ans)]

            else:

                tlist = true_result.get(q_id)
                tlist.append(int(q_ans))
                true_result[q_id] = tlist
    return true_result


def saveAnswers(queriesList, index, dataInfo, path):

    allValues_answers = []
    trueValue = loadAnswers(path)
    for i, v in enumerate(queriesList):
        qVec = createVectorEmbadded(v)
        temp = cosine_embedding(qVec, index, dataInfo)
        # temp = get_similar_articles_TFIDF(v, index, dataInfo)
        listTemp = []
        for j in temp:
            listTemp.append(j["id"])

        indexi = i + 1
        allValues_answers.append({"id": indexi, "results": listTemp, "trueResults": trueValue.get(str(indexi))})


    return allValues_answers


# for i,v in enumerate(queryList):
#     if str(v).__contains__(query):
#         if dataSet=="cisi":
#             cisi_queriesResult_answers.append({"id":i+1,"result":[i["id"] for i in results],"true_results":trueResult})
#         elif dataSet=="cacm":
#             cacm_queriesResult_answers.append({"id": i + 1, "result": [i["id"] for i in results], "true_results": trueResult})


# processed, stamped_dates_dictionary = process_text(documents_list, "")
# all_cacm = saveAnswers(getQueries(q_path), processed_document_list, cacm_datasetInfo_json, q_true)


def intersection(lst1, lst2):
    lst3 = []
    for i in range(len(lst1)):
        for j in range(len(lst2)):
            if lst1[i] == lst2[j]:
                lst3.append(lst1[i])

    return lst3

print("inter")
print(intersection([5,8,1,89,5],[1,2,3]))

def reciprocalRank(l1, l2):
    index = 0.0
    for i, v in enumerate(l1):
        newi = i + 1
        for v1 in l2:
            if v == v1:
                index = 1 / newi
                break
    return index


def measurementCalculation(allValues):
    measurement = []
    MAP = 0.0
    MRR = 0.0
    allAVG = []
    allreciprocal = []
    for item in allValues:
        id = item["id"]

        results=[]
        trueResults=[]
        if type(item["results"]) is list:
            results=item["results"]
        else:
            continue

        if type(item["trueResults"]) is list:

            trueResults = item["trueResults"]
        else:
            continue

        print(id)
        precision = intersection(list(results), list(trueResults)).__len__()
        if precision != 0:
            precision = precision / len(list(results))
        recall = intersection(list(results), list(trueResults)).__len__()
        if recall != 0:
            recall = recall / len(list(trueResults))
        precisionAT10 = intersection(list(results)[0:10], list(trueResults)).__len__()
        if precisionAT10 != 0:
            precisionAT10 = precisionAT10 / 10
        avgList = []
        for i in range(len(list(results))):
            newIndex = i + 1
            v = intersection(list(results)[0:newIndex], list(trueResults)).__len__()
            if v != 0:
                v = v / newIndex
            avgList.append(v)
        reciprocal = reciprocalRank(list(results), list(trueResults))
        allreciprocal.append(reciprocal)
        avg = sum(avgList) / len(avgList)
        allAVG.append(avg)
        measurement.append(
            {"id": id, "precision": precision, "recall": recall, "precisionAT10": precisionAT10, "avg": avg,
             "reciprocal": reciprocal})
    if len(allValues)!=0:
        MAP = sum(allAVG) / len(allValues)
    if len(allreciprocal)!=0:
     MRR = sum(allreciprocal) / len(allreciprocal)
    return measurement, MAP, MRR

