import pandas as pd
import urllib3.request
from bs4 import BeautifulSoup
import re
import requests

BASE_URL='http://www.cap.ru/news/'
proxy = {'http':'188.0.168.205:8080','http':'178.213.145.24:8080'}

def get_html(url):
    #response = urllib.request.urlopen(url)
    response = requests.get(url)
    #return response.read()
    return response.text

def get_page_count(html):
    soup = BeautifulSoup(html)
    last = soup.find('div', class_='PagerLast')
    return int(last.text.strip())

def parse(html):
    soup = BeautifulSoup(html)
    #soup = BeautifulSoup(response, 'html.parser')
    table = soup.find('div', class_='main_news')
    #rows =  soup.findAll('div', 'main_news')
    topics = table.findAll('div', class_='news_title')
    date = table.findAll('div', class_='doc_date')
    #time = re.findall(r'\d\d\:+\d\d',str(table))
    dates = re.findall(r'\d+\s\w+\s\d+\sг.',str(date))
    time = re.findall(r'\d\d\:+\d\d',str(date))
    
    z=1 #счётчик новостей
    news=[]

    for i in topics:
        #print("№"+str(z), '=> ' + i.text.strip())
        #dates = date[z-1].text.strip()
        #dd = re.findall(r'\d+\s\w+\s\d+\sг.',dates)
        #time = re.findall(r'\d\d\:+\d\d',str(dates))
        #print(z, dates, dd, type(dd)) # выводим дату на печать
        #print(dates, re.findall(r'\d+\s\w+\s\d+\sг.',dates)[0])
        z+=1
        news.append(i.text.strip())
        
        #df = pd.DataFrame({'time':time,'date':date, 'topics':list(all_topics)})
    df = pd.DataFrame({'topics':list(news), 'dates':list(dates), 'times':list(time)})
    return df
   
def myip():
    response = requests.get('http://pr-cy.ru/browser-details/', proxies = proxy)
    soup = BeautifulSoup(response.text)
    return soup.html.find('div', class_='ip').text
    
def main():
    print('Мой ip:',myip())
    #parse(get_html(BASE_URL))
    #print(get_page_count(get_html(BASE_URL)))
    pages = get_page_count(get_html(BASE_URL))
    print ("Найдено:", pages,"страниц")
    
    allnews = pd.DataFrame()
    
    for page in range(1, 1000):
        print('Парсинг %d%%' % (page / pages * 100))
        html = get_html(BASE_URL + '?page=%d' % page)
        allnews = allnews.append(parse(html), ignore_index = True)
        #print(parse(html))
    return allnews
   
if __name__ == '__main__':
    allnews = main()
    print(allnews)

    