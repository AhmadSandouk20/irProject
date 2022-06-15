from textblob import TextBlob, Word
from static.measuringFunctions import getQueries
from static.files_handler import save_list, get_list

cacm_query_path = r"C:\Users\Black\PycharmProjects\flaskProject3\cacm\query.text"
cisi_query_path = r"C:\Users\Black\PycharmProjects\flaskProject3\CISI\CISI.QRY"


# run offline to prepare the ngrams files
def prepare(dataset_queries_path, ngrams, dataset_name):
    res = []
    dataset_queries_list = getQueries(dataset_queries_path)
    for dataset_query in dataset_queries_list:
        dataset_query = TextBlob(dataset_query)
        ngram = dataset_query.ngrams(n=ngrams)
        res.append(ngram)
    save_list(res, r"C:\Users\Black\PycharmProjects\flaskProject3\project_files\\" + dataset_name + "-ngrams")


def get_res(user_query, dataset):  # get_res("this is a query example",1 or 2  )
    res = [{}]

    dataset_name = ''
    if dataset == 1:
        dataset_name = r"C:\Users\Black\PycharmProjects\flaskProject3\project_files\cacm-ngrams"

    else:
        dataset_name = r"C:\Users\Black\PycharmProjects\flaskProject3\project_files\CISI-ngrams"

    list_of_ngram_list = get_list(dataset_name)  # [[[]],[[]],[[]]]
    for ngram_list in list_of_ngram_list:
        for ngram_item in ngram_list:
            index = match_index(user_query, ngram_item)
            if index != -1:
                res_string = ''

                for p in range(index, ngram_item.__len__()):
                    res_string += ngram_item[p] + " "

                res.append({"result": res_string})
    if not res[0]:
        res.pop(0)
    return res


# takes a query and a list of string (n_grammed string) and return the last index of the last match if exists
def match_index(user_query, dataset_query_ngrammed):  # is_match("this is a query example",["this" ,"is","an","example"])
    user_query = user_query.lower().strip().split()
    index = -1
    ngram_dataset_query = []
    for n in dataset_query_ngrammed:
        ngram_dataset_query.append(n)

    for word_index, word in enumerate(user_query):  # looping in user_entry
        for testId, test in enumerate(ngram_dataset_query):  # looping with index
            corret_t = Word(word).correct()  # correcting the word
            if corret_t.__eq__(test.lower()):
                index = index + 1
                ngram_dataset_query.pop(testId)
                if word_index == user_query.__len__() - 1:
                    return index
                break
            else:
                return -1
    return index  # returninhg the last match index


prepare(cacm_query_path, 4, "cacm")
# prepare(cisi_query_path, 3, "CISI")
res = get_res("articles ", 1)
print(res)
# example = is_match("I should be not", ["i", "should", "be", "going", "by", "now"], )
# print(example)
