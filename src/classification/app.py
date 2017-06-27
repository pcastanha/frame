from flask import Flask, request, jsonify
from sklearn.externals import joblib
from os.path import join
from classification.utils import *
from classification.norma import *
import classification.lib as lib


app = Flask(__name__)


#@app.route('/classify', methods=['POST'])
def classificador_documentos():
    corpo = checar_retorno(request.get_json(), 'JSON Vazio')
    texto_documento = checar_retorno(unidecode(corpo.get('texto')), 'JSON Nao possui campo texto')
    tipos = checar_retorno(corpo.get('tipos'), 'Tipo de Classificacao nao informada')
    sugestoes_por_tipo = []
    for tipo_sugestao in tipos:
        sugestoes_por_tipo.append({tipo_sugestao: classificar_documento_para_tipo(texto_documento, tipo_sugestao)})

    return jsonify(normas=normas(texto_documento), resultado=sugestoes_por_tipo)


def classificar_documento_para_tipo(texto_documento, tipo_classificacao):
    classificador = classificador_para(tipo_classificacao)

    if classificador is None:
        return []
    probs = classificador.predict_proba([texto_documento])[0]
    sugestoes = sorted(zip(classificador.classes_, probs), key=lambda name_prob: name_prob[1], reverse=True)
    return [criar_sugestoes(class_name, prob) for class_name, prob in sugestoes]


def classificador_para(nome_classe):
    return classifiers.get(nome_classe)


def criar_sugestoes(classificacao, probabilidade):
    probabilidade = '%.6f' % probabilidade
    return {'classe': classificacao, 'probabilidade': probabilidade}


def produzir_modelo(info):
        return {nome_classe: joblib.load(join(lib.MODELS_DIR, model_filename))
                for nome_classe, model_filename in info.items()}

classifiers = produzir_modelo({
    lib.CLASSIFICADOR_INICIAL: lib.CLASSIFICADOR_INICIAL_MODELO,
})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')




