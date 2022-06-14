from static.files_handler import readJSON, get_list

cacm_json_path = r"C:\Users\Black\PycharmProjects\flaskProject3\project_files\cacm.json"
cacm_index_path = r"C:\Users\Black\PycharmProjects\flaskProject3\project_files\cacm_index"

cisi_json_path = r"C:\Users\Black\PycharmProjects\flaskProject3\project_files\CISI.json"
cisi_index_path = r"C:\Users\Black\PycharmProjects\flaskProject3\project_files\CISI_index"


def init_files():
    cacm_datasetInfo_json = readJSON(cacm_json_path)
    cacm_index_list = get_list(cacm_index_path)
    cisi_datasetInfo_json = readJSON(cisi_json_path)
    cisi_index_list = get_list(cisi_index_path)

    return cacm_datasetInfo_json, cacm_index_list, cisi_datasetInfo_json, cisi_index_list


from static.indexing_and_matching import cosine_embedding, createVectorEmbadded, addTime2Vector
from static.text_preprocessing import process_text


def match_query_doc(query, index, dataset_list_json):
    processed_query, dateList = process_text(None, query)
    query_vector = createVectorEmbadded(processed_query)
    query_vector = addTime2Vector(query_vector, dateList, False)

    return cosine_embedding(query_vector, index, dataset_list_json)

# TODO loading indexes


# match_query_doc("It is shown that the mapping of a particular area of science, in this"
#                 "are cocitation counts drawn online from Social Scisearch (Social Sciences"
#                 "Citation Index) over the period 1972-1979.  GThe resulting map shows", "", "")

# TODO loading indexes
