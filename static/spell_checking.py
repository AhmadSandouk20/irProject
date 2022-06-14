
from textblob.en import Spelling

from static.measuringFunctions import getQueries




def get_a_string_from_list(dataset_path):
    query_list = getQueries(dataset_path)
    res = ''
    for stringI in query_list:
        for item in stringI:
            res += item
    return res.lower()


# generate correct spell files
def generate_correct_spelling(query_file_path, dataset):

    result = get_a_string_from_list(query_file_path)
    # words = re.findall("[a-z]+", result)  # Find all the words and place them into a list
    # oneString = " ".join(words)  # Join them into one string

    if dataset == 1:
        correct_spell_path = r"C:\Users\Black\PycharmProjects\flaskProject3\project_files\cacm-correct_spell.txt"
    else:
        correct_spell_path = r"C:\Users\Black\PycharmProjects\flaskProject3\project_files\CISI-correct_spell.txt"
    # The path we want to store our stats file at

    spelling = Spelling(path=correct_spell_path)  # Connect the path to the Spelling object
    spelling.train(result, correct_spell_path)

    return spelling


# generate_correct_spelling(cacm_query_path, 1)
# generate_correct_spelling(cisi_query_path, 2)


# sugeest depending on the generated correct spell files
def word_suggest(query, dataset):
    if dataset == 1:
        correct_spell_path = r"C:\Users\Black\PycharmProjects\flaskProject3\project_files\cacm-correct_spell.txt"
    else:
        correct_spell_path = r"C:\Users\Black\PycharmProjects\flaskProject3\project_files\CISI-correct_spell.txt"

    word_suggestior = Spelling(path=correct_spell_path)

    query = query.replace(',', " ").replace('.', ' ').strip().lower().split(' ')
    suggestion_string = ""

    for item in query:
        suggestions = word_suggestior.suggest(item)
        for i, suggestion in enumerate(suggestions):
            if i == 1:
                break
            else:
                suggestion_string += " " + suggestion[0]

    return suggestion_string





