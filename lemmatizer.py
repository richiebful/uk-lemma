import sqlite3
import regex
import nltk

#@todo resolve issues with tokenizer separating words with apostophe
class SQLConnection:
        def __init__(self, file):
                self.db_file = file
        
        def get_lemma(self, form):
                conn = sqlite3.connect(self.db_file)
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                #might run into issues with capitalization later
                c.execute("""SELECT DISTINCT nom.reestr as lemma
                             FROM nom
                             JOIN forms
                             ON nom.nom_old = forms.nom_id
                             WHERE forms.form = ?
                          """, (form, ))
                result = c.fetchall()
                conn.commit()
                conn.close()
                return result

db_conn = SQLConnection("mph_ua.db")

def lemmatize_form(form):
        not_cyrillic = regex.compile('\P{Cyrillic}')
        if (not_cyrillic.search(form)):
                return form
        
        lemmas = db_conn.get_lemma(form)
        if lemmas is None or len(lemmas) == 0:
                form = form[0].swapcase() + form[1:]
                lemmas = db_conn.get_lemma(form)

        if lemmas is None or len(lemmas) == 0:
                return 'none'
        elif len(lemmas) == 1:
                return lemmas[0]["lemma"]
        else:
                return list([r[0] for r in lemmas])

def lemmatize(vect):
        return [lemmatize_form(form) for form in vect]

text = """
Єдиний діючий в Україні сміттєспалювальний завод «Енергія», розташований в Києві, тимчасово призупинив прийом сміття.

Про це повідомляє Київенерго.

Завод не приймає відходи через завершення 31 серпня дії угоди влади Києва з Київенерго. На підприємстві заявили, що вони мають близько 10 тонн запасів твердих побутових відходів, чого достатньо для планової роботи до 31 липня.

З 1 серпня завод переходить в управління міської влади як об'єкт комунальної власності.

На заводі «Енергія» в 2014 році побудували перемичку, яка з’єднала завод з міськими тепломережами. Тепло, яке отримується під час спалювання сміття, достатньо для забезпечення опалення та гарячою водою близько 300 багатоповерхівок.
достатньо
У Київенерго наголосили, що на сьогодні сміттєспалювальний завод є повноцінною міською міні-теплоцентраллю, а Київ — єдиним в Україні містом, де з побутового сміття проводиться і подається в мережі теплоенергія. Завод «Енергія» переробляє близько 25% обсягу твердих побутових відходів Києва."""

res = lemmatize(nltk.word_tokenize(text, language='ukrainian'))
tot_words = len(res)
ambig_words = len(list(filter(lambda w: type(w) == type([]), res)))
none_words = len(list(filter(lambda w: w == 'none', res)))
print(res)
print("ambiguous: %i %%" % (ambig_words / tot_words * 100))
print("none: %i %%" % (none_words / tot_words * 100))