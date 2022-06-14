import json
import pickle


def creatJSON(name, file):
    with open(name, "w") as outfile:
        json.dump(file, outfile)


def readJSON(name):
    f = open(name)
    data = json.load(f)
    return data


def extractListsFromJSON(file):
    documents = []
    for i in file:
        documents.append(i['text'])
    return documents


def save_list(data_list, save_file_path):
    with open(save_file_path, 'wb') as file:
        pickle.dump(data_list, file)


def get_list(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)
