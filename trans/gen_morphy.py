import sqlite3
import regex
from csv import DictWriter
import sys

def last_vowel(w):
        last_vowel_re = regex.compile("([АЄІЇОУЯЕЙЁЮаєіїоуяеию])([^АЄІЇОУЯЕЙЁЮаєіїоуяеию]*)")
        matches = last_vowel_re.findall(w)
        if len(matches) > 0:
                return len(w) - len(matches[0][1]) - 1
        else:
                return -1

def remove_stress(stressed):
        i = stressed.find('"')
        if i == -1:
                last_vowel_re = regex.compile("([АЄІЇОУЯЕЙЁЮаєіїоуяеию])([^АЄІЇОУЯЕЙЁЮаєіїоуяеию]*)")
                matches = last_vowel_re.findall(stressed)
                if len(matches) > 0:
                        return stressed, len(stressed) - len(matches[0][1]) - 1
                else:
                        return stressed, -1
        else:
                return stressed.replace('"', ''), i - 1

assert remove_stress('коммуни"зм') == ('коммунизм', 6)
assert remove_stress('а') == ('а', 0)
assert remove_stress('путин') == ('путин', 3)

def stress_snippet(tag, lemma, stress):
        snippet = lemma [0: stress]
        snippet += "<stress>" + lemma[stress] + "</stress>"
        snippet += lemma[stress + 1: ]
        element = "<{0}>{1}</{0}>".format(tag, snippet)
        return element

def write_to_file(morphy, doc):
        entry = etree.SubElement(doc.getroot(), "item")
        snippet = stress_snippet("stressed", morphy["lemma"], morphy["stress"])
        stressed = etree.fromstring(snippet)
        entry.append(stressed)
        for form in morphy["forms"]:
                stress_snippet("form", form["form"], form["stress"])
                stressed = etree.fromstring(snippet)
                entry.append(stressed)

conn = sqlite3.connect(sys.argv[1])
conn.row_factory = sqlite3.Row
c = conn.cursor()
c1 = conn.cursor()
c2 = conn.cursor()

c.execute("""SELECT nom_old as id, reestr, type, part, accent
             FROM nom""")

for lemma in c:
        base, stress = remove_stress(lemma["reestr"])
        #truncate base form to form the stem
        c1.execute("""SELECT indent as truncate, gr_id as gram
                      FROM indents
                      WHERE type = ?""", (lemma["type"],))
        truncate, gr_id = tuple(c1.fetchone())
        stem = base
        if (truncate > 0):
                stem = stem[:-truncate]
        #get all forms and parse them
        c1.execute("""SELECT flex, field2 as gram_cat
                      FROM flexes
                      WHERE type = ?""", (lemma["type"],))
        for flex in c1:
                form = {}
                remove_non_uk = regex.compile('\P{Cyrillic}')
                ending = flex["flex"]
                if ending is None or "empty" in ending:
                        form["form"] = stem
                else:
                        ending = remove_non_uk.sub('', ending)
                        form["form"] = stem + ending
                form["nom_id"] = lemma["id"]
                form["gram_id"] = flex["gram_cat"]                      
                c2.execute("""INSERT INTO Forms
                              VALUES(?,?,?)""", (form["form"], form["nom_id"], form["gram_id"]))
conn.commit()
conn.close()
