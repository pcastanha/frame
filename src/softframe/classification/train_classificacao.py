"""
CLASSIFICATION TRAINING
=======================
The serialized model created consider the project structure, os and class definitions.
In case of changes in any of these topics please consider to recreate the model.
"""

from softframe.classification.tfdfc import *
from softframe.classification.utils import *
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline

import softframe.classification.lib as lib

train_dir = 'train/'
test_dir = 'test/'


train_filenames = obter_lista_documentos(train_dir)
test_filenames = obter_lista_documentos(test_dir)

train_docs = carregar_texto_de_lista_documentos(train_filenames)
n_train = len(train_docs)
train_names = train_docs.keys()

test_docs = carregar_texto_de_lista_documentos(test_filenames)
n_test = len(test_docs)
test_names = test_docs.keys()

print('Processando Documentos...')
train_corpus, train_y, train_filenames = zip(*montar_corpus(train_docs))
test_corpus, test_y, test_filenames = zip(*montar_corpus(train_docs))

pipeline = make_pipeline(
 CountVectorizer(min_df=30, max_df=0.99, ngram_range=(1, 4), encoding='utf-8'),
 TfdcfTransformer(use_product=False, norm='l2', sublinear_tf=True, binary=True, relative=False),
 # TfidfTransformer(norm='l2', use_idf=True, sublinear_tf=True),
 TruncatedSVD(100),
 # LogisticRegression(C=20.0, multi_class='multinomial', solver='lbfgs'))
 # SVC(C=150, gamma=2e-2, probability=True))
 GradientBoostingClassifier(n_estimators=50000, learning_rate=2**(-9.5), max_features='log2', max_depth=7, random_state=1, verbose=1))


print('Produzindo o Modelo...')
pipeline.fit(train_corpus, train_y)
print(pipeline.score(test_corpus, test_y))

print('Persistindo o Modelo...')
joblib.dump(pipeline, os.path.join(lib.MODELS_DIR, lib.CLASSIFICADOR_INICIAL_MODELO))
