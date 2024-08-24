from bs4 import BeautifulSoup
import requests
import json
#'https://quotes.toscrape.com/'
# print(f"https://quotes.toscrape.com/tag/{cat}/page/{page}/")
def scrsp(cat,author,page=1,total=0):
    print(f"page number {page}")
    if cat == "":
        url =f'https://quotes.toscrape.com/page/{page}'
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
    if is_auth_set:
        contents=[]
        i=0
        for item in x:
            contents.append(item.find("span").text)
            auth=item.find("small").text
            if auth==author:
                i=i+1
                print(item.find(attrs={"class":"text"}).text)
    # if is_auth_set:
    #     print("")       
    length = len(x)
    total=total+length
    if length > 0:
        page=page+1
        scrap(cat,author,page,total)
        # print(contents)
        # print('.................................')
    return [total,i,contents]
t = scrap(cat,author)
# r=json.dumps(t)
print(t)
# print(soup.span)