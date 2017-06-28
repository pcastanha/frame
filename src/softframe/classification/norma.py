# encoding: utf-8
import re


def normas(text):
    #ARTIGO = r'(?P<artigo>art(igo)?\s*\.*\s*\d+\s*\,*\d+\s*\,*(e)*\s*\d+)'
    ARTIGO = r'(?P<artigo>art(igo)*\s*\.*\s*\d*(\s)*(º)*\s*(\(\.\.\.\))*(e\s)*\,*\d*(\s)*\,*\s*[LIVX]*( do CDC)*)'
    PARAGRAFO = r"(?P<paragrafo>(§\s+\d+|par[áa]grafo\ [úu]nico|par[áa]grafo\s?\.?\s?\d+))"
    INCISO = r"(?P<inciso>inciso(s)*\s*[IVX](,)*\s*(e)*\s*[IVX]*\s*(e)*\s*[IVX]*)"
    TITULO = r"(?P<titulo>T[ÍI]TULO\s+[IVX]+)"
    CAPITULO = r"(?P<capitulo>cap[íi]tulo\s+[IVXL]+)"
    LEI = r"(?P<lei>Lei\s*(municipal|estadual|federal)*\s*[n]*\.*[º]*\s+[\d\.]*\s*(,)*(\s+de\s+)*(\d{1,2}[\/\.]\d{1,2}[\/\.])*\s*(\/)*\s*\d{2,4})"
    DECRETO = r"(?P<decreto>Decreto\s*[nº]*\s+[\d\.]*\s*(,)*(\s+de\s+)*(\d{1,2}[\/\.]\d{1,2}[\/\.])*\s*(\/)*\s*\d{2,4})"
    CODIGO = r"(?P<codigo>C[óo]digo Comercial|C[óo]digo Civil|C[óo]digo de Águas|(C[óo]digo de Defesa do Consumidor)|C[óo]digo Penal|C[óo]digo de Processo Penal|C[óo]digo Brasileiro de Telecomunicações|C[óo]digo Florestal|C[óo]digo Eleitoral|C[óo]digo Sanit[áa]rio do Distrito Federal|C[óo]digo Tribut[áa]rio Nacional|C[óo]digo de Processo Penal Militar|C[óo]digo Penal Militar|C[óo]digo de Minera[çc][ãa]o|C[óo]digo de Minas|C[óo]digo de Ca[çc]a - Prote[çc][ãa]o a Fauna|C[óo]digo de Processo Civil|C[óo]digo Brasileiro de Aeron[áa]utica|C[óo]digo de Menores|Estatuto da Crian[çc]a e do Adolescente|C[óo]digo de Propriedade Industrial|C[óo]digo de Tr[âa]nsito Brasileiro|C[óo]digo de Conduta da Alta Administra[çc][ãa]o Federal|Consolida[çc][ãa]o das Leis do Trabalho\s*-*\s*(CLT)*|Carta Magna de 1988)"
    VIGENCIA = r"(?P<vigencia>Vigência)"
    NORMAS = [LEI, CODIGO, ARTIGO, PARAGRAFO, INCISO, TITULO, DECRETO, VIGENCIA, CAPITULO]
    TAG = re.compile(r'|'.join(NORMAS), re.IGNORECASE)

    d = {}

    def obter_normas(text, regex):
        try:
            d = {}
            for k in [m.groupdict() for m in regex.finditer(text)][0]:
                d[k] = list(d[k] for d in [m.groupdict() for m in regex.finditer(text)] if d[k])
            return dict((k, v) for k, v in d.iteritems() if v)
        except IndexError:
            return None

    return obter_normas(text, TAG)
