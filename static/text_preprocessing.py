from nltk.corpus import wordnet
import re

import nltk
import string
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords

from static.date_catch import extract_and_stamp_date

ps = PorterStemmer()
stop_words = set(stopwords.words('english'))


def process_text(document_list=None, query=""):
    if document_list is not None:
        deal_list = document_list

    else:
        query = [query]
        deal_list = query

    result = []
    date_list = []

    for i, text in enumerate(deal_list):

        extracted_date_list, text_without_date = extract_and_stamp_date(text)

        if extracted_date_list:
            date_list.append({"id": i, "stamped_dates": extracted_date_list})

        processed_text = clean_text(text_without_date)

        processed_text = [ps.stem(word, to_lowercase="true")
                          for word in processed_text]
        processed_text = lemmtaize_with_tagging(processed_text)

        if processed_text:
            result.append(processed_text)

    if query:
        query_string = ""

        for a in result:
            for b in a:
                query_string += b + " "

        return query_string, date_list

    else:
        final = []

        for index in range(len(result)):
            temp = ""
            for u in result[index]:
                # print(u)
                temp += " " + u
            final.append(temp.strip())
    #
    return final, date_list


def pos_tagger(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def lemmtaize_with_tagging(text_array):
    lemmatizer = WordNetLemmatizer()
    tag_chars = []
    for word_tag in nltk.pos_tag(text_array):
        tag_chars.append(pos_tagger(word_tag[1]))

    result = [
        lemmatizer.lemmatize(word, tag_chars[index])
        for index, word in enumerate(text_array)
    ]
    return result


def remove_double_spaces(text_array):
    no_double_spaces = []
    for line in text_array:
        line = re.sub(r'\s{2,}', ' ', line)
        no_double_spaces.append(line)
    return no_double_spaces


def clean_text(text):
    processed_text = word_tokenize(text)

    processed_text = [w for w in processed_text if w not in stop_words]
    processed_text = [
        word for word in processed_text if word not in string.punctuation]
    # Remove the doubled space
    processed_text = remove_double_spaces(processed_text)
    return processed_text
















