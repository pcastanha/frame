
from os import walk
from io import BytesIO
from pickle import load
from pkgutil import get_data

# Third party imports

from nltk.tokenize.punkt import PunktSentenceTokenizer

from lxml.html import fromstring

import requests


class Parser(object):

    _PT_BR_CORPUS = "tokenizers/punkt/portuguese.pickle"
    _CONVERTER_URL = "http://soft050-049:8081/doc-conv/converter"

    def __init__(self):

        # The naming ``cli.resources`` will raise an error if this is file executed as script
        # Change to ``resources`` to debug as script
        # self._PRE_TRAINED = load(BytesIO(get_data("cli.resources", "files/data.pickle")))
        self._PRE_TRAINED = load(BytesIO(get_data("resources", "files/data.pickle")))
        self.tokenizer = PunktSentenceTokenizer(self._PRE_TRAINED)

    @staticmethod
    def convert_html_to_string(url):
        if url is not None:
            print("Initiating request")
            doc = requests.get(url).text
            print("Done")
        else:
            doc = None
            print("URL should not be empty")

        return doc

    @staticmethod
    def read_html(html_string=None, url=None):
        if url is not None:
            content = requests.get(url).text
            doc = fromstring(content)
        else:
            if html_string is None:
                doc = None
                print("Html string should not be empty")
            else:
                doc = fromstring(html_string)

        return doc

    @staticmethod
    def find_paragraphs(html):
        els = html.findall(".//p")
        paragraphs = []

        for el in els:
            txt = el.text_content()
            paragraphs.append(txt.strip())

        return paragraphs

    def convert_pdf_to_html(self, file_path):
        try:
            name = file_path.split("\\")[-1]

            file_ = {
                        'file': (name,
                        open(file_path, 'rb'),
                        'multipart/form-data')
                    }

            r = requests.post(self._CONVERTER_URL, files=file_)
            return r.text
        except Exception as e:
            print(repr(e))
            return None

    @staticmethod
    def find_files(path):
        for dirpath, dirnames, filenames in walk(path):
            print("Found %d files at %s" % (len(filenames), path))

        result = [path + "\\" + f for f in filenames]

        return result

    def sentence_extractor(self, data, list_=False):
        if list_ is not False:
            result = []
            for p in data:
                result.append([s for s in self.tokenizer.tokenize(p)])

        else:
            result = [s for s in self.tokenizer.tokenize(data)]

        return result


def main():
    pass

if __name__ == "__main__":
    main()
