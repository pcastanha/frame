import os
import codecs
import requests, json
from os import walk
from sklearn.datasets import load_svmlight_file
import pickle
from text_unidecode import unidecode


def TextToDep(text):
    dados = {"doc": text }
    jsonArray = json.dumps(dados)
    response = requests.post("http://172.23.227.172:4567/parse", data=jsonArray)
    tags = response.json()
    return tags


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_file(filename, doc):
    file = codecs.open(filename, "w", "utf-8")
    file.write(doc)
    file.close()


def load_file(filename):
    X, y = load_svmlight_file(filename)
    return X, y


def FastSerialize(obj, file):
    f = open(file, 'wb')
    pickle.dump(obj, file)
    f.close()
    return 0


def FastLoad(obj, file):
    f = open(file, 'rb')
    obj = pickle.load(file)
    return obj


def load_file_as_list(filename):
    with open(filename) as f:
        l = f.read().splitlines()
    return l


def tokenize(text):
    return([text.split('#', 1)[0].strip()])


def carregar_texto_de_lista_documentos(filenames, tag=False):
    docs = {}
    for filename in filenames:
        if "svmlight" not in filename:
            # implementar teste de filesize
            with codecs.open(filename=filename, encoding='utf8') as f:
                if tag is False:
                    text = f.read().strip()
                else:
                    text = ' '.join(TextToDep(f.read().strip()))
                docs[filename] = text
    return docs


def separar_texto_em_tokens(docs, stopwords=set([])):
    corpus = {}
    for key, val in docs.items():
        corpus[key] = [word for word in val.split() if word not in stopwords]
    return corpus


def checar_retorno(arg, message):
    if arg is None:
        raise ValueError(message)
    return arg


def montar_corpus(documento):
    saida = []
    for i in documento.keys():
        label = i.split('/')[1].split('_')[0]
        saida.append([unidecode(documento.get(i)), label, i])
    return saida


def obter_lista_documentos(path):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        for filename in filenames:
            f.append(dirpath + filename)
    return f
