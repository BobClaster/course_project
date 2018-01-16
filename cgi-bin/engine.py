import os
import random
import time
import sqlite3
import hashlib
from random import choice
from string import ascii_letters
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class DataBase:
    def __init__(self):
        self.name_db = 'db_for_php'
        self.__connect_to_db(self.name_db)
        # print("\n"+str(self.__create_table_in_db())+"\n")
        self.__close_db()

    def __connect_to_db(self, db_name):
        self.conn = sqlite3.connect(os.path.join(BASE_DIR, db_name))
        self.cursor_db = self.conn.cursor()

    def __create_table_in_db(self):
        sql_stmt = '''CREATE TABLE operators (id INTEGER PRIMARY KEY AUTOINCREMENT, operator VARCHAR)'''
        self.cursor_db.execute(sql_stmt)
        sql_stmt = '''CREATE TABLE example (id INTEGER PRIMARY KEY AUTOINCREMENT, text VARCHAR)'''
        self.cursor_db.execute(sql_stmt)
        sql_stmt = '''CREATE TABLE description (id INTEGER PRIMARY KEY AUTOINCREMENT, text VARCHAR)'''
        self.cursor_db.execute(sql_stmt)


    def __close_db(self):
        self.cursor_db.close()
        self.conn.close()        


    def _add_new_operator(self, operator):
        self.__connect_to_db(self.name_db)
        sql_stmt = '''INSERT INTO main.operators (operator) 
                      VALUES (?)'''
        self.cursor_db.execute(sql_stmt, (operator,))
        self.conn.commit()
        self.__close_db()
    

    def _add_example(self, text):
        self.__connect_to_db(self.name_db)
        sql_stmt = '''INSERT INTO example (text) 
                      VALUES (?)'''
        self.cursor_db.execute(sql_stmt, (text,))
        self.conn.commit()
        self.__close_db()
    

    def _add_description(self, text):
        self.__connect_to_db(self.name_db)
        sql_stmt = '''INSERT INTO description (text) 
                      VALUES (?)'''
        self.cursor_db.execute(sql_stmt, (text,))
        self.conn.commit()
        self.__close_db()

    
    def add_article(self, operator, text_for_example, text_for_description):
        try:
            self._add_new_operator(operator)
            self._add_example(text_for_example)
            self._add_description(text_for_description)
        except:
            pass
        else:
            return 0

    
    def get_all_articles(self):
        self.__connect_to_db(self.name_db)
        sql_stmt = '''SELECT oper.id, oper.operator, ex.text, descr.text
                      FROM main.operators oper, main.example ex, main.description descr
                      WHERE oper.id = ex.id AND oper.id = descr.id'''
        self.cursor_db.execute(sql_stmt)
        return self.cursor_db.fetchall()


    def get_article(self, id):
        self.__connect_to_db(self.name_db)
        sql_stmt = '''SELECT oper.id, oper.operator, ex.text, descr.text
                      FROM main.operators oper, main.example ex, main.description descr
                      WHERE oper.id = (?) AND ex.id = oper.id AND descr.id = oper.id'''
        self.cursor_db.execute(sql_stmt, (id,))
        self.conn.commit()
        self.__close_db()


    def edit_article(self, id, operator, text_for_example, text_for_description):
        try:
            self.__connect_to_db(self.name_db)
            sql_stmt = '''UPDATE main.operators
                        SET operator = ?
                        WHERE id = ?'''
            self.cursor_db.execute(sql_stmt, (operator, id))

            sql_stmt = '''UPDATE main.example
                        SET text = ?  
                        WHERE id = ?'''
            self.cursor_db.execute(sql_stmt, (text_for_example, id))

            sql_stmt = '''UPDATE main.description
                        SET text = ? 
                        WHERE id = ?'''
            self.cursor_db.execute(sql_stmt, (text_for_description, id))

            self.conn.commit()
            self.__close_db()
        except:
            pass
        else:
            return 0

    def delete_article(self, id):
        self.__connect_to_db(self.name_db)
        sql_stmt = '''DELETE FROM main.operators
                      WHERE main.operators.id = ?'''
        self.cursor_db.execute(sql_stmt, (id,))
        self.conn.commit()

        sql_stmt = '''DELETE FROM main.example
                      WHERE main.example.id = ?'''
        self.cursor_db.execute(sql_stmt, (id,))
        self.conn.commit()

        sql_stmt = '''DELETE FROM main.description 
                      WHERE main.description.id = ?'''
        self.cursor_db.execute(sql_stmt, (id,))
        self.conn.commit()

        self.__close_db()


    def search_operators(self, query):
        self.__connect_to_db(self.name_db)
        sql_stmt = '''SELECT oper.id, oper.operator, ex.text, descr.text
                      FROM main.operators oper, main.example ex, main.description descr
                      WHERE (oper.operator LIKE "%{0}%" OR ex.text LIKE "%{1}%" OR descr.text LIKE "%{2}%") 
                      AND oper.id = ex.id AND ex.id = descr.id'''.format(query, query, query)
        self.cursor_db.execute(sql_stmt)
        return self.cursor_db.fetchall()



class Session:
    def __init__(self):
        self.db = DataBase() 

    def get_all_articles(self,):
        return self.db.get_all_articles()

    def get_single_article(self, id):
        return self.db.get_article(id)
    
    def add_articles(self, operator, text_for_example, text_for_description):
        return self.db.add_article(operator, text_for_example, text_for_description)

    def edit_articles(self, id, operator, text_for_example, text_for_description):
        return self.db.edit_article(id, operator, text_for_example, text_for_description)
    
    def del_articles(self, id):
        self.db.delete_article(id)

    def search_operators(self, query):
        return self.db.search_operators(query)