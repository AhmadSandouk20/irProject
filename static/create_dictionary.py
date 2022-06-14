def loadDataSet(path):
    documents = []
    documents_info = []
    index = 0
    file = open(path, 'r')
    docTemp = file.read().strip().split(".I ")
    docTemp = filter(None, docTemp)

    # print(docTemp)
    for i in docTemp:
        title = ""
        if str(path.upper()).__contains__("CISI".upper()):
            title = i[i.index(".T") + 2:i.index(".A")]

        elif str(path.upper()).__contains__("CACM".upper()):
            if str(i).__contains__(".W "):
                title = i[i.index(".T") + 2:i.index(".W")]
            else:
                title = i[i.index(".T") + 2:i.index(".B")]

        index += 1
        i = i[i.index(".T") + 2:i.index(".X")].strip()
        i = i.replace("\n", "")
        i = i.replace(".T", "")
        i = i.replace(".W", "")
        i = i.replace(".B", "")
        i = i.replace(".N", "")
        i = i.replace(".A", "")

        documents_info.append({"id": index, "title": title})
        documents.append(i)

    return documents_info, documents
