from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from bs4 import BeautifulSoup
import requests
import json
# import csv
import xlsxwriter

app = Flask(__name__)

def fetchData(cat,auther,page=1,total=0,i=0,contents=[],first=True):
    if first:
        contents=[]
    if cat == "default" and auther == "default" :
        url =f'https://quotes.toscrape.com/page/{page}'
        is_auth_set =False
    else:
        if cat == "default" or auther == "default" :
            if cat=="default":
                url =f'https://quotes.toscrape.com/page/{page}'
            if auther == "default":
                url=f"https://quotes.toscrape.com/tag/{cat}/page/{page}"
                is_auth_set =False
        else:
                url=f"https://quotes.toscrape.com/tag/{cat}/page/{page}"
                is_auth_set =True

    response=requests.get(url)
    # print(response.status_code)
    soup = BeautifulSoup(response.content, 'html.parser')
    soup.prettify()
    # x =soup.find_all('a')
    x=soup.find_all(attrs={"class":"quote"})
    if auther != "default":
        for item in x:
            auth=item.find("small").text

            if auth==auther:
                h =item.find("a").get('href')
                contents.append([item.find("span").text[0:50],auth,h])   
                i=i+1
    else:
        for item in x:
            auth=item.find("small").text
            h =item.find("a").get('href')  
            contents.append([item.find("span").text[0:50],auth,h])     
    length = len(x)
    total=total+length
    if length > 0:
        page=page+1
        return fetchData(cat,auther,page,total,i,contents,False)

    return [total,i,contents]

def fetchDataExport(cat,auther,page=1,i=0,contents=[],first=True):
    if first:
        contents=[]
    if cat == "default" and auther == "default" :
        url =f'https://quotes.toscrape.com/page/{page}'
        is_auth_set =False
    else:
        if cat == "default" or auther == "default" :
            if cat=="default":
                url =f'https://quotes.toscrape.com/page/{page}'
            if auther == "default":
                url=f"https://quotes.toscrape.com/tag/{cat}/page/{page}"
                is_auth_set =False
        else:
                url=f"https://quotes.toscrape.com/tag/{cat}/page/{page}"
                is_auth_set =True

    response=requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    soup.prettify()
    x=soup.find_all(attrs={"class":"quote"})
    if auther != "default":
        for item in x:
            auth=item.find("small").text

            if auth==auther:
                contents.append([item.find("span").text[0:50],auth]) 
                i=i+1
    else:
        for item in x:
            auth=item.find("small").text
            contents.append([item.find("span").text[0:50],auth])
    length = len(x)

    if length > 0:
        page=page+1
        return fetchDataExport(cat,auther,page,i,contents,False)

    return contents

@app.route('/')
def index():
    return 'index'

@app.route('/scrap/<cat>/<auther>')
def scrap(cat,auther):
    return fetchData(cat,auther)
    #fetchData(cat=cat,auther=auther)
@app.route('/x/<cat>/<auther>')
def xx(cat,auther):
    array = fetchDataExport(cat,auther)
    return array

@app.route('/test/<cat>/<auther>')
def test(cat,auther):
    array = fetchDataExport(cat,auther)
    workbook = xlsxwriter.Workbook('arrays.xlsx')
    worksheet = workbook.add_worksheet()

    # array = [['a1', 'a2', 'a3'],
    #         ['a4', 'a5', 'a6'],
    #         ['a7', 'a8', 'a9'],
    #         ['a10', 'a11', 'a12', 'a13', 'a14']]

    # row = 0
    # worksheet.add_table('A:B', {'data': array})

    # worksheet.write_row("col1","col2")
    worksheet.write(0, 0, "النص")
    worksheet.write(0, 1, "الكاتب")

    for index, entity in enumerate(array):

        worksheet.write(index+1, 0, str(entity[0]))
        worksheet.write(index+1, 1, str(entity[1]))


    workbook.close()
    return "OK"


@app.route('/export')
def exportAsExcel():
    header = ['الكاتب', 'الموضوع']
    data = [['Afghanistan', 652090],
            ['AF', 'AFG']]

    with open('countries.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)
        # write the data
        writer.writerow(data)
    return "True"

@app.route('/x')
def x():
    workbook = xlsxwriter.Workbook('arrays.xlsx')
    worksheet = workbook.add_worksheet()

    array = [['a1', 'a2', 'a3'],
            ['a4', 'a5', 'a6'],
            ['a7', 'a8', 'a9'],
            ['a10', 'a11', 'a12', 'a13', 'a14']]

    row = 0

    for col, data in enumerate(array):
        worksheet.write_column(row, col, data)

    workbook.close()
    return "rrr"

@app.route('/')
@app.route('/<name>')
def user(name):
    return render_template("index.html",person=name)

if __name__ == '__main__':
   app.run(debug = True)


# @app.route('/login')
# def login():
#     return 'login'

# @app.route('/user/<username>')
# def profile(username):
#     return f'{username}\'s profile'
