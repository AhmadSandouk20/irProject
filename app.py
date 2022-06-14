from flask import Flask, render_template, request, jsonify

from static.online import match_query_doc
from static.spell_checking import word_suggest
from static.online import init_files

app = Flask(__name__)

cacm_dataset_json, cacm_index_list, cisi_dataset_json, cisi_index_list = init_files()


def get_id_list_from_query(query, dataset):
    if query:
        query_as_json = jsonify({"query": query.strip(), }, )

        if dataset == 1:
            index = cacm_index_list
            dataset_list = cacm_dataset_json
        else:
            index = cisi_index_list
            dataset_list = cisi_dataset_json

        doc_id_List = match_query_doc(query_as_json.get_json()["query"], index, dataset_list)
        # doc_id_List_as_json = jsonify(doc_id_List)
        correct_query = word_suggest(query, dataset)
        return render_template('search_ui.html',
                               query=query,
                               results=doc_id_List,
                               corret_spell=correct_query.strip())
    else:
        return render_template('search_ui.html', query="")


@app.route('/', methods=["GET"])
def cacm_search():
    query = request.args.get("query")
    return get_id_list_from_query(query, 1)


@app.route('/cisi', methods=["GET"])
def get_cisi_query_res():
    query = request.args.get("query")
    return get_id_list_from_query(query, 2)


# @app.route('/suggestions', methods=["GET"])
# def get_suggestions():
#     query = request.args.get("query")
#     # return get_id_list_from_query(query, 2)
#     return {"options": ["a1", "a2", "a3"]}


if __name__ == '__main__':
    app.run(debug=True)
