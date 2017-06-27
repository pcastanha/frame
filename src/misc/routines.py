import json
import os
import tempfile
from time import time

from selenium import webdriver

from classification import lib
from classification.app import classificar_documento_para_tipo
from database.connection import DatabaseConnector
from processing.utils import Parser


def read_and_convert(path):
    parser = Parser()
    con_ = DatabaseConnector()
    files = parser.find_files(path)

    for i, f in enumerate(files):
        print("Reading HTML document...")
        print("File %d: %s" % (i, f))
        pdf2html = parser.convert_pdf_to_html(f)
        print("Done... ")

        if pdf2html is not None:
            try:
                print("Parsing HTML")
                html_ = parser.read_html(html_string=pdf2html)
                db_doc = {"value": pdf2html}
                print("Done... ")

                print("Inserting document at DB...")
                con_.set_collection("documents")
                doc_id = con_.insert_item(db_doc)
                print("Done...")

                print("Extracting paragraphs...")
                pars = parser.find_paragraphs(html_)
                if len(pars) > 0:
                    objs = [{"doc_pos": idx, "value": el, "doc_id": doc_id} for idx, el in enumerate(pars)]
                    print("Done...")

                    print("Inserting paragraphs at DB...")
                    con_.set_collection("paragraphs")
                    pars_ids = con_.bulk_insert_items(objs)
                    print("Done...")

                    print("Extracting sentences...")
                    sen_insert_list = []
                    tuples = zip(pars_ids, pars)

                    for par_id, par in tuples:
                        sentences = parser.sentence_extractor(par)
                        sen_objs = [{"doc_id": doc_id, "par_id": par_id, "par_pos": idx, "value": el} for idx, el in enumerate(sentences)]
                        sen_insert_list.extend(sen_objs)
                    print("Done...")

                    print("Inserting sentences at DB...")
                    con_.set_collection("sentences")
                    con_.bulk_insert_items(sen_insert_list)
                    print("Done...")
            except Exception as e:
                print(repr(e))

        else:
            print("Failed to parse pdf.")

        print("Closing connection...")
        con_.close_connection()
        print("Done...")


def classify_paragraphs(html):
    parser = Parser()
    # 'phantomjs.exe' executable needs to be in PATH
    driver = webdriver.PhantomJS("../misc/resources/files/phantomjs.exe")  # Headless browser used by selenium

    element_tree = parser.read_html(html_string=html.strip())  # Convert html string to LXML ElementTree
    paragraphs = element_tree.xpath(".//p")

    __, temp_path = tempfile.mkstemp(suffix=".html")  # Should point to the system temp directory
    with open(temp_path, encoding='utf8', mode='w') as f:
        f.write(html)

    response = []  # Response array used to store every sentence classified and its respective xpath location

    if os.name == "nt":
        path = "file:///" + temp_path.replace("\\", "/")

    else:
        path = "file:///" + temp_path

    for paragraph in paragraphs:
        raw_text = paragraph.text_content()
        sentences = parser.sentence_extractor(raw_text)

        for sentence in sentences:
            driver.get(path)
            try:
                text_to_find = sentence.strip()
                classification = classificar_documento_para_tipo(text_to_find, lib.CLASSIFICADOR_INICIAL)  # Classify
                javascript_string = \
                    json.dumps("window.find('{}'); return window.getSelection().getRangeAt(0);".format(text_to_find),
                               ensure_ascii=False)
                path_object = driver.execute_script(javascript_string[1:-1])  # Remove leading and trailing quotes
                response.append({"prediction": classification, "path": path_object})
            except Exception as e:
                print(javascript_string)

    os.close(__)
    os.remove(temp_path)

    return response

if __name__ == '__main__':

    t0 = time()
    with open("C:/Users/pedro.castanha/Downloads/file_1.html", encoding="utf8", mode='r') as f:
        html_string = f.read()

    locations = classify_paragraphs(html_string)
    t0 = time() - t0

    print("Done in {}".format(t0))
    print(len(locations))
    print(locations)
