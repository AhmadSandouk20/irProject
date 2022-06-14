from static.files_handler import get_list, readJSON, creatJSON
from static.measuringFunctions import saveAnswers, getQueries, measurementCalculation




q_path_cacm = r"C:\Users\Black\PycharmProjects\flaskProject3\cacm\query.text"
q_true_cacm = r"C:\Users\Black\PycharmProjects\flaskProject3\cacm\qrels.text"
cacm_index_list = get_list(r"C:\Users\Black\PycharmProjects\flaskProject3\project_files\cacm_index")
cacm_datasetInfo_json = readJSON(r"C:\Users\Black\PycharmProjects\flaskProject3\project_files\cacm.json")


q_path_CISI = r"C:\Users\Black\PycharmProjects\flaskProject3\CISI\CISI.QRY"
q_true_CISI = r"C:\Users\Black\PycharmProjects\flaskProject3\CISI\CISI.REL"
CISI_index_list = get_list(r"C:\Users\Black\PycharmProjects\flaskProject3\project_files\CISI_index")
CISI_datasetInfo_json = readJSON(r"C:\Users\Black\PycharmProjects\flaskProject3\project_files\CISI.json")

# all_CISI = saveAnswers(getQueries(q_path_CISI), CISI_index_list, CISI_datasetInfo_json, q_true_CISI)
#
# measure, map1, mrr = measurementCalculation(all_CISI)
#

all_cacm = saveAnswers(getQueries(q_path_cacm), cacm_index_list, cacm_datasetInfo_json, q_true_cacm)

measure, map1, mrr = measurementCalculation(all_cacm)
print(measure)
print(map1)

print(mrr)
# creatJSON(r"C:\Users\Black\PycharmProjects\flaskProject3\Measure"+r"\new_model_CISI.json",measure)
#
# creatJSON(r"C:\Users\Black\PycharmProjects\flaskProject3\Measure"+r"\new_model_map_mrr_CISI.json",{"map":map1,"mrr":mrr})
#
#
# creatJSON(r"C:\Users\Black\PycharmProjects\flaskProject3\Measure"+r"\new_model_cacm.json",measure)
#
# creatJSON(r"C:\Users\Black\PycharmProjects\flaskProject3\Measure"+r"\new_model_map_mrr_cacm.json",{"map":map1,"mrr":mrr})
