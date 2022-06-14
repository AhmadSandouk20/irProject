import json

from static.create_dictionary import loadDataSet
from static.indexing_and_matching import createVectorEmbadded, addTime2Vector
from static.files_handler import  creatJSON, save_list
from static.text_preprocessing import process_text
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize


cisi_path = r"C:\Users\Black\PycharmProjects\flaskProject3\CISI\CISI.ALL"
cacm_path = r"C:\Users\Black\PycharmProjects\flaskProject3\cacm\cacm.mm"
test_pro=[]

def offline_work(path):
    dataset_name = path[path.rfind('\\'):path.rfind('.')]

    print("dhello ", dataset_name)
    documents_info, documents = loadDataSet(path)
    creatJSON(r"C:\Users\Black\PycharmProjects\flaskProject3\project_files\\" + dataset_name + ".json", documents_info)
    # documents_list = extractListsFromJSON(documents_json)
    documents_list = documents

    # processed_document_list, stamped_dates_dictionary = process_text(documents_list, "")
    processed_document_list, stamped_dates_dictionary = process_text(documents_list, "")
    print(processed_document_list)
    # test_pro = processed_document_list
    # documents_list_vectors = createVectorEmbadded(processed_document_list)
    # try new word embedding model
    tokenized_sent = []
    for s in processed_document_list:
        tokenized_sent.append(word_tokenize(s.lower()))
    tagged_data = [TaggedDocument(d, [i]) for i, d in enumerate(tokenized_sent)]

    model = Doc2Vec(tagged_data, vector_size=20, window=2, min_count=1, epochs=100)
    newVetors = addTime2Vector(model.dv.vectors, stamped_dates_dictionary, True)

    # newVetors=addTime2Vector(documents_list_vectors,stamped_dates_dictionary,True)
    print("new vec from offline ", newVetors[0])
    save_list(newVetors,
              "../project_files/" + dataset_name + "_index")
    return newVetors

offline_work(cisi_path)
offline_work(cacm_path)
