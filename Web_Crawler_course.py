import requests
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup
import urllib.request

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
    #print(bs_new)
    main_url = 'https://www.handbook.unsw.edu.au'
    #print(url_new)
    #driver = webdriver.Chrome()
    #driver.get(url_new)
    #elem = driver.find_element_by_xpath('//*[@id="toggleLink_core_courses_1"]/div')
    #elem.click()
    #elem = driver.find_element_by_xpath('//*[@id="toggleBody_core_courses_1"]/div/div[1]')
    #print(elem)


    main = bs_new.find('div',{'class':'p-all-1 p-top-0'})

    all_card = main.find_all('div',{'class':'a-card a-card--has-body'})
    for card in all_card:
        course = card.find('div',{'data-hbui':'course-list'})
        #print(course)
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


    '''
    div_main = bs_new.find('div',{'role':'main'})
    #print(div_main)
    core_course = div_main.find('div', {'class': 'm-accordion-body'})
    #print(core_course)
    level_1 = core_course.find('div', {'data-hbui':'accordion__body-inner','class':'m-accordion-body-inner has-focus'})
    url_core_course = level_1.find_all('a')

    for i in url_core_course:
        all_url = {}
        all_url['course_code'] = i.find('span',{'class':'align-left'}).string
        if all_url['course_code'] not in all_url_list:
            all_url['course_name'] = i.find('span').string
            all_url['course_uoc'] = i.find('p').string
            all_url['url_core'] = main_url + i['href']
            all_url_list[all_url['course_code']] = all_url

    level_2 = core_course.find('div', {'sticky-parent':''})

    url_one_of_them = level_2.find_all('a')
    for i in url_one_of_them:
        all_url = {}
        all_url['course_code'] = i.find('span',{'class':'align-left'}).string
        print(all_url['course_code'])
        if all_url['course_code'] not in all_url_list:
            all_url['course_name'] = i.find('span').string
            all_url['course_uoc'] = i.find('p').string
            all_url['url_core'] = main_url + i['href']

            all_url_list[all_url['course_code']] = all_url
    '''
    return all_url_list


def get_course_list(html_text):
    bs = BeautifulSoup(html_text, "html.parser")
    body = bs.body
    main_url = 'https://www.handbook.unsw.edu.au'
    #print(main_url)
    undergraduate = body.find('div',{'data-hbui':'course-list'})
    program_name_1 = body.find('h1',{'class':'o-ai-overview__h1'})
    program_name = program_name_1.find('span').string
    all_url_list = {}
    url_under = undergraduate.find_all('a')

    for i in url_under:
        url_new = main_url+i['href'][:-2]
        #print(program_name)
        print(url_new)
        all_url_list = get_course_info(url_new,all_url_list)
        print(len(all_url_list.keys()))
    #print(all_url_list)

    return all_url_list


def sccc():
    url = 'https://www.handbook.unsw.edu.au/undergraduate/programs/2020/3778?browseByInterest=cd74ce13db96df002e4c126b3a96194f&'
    path = 'C:/Users/lenovo/Desktop/COMP9323'

    html_text = get_html(url)
    all_url_list = get_course_list(html_text)
    return all_url_list
