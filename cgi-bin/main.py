#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import html
import http.cookies
import os
import re
import urllib.request as urllib2

from engine import Session

wall = Session()

notific = ''
header = '...'
out = ''

form = cgi.FieldStorage()

delete = form.getfirst("delete", "")
delete = html.escape(delete)

search = form.getfirst("search", "")
search = html.escape(search)

if delete != '':
    wall.del_articles(int(delete))
    articles = wall.get_all_articles()

elif search != '':
    articles = wall.search_operators(search)
    notific = 'За запитом "<b>' + search + '</b>" знайдено записів: <b>' + str(len(articles)) + '</b><br><a href="/cgi-bin/main.py">Повернутись до всіх записів</a>'

else:
    articles = wall.get_all_articles()




##########################################################################
##                              PRINTING                                ##
##########################################################################

file = open('html/pattern.html', 'r')
pattern = file.read()

header = 'All operators'
out ="""
        <a href="/cgi-bin/main.py" class="menu" >Всі оператори</a>
        <a href="/cgi-bin/add_operator.py" class="menu" >Додати оператор</a>
        <form action="/cgi-bin/main.py" style="display: inline; ">
            <input name="search" type="text" placeholder="Пошук">
            <button type="submit">Пошук</button>
        </form>
        <hr>
        
        <table>
        
        <tr>
            <td><h3>ID</h3></td>
            <td><h3>Оператор</h3></td>
            <td><h3>Приклад</h3></td>
            <td><h3>Опис</h3></td>
            <td><h3>Навігація</h3></td>
        </tr>
        """
for article in articles:
    out += '<tr>'
    out += "<td>" + str(article[0]) + "</td>"
    out += "<td>" + str(article[1]) + "</td>"
    out += "<td>" + str(article[2]) + "</td>"
    out += "<td>" + str(article[3]) + "</td>"
    out += "<td style='width: 100px;'>"
    out += "<a href='/cgi-bin/edit_operator.py?id=" + str(article[0]) + "&operator=" + article[1] + "&example=" + article[2] + "&desc=" + article[3] + "'><img src='../html/img/edit.png' style='width: 25px; padding: 4px;'></a>"
    out += "<a href=''><img src='../html/img/copy.png' style='width: 25px; padding: 4px;'></a>"
    out += "<a href='?delete=" + str(article[0]) + "' ><img src='../html/img/delete.ico'  style='width: 25px; padding: 4px;'></a>"
    out += "</td>"
    out += '</tr>'

#           OUT
print('Content-type: text/html\n')
print(pattern.format(title=header, content=out, notifications=notific))
