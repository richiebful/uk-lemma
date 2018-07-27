import sqlite3

class SQLConnection:
        def __init__(self, file):
                self.db_file = file
        
        def get_lemma(self, form):
                conn = sqlite3.connect(self.db_file)
                conn.row_factory = sqlite3.Row
                c = self.conn.cursor()
                #might run into issues with capitalization later
                c.execute("""SELECT nom.reestr
                             FROM nom
                             JOIN forms
                             ON nom.nom_old = forms.nom_id
                             WHERE forms.form = ?
                          """, (form, ))
                c.commit()
                conn.close()