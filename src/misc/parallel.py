import os
import abc
import tempfile

from time import time

from multiprocessing import Pool

import database as con

from selenium import webdriver

from lxml import etree
from lxml.html import fromstring

from nltk.tokenize import word_tokenize


class ParallelInterface(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.num = 1
        self.args = tuple()
        self.multiple = False

    @abc.abstractmethod
    def function(self, *args):
        pass

    def set_arguments(self, args):
        """
        args: Arguments used by the abstract function.\n
        Default to tuples of values (x,...) for single parameter call.\n
        Use as array of tuples [(x,...),...] for multiple parameters call.\n
        """

        if isinstance(args, list):
            self.multiple = True
        elif isinstance(args, tuple):
            self.multiple = False

        self.args = args

    def set_workers(self, num):
        self.num = num

    def run(self):
        pool = Pool(processes=self.num)

        if self.multiple is True:
            res = pool.starmap(self.function, self.args)
        else:
            res = pool.map(self.function, self.args)

        pool.close()
        pool.join()

        return res


class Element(object):

    def __init__(self, word, fam="N", font_size="N", under=False, bold=False, ita=False):
        self.word = word
        self.font_family = fam
        self.font_size = font_size
        self.underline = under
        self.bold = bold
        self.italic = ita

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.word == other.word
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __str__(self):
        """Define tostring method"""
        und = 'N'
        bol = 'N'
        ita = 'N'

        if self.underline is True:
            und = 'u'
        if self.bold is True:
            bol = 'b'
        if self.italic is True:
            ita = 'i'

        text = self.font_family + "_" + self.font_size + "_" + und + bol + ita

        return text

    def __repr__(self):
        """Some methods call repr for every element in a list"""
        return self.__str__()


class ExtractFeature(ParallelInterface):

    def function(self, html_str, doc_id):

        print("Processing doc: " + str(doc_id))

        database = con.DatabaseConnector()
        database.set_collection("words")

        browser = webdriver.PhantomJS("C:/Program Files/PhantomJS/bin/phantomjs.exe")

        tree = fromstring(html_str)

        fd, temp_path = tempfile.mkstemp(suffix=".html")  # Should point to the system temp directory
        f = open(temp_path, 'w')
        f.write(html_str)
        f.flush()
        os.fsync(fd)
        f.close()
        etree_ = etree.ElementTree(tree)
        els = tree.xpath('.//p')

        path = "file:///" + temp_path.replace("\\", "/")
        browser.get(path)

        paragraphs = []

        for pos, el in enumerate(els):

            unique = dict(zip(word_tokenize(str(el.text_content())), [Element(word) for word in word_tokenize(str(el.text_content()))]))

            for e in el.iter():
                try:
                    b_el = browser.find_element_by_xpath(str(etree_.getpath(e)))
                    tokens = word_tokenize(str(e.text_content()))

                    for token in tokens:
                        element = unique[token]
                        element.font_family = str(b_el.value_of_css_property("font-family"))
                        element.font_size = str(b_el.value_of_css_property("font-size"))
                        if e.tag == 'u':
                            element.underline = True
                        if e.tag == 'b':
                            element.bold = True
                        if e.tag == 'i':
                            element.italic = True

                        unique[token] = element
                        value = {str(unique[token]): token, "doc_pos": pos, "doc_id": doc_id}
                        database.insert_item(value)

                except Exception:
                    pass
                    # print("Exception")

            paragraphs.append(unique)

        os.close(fd)
        os.remove(temp_path)
        database.close_connection()
        print("Done doc: " + str(doc_id))


if __name__ == '__main__':
    t0 = time()

    NUM_WORKERS = 7
    db = con.DatabaseConnector()
    db.set_collection("documents")
    docs = db.get_all_items()
    db.close_connection()

    values = [(doc["value"], doc["_id"]) for doc in docs]

    ext = ExtractFeature()
    ext.set_workers(NUM_WORKERS)
    ext.set_arguments(values)
    out = ext.run()

    t0 = time() - t0
    print("Finished execution in %.4fs" % t0)
