import requests
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup
import urllib.request
import Web_Crawler_course
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
            page = urllib.request.urlopen(url)
            contents = page.read()
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
    return contents

def get_course_info(url_new,all_url_list):
    html_new = get_html(url_new)
    bs_new = BeautifulSoup(html_new, "html.parser")
    main_url = 'https://www.handbook.unsw.edu.au'


    main = bs_new.find('div',{'class':'p-all-1 p-top-0'})

    all_card = main.find_all('div',{'class':'a-card a-card--has-body'})
    for card in all_card:
        course = card.find('div',{'data-hbui':'course-list'})
        all_course = course.find_all('a')
        for i in all_course:
            all_url = {}
            x = i.find('span', {'class': 'align-left'})
            if x != None:
                all_url['course_code'] = x.string
                if all_url['course_code'] not in all_url_list:
                    all_url['course_name'] = i.find('span').string
                    all_url['course_uoc'] = i.find('p').string
                    all_url['url_core'] = main_url + i['href']
                    all_url_list[all_url['course_code']] = all_url

        level_2 = card.find('div', {'sticky-parent': ''})
        if level_2 != None:
            url_one_of_them = level_2.find_all('a')
            for i in url_one_of_them:
                all_url = {}
                all_url['course_code'] = i.find('span', {'class': 'align-left'}).string
                if all_url['course_code'] not in all_url_list:
                    all_url['course_name'] = i.find('span').string
                    all_url['course_uoc'] = i.find('p').string
                    all_url['url_core'] = main_url + i['href']
                    all_url_list[all_url['course_code']] = all_url

    return all_url_list


def get_course_list(html_text,all_url_list):
    bs = BeautifulSoup(html_text, "html.parser")
    body = bs
    main_url = 'https://www.handbook.unsw.edu.au'
    program_name_1 = body.find('div',{'class':'p-all-1 p-top-0'})
    program_name_2 = program_name_1.find('div', {'data-hbui':'filters'})

    url_under = program_name_2.find_all('a')

    for i in url_under:
        try:
            url_new = main_url+i['href'][:-2]
            print(url_new)
            all_url_list = get_course_info(url_new,all_url_list)
            print(len(all_url_list.keys()))
        except:
            pass

    return all_url_list


if __name__ == '__main__':
    all_url_list = Web_Crawler_course.sccc()
    url = 'https://www.handbook.unsw.edu.au/postgraduate/programs/2020/8543?browseByInterest=cd74ce13db96df002e4c126b3a96194f&'
    #path = 'C:/Users/lenovo/Desktop/COMP9323/'

    html_text = get_html(url)
    all_url_list = get_course_list(html_text,all_url_list)
    print(all_url_list)
    new_dict = {'course_code': [], 'course_name': [], 'course_uoc': [], 'url_core': []}
    for k in all_url_list.keys():
        new_dict['course_code'].append(all_url_list[k]['course_code'])
        new_dict['course_name'].append(all_url_list[k]['course_name'])
        new_dict['course_uoc'].append(all_url_list[k]['course_uoc'])
        new_dict['url_core'].append(all_url_list[k]['url_core'].strip())

    data = pd.DataFrame.from_dict(new_dict)
    #print(data)
    #data.to_csv(path+'course.csv')
    print("Well done!")