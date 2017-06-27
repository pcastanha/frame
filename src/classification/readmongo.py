# encoding: utf-8
import sys
import re
from bson.objectid import ObjectId
from classification.utils import *


from pymongo import MongoClient
client = MongoClient('172.23.227.73')
db = client.test_database
paragraphs = db.paragraphs


elements = { "FATO": "^DOS FATOS", "PEDIDO": "^DOS PEDIDO", "OUTROS": "residente e domiciliad", "ARGUMENTOS": "^DO DIREITO"}


for key in elements.keys():
    el_value = elements[key]
    path = "train/"
    test_path = "test/"
    ensure_dir(path)
    ensure_dir(test_path)

    docs = []
    print("Getting All Documents from " + el_value + " Criteria")
    allDocumentsCriteria = paragraphs.find({ "value": re.compile(el_value + '.*') })
    [ docs.append([doc.get('doc_id'), doc.get('doc_pos')]) for doc in allDocumentsCriteria ]
    #paragraphs.find({ "$and": [{"doc_id" : ObjectId("591c890d5bf62d3454ad097f")}, {"doc_pos": 26 }]})

    corpus = []
    print("Making Corpus from " + key + " Criteria")
    for doc_id, position in docs:
        if "OUTRO" in key:
            value = paragraphs.find({"$and": [{"doc_id": ObjectId(doc_id)}, {"doc_pos": position}]})[0].get('value')
            corpus.append(value)
        else:
            for c in range(1, 5):
                value = paragraphs.find({"$and": [{"doc_id": ObjectId(doc_id)}, {"doc_pos": position + c}]})[0].get('value')

                try:
                    if  len(value) > 15 and value[0].isupper() is False:
                        print("ok" + str(len(value)) + " ### " + str(doc_id))
                        corpus.append(value)
                except:
                    pass

    print("Writing Files")
    for count, value in enumerate(corpus):
        write_file(path + "/" + key.lower() + "_" + str(count), value)

    print("Splitting Training and Testing Set")
    move = []
    for i in obter_lista_documentos(path):
        if key.lower() in i:
            move.append(i)
    for i in range(0, int(len(move) * 0.3)):
        fname = move[i]
        dst_file = test_path + os.path.basename(fname)
        os.rename(fname, dst_file)










