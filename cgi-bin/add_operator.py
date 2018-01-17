#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import html
import http.cookies
import os
import re


from engine import DataBase

wall = DataBase()

##########################################################################
##                                FORMS                                 ##
##########################################################################

bad_form = False
notific = ''
header = '...'
out = ''

form = cgi.FieldStorage()
#    ADD OPERATOR
add_operator = form.getfirst("add_operator", "")
add_operator = html.escape(add_operator)

add_example = form.getfirst("add_example", "")
add_example = html.escape(add_example)

add_desc = form.getfirst("add_description", "")
add_desc = html.escape(add_desc)



if add_operator != '' and add_example != '' and add_desc != '':
    notific = wall.add_article(add_operator, add_example, add_desc)
    if notific == 0:
        notific = "Оператор успішно додано"
    else:
        notific = "Помилка. Спробуйте ще раз, або"
    notific += '<br><a href="/cgi-bin/main.py">Повернутись до всіх записів</a>'

##########################################################################
##                              PRINTING                                ##
##########################################################################
# else:
file = open('html/pattern.html', 'r')
pattern = file.read()

header = 'Додати оператор'
out = """   
    <a href="/cgi-bin/main.py" class="menu">Всі оператори</a>
    <a href="/cgi-bin/add_operator.py" class="menu">Додати оператор</a>
    <form action="/cgi-bin/main.py" style="display: inline; ">
        <input name="search" type="text" placeholder="Пошук">
        <button type="submit">Пошук</button>
    </form>
    <hr>
    <form action="add_operator.py" method="GET" >
        <input type="text" name="add_operator" placeholder="Operator">
        <input type="text" name="add_example" placeholder="Example">
        <input type="text" name="add_description" placeholder="Description">
        <button type="submit">Додати</button>
    </form>
"""

#           OUT
print('Content-type: text/html\n')
print(pattern.format(title=header, content=out, notifications=notific))
