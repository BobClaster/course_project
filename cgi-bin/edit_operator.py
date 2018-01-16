#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import html
import http.cookies
import os
import re


from engine import Session

wall = Session()

##########################################################################
##                                FORMS                                 ##
##########################################################################

bad_form = False
notific = ''
header = '...'
out = ''

form = cgi.FieldStorage()

id = form.getfirst("id", "")
id = html.escape(id) 

old_operator = form.getfirst("operator", "")
old_operator = html.escape(old_operator)

old_example = form.getfirst("example", "")
old_example = html.escape(old_example)

old_desc = form.getfirst("desc", "")
old_desc = html.escape(old_desc)


#    CHANGE OPERATOR
change_operator = form.getfirst("change_operator", "")
change_operator = html.escape(change_operator)

change_example = form.getfirst("change_example", "")
change_example = html.escape(change_example)

change_desc = form.getfirst("change_description", "")
change_desc = html.escape(change_desc)



if id != '' and change_operator != '' and change_example != '' and change_desc != '':
    notific = wall.edit_articles(id, change_operator, change_example, change_desc)
    if notific == 0:
        notific = "Ви успішно змінили даний запис."
    else:
        notific = "Помилка редагування.Спробуйте ще раз або"
    notific += '<br><a href="/cgi-bin/main.py">Повернутись до всіх записів</a>'

##########################################################################
##                              PRINTING                                ##
##########################################################################
# else:
file = open('html/pattern.html', 'r')
pattern = file.read()

header = 'Змінити оператор: ' + old_operator
out = '''
        <a href="/cgi-bin/main.py" class="menu">Всі оператори</a>
        <a href="/cgi-bin/add_operator.py" class="menu">Додати оператор</a>
         <form action="/cgi-bin/main.py" style="display: inline; ">
            <input name="search" type="text" placeholder="Пошук">
            <button type="submit">Пошук</button>
         </form>
         <hr>'''
out += '<form action="edit_operator.py" method="GET">'
out += '<input type="text" hidden name="id" placeholder="Operator" value="' + id + '">'
out += '<input type="text" name="change_operator" placeholder="Operator" value="' + old_operator + '">'
out += '<input type="text" name="change_example" placeholder="Example" value="' + old_example + '">'
out += '<input type="text" name="change_description" placeholder="Description" value="' + old_desc + '">'
out += '<button type="submit">Змінити</button>'
out += "</form>"

#           OUT
print('Content-type: text/html\n')
print(pattern.format(title=header, content=out, notifications=notific))
