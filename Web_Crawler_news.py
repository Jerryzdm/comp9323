import requests
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup


def get_html(url, data=None):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
    }

    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url, headers=header, timeout=timeout)
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print('3:', e)
            time.sleep(random.choice(range(8, 15)))
        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20, 60)))
        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30, 80)))
        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(5, 15)))
    return rep.text


def get_top_10_news_list(url,html_text):
    bs = BeautifulSoup(html_text, "html.parser")
    body = bs.body
    main_url = url[:-7]
    #print(main_url)
    #print(body)

    top_10_news = bs.find('div', {'class': 'content-wrapper'})
    all_news_list = {}
    for i in range(1,11):
        if i%2 == 1:
            class_name = 'views-row views-row-%s views-row-odd' % str(i)
        else:
            class_name = 'views-row views-row-%s views-row-even' % str(i)
        if i == 1:
            class_name += ' views-row-first'
        if i == 10:
            class_name += ' views-row-last'
        news = top_10_news.find('div', {'class': class_name})

        news_link = news.find('a')['href']
        imageURL = news.find('img')['src']
        #u = urllib.request.urlopen(imageURL)
        #img_bo = u.read()
        news_link_combine = main_url+news_link
        title = news.find('h2',{'class':'headline'}).string
        date = news.find('div',{'class':'field-post-date'}).string
        standfirst_1 = news.find('div', {'class': 'field-standfirst'})
        standfirst = standfirst_1.find('p').string

        new_num = {'title':title,'date':date.strip(),'standfirst':standfirst,'link':news_link_combine,
                   'img_bo':imageURL}

        all_news_list['new_'+str(i-1)] = new_num
    #print(Level_6)
    return all_news_list


def return_10_news():
    url = 'https://newsroom.unsw.edu.au/search'
    #path = 'C:/Users/lenovo/Desktop/COMP9323'

    html_text = get_html(url)
    all_news_list = get_top_10_news_list(url,html_text)
    #print(all_news_list)
    #print("Well done!")
    return all_news_list
print(return_10_news())

