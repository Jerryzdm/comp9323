import socket
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from courseRoutes import sendEmail
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

#server connect
serverPort = 12000 # change this port number if required
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.settimeout(45)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)


#encode_pack, dict -> json_str -> bytes
def encode_request(pack):
    pack_j = json.dumps(pack)
    encode_pack = pack_j.encode('UTF-8')
    return encode_pack

#decode_pack, bytes -> json_str -> dict
def decode_response(pack):
    decode_pack = pack.decode('UTF-8')
    return json.loads(decode_pack)

#push the request_order to Server_Transaction
#return the response from Server_Transaction

def congure_set():
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)

    #driver = webdriver.Chrome()
    # driver.get('https://ssologin.unsw.edu.au/cas/login?service=https%3A%2F%2Fmy.unsw.edu.au%2Fportal%2FadfAuthentication')
    driver.get(
        'https://ssologin.unsw.edu.au/cas/login?service=https%3A%2F%2Fmy.unsw.edu.au%2Factive%2FstudentClassEnrol%2Fcourses.xml')
    return driver

def login(z_id, z_password, driver):
    time.sleep(0.1)
    elem = driver.find_element_by_xpath('//*[@id="username"]')
    elem.send_keys(z_id)
    time.sleep(0.1)
    elem = driver.find_element_by_xpath('//*[@id="password"]')
    elem.send_keys(z_password)
    time.sleep(0.1)
    elem = driver.find_element_by_xpath('//*[@id="submit"]')
    elem.click()
    time.sleep(0.1)
    elem = driver.find_element_by_xpath('/html/body/div[2]/section/form/table/tbody/tr[1]/td[5]/button')
    elem.click()
    time.sleep(0.1)
    return driver

def input_course_code(course_code, term, driver):
    if term == 'Summer':
        elem = driver.find_element_by_xpath('//*[@id="term5202Link"]')
        elem.click()
        time.sleep(0.2)
        elem = driver.find_element_by_xpath('//*[@id="formSearchBtn5202"]')
        elem.click()
        time.sleep(0.2)

        elem = driver.find_element_by_xpath('//*[@id="freeText"]')
        elem.send_keys(course_code)
        elem = driver.find_element_by_xpath('/html/body/div[2]/form/div[2]/button[2]')
        elem.click()

        page_s = driver.page_source
        if jugde_result_noll(page_s) == False:
            elem = driver.find_element_by_xpath('/html/body/div[2]/form/div[2]/button[1]')
            elem.click()
            return driver, None

        elem = driver.find_element_by_xpath('/html/body/div[2]/form/div/button[1]')
        elem.click()

        return driver, page_s

    elif term == 'Term1':
        #print(term)
        elem = driver.find_element_by_xpath('//*[@id="term5203Link"]')
        elem.click()
        time.sleep(0.2)
        elem = driver.find_element_by_xpath('//*[@id="formSearchBtn5203"]')
        elem.click()
        time.sleep(0.2)

        elem = driver.find_element_by_xpath('//*[@id="freeText"]')
        elem.send_keys(course_code)
        elem = driver.find_element_by_xpath('/html/body/div[2]/form/div[2]/button[2]')
        elem.click()

        page_s = driver.page_source
        if jugde_result_noll(page_s) == False:
            elem = driver.find_element_by_xpath('/html/body/div[2]/form/div[2]/button[1]')
            elem.click()
            return driver,None

        elem = driver.find_element_by_xpath('/html/body/div[2]/form/div/button[1]')
        elem.click()

        return driver, page_s

    elif term == 'Term2':
        #print(term)
        elem = driver.find_element_by_xpath('//*[@id="term5206Link"]')
        elem.click()
        time.sleep(0.2)
        elem = driver.find_element_by_xpath('//*[@id="formSearchBtn5206"]')
        elem.click()
        time.sleep(0.2)

        elem = driver.find_element_by_xpath('//*[@id="freeText"]')
        elem.send_keys(course_code)
        elem = driver.find_element_by_xpath('/html/body/div[2]/form/div[2]/button[2]')
        elem.click()

        page_s = driver.page_source
        if jugde_result_noll(page_s) == False:
            elem = driver.find_element_by_xpath('/html/body/div[2]/form/div[2]/button[1]')
            elem.click()
            return driver,None

        elem = driver.find_element_by_xpath('/html/body/div[2]/form/div/button[1]')
        elem.click()

        return driver, page_s


    elif term == 'Term3':

        #print(term)
        elem = driver.find_element_by_xpath('//*[@id="term5209Link"]')
        elem.click()
        time.sleep(0.2)
        elem = driver.find_element_by_xpath('//*[@id="formSearchBtn5209"]')
        elem.click()
        time.sleep(0.5)

        elem = driver.find_element_by_xpath('//*[@id="freeText"]')
        elem.send_keys(course_code)
        elem = driver.find_element_by_xpath('/html/body/div[2]/form/div[2]/button[2]')
        elem.click()

        time.sleep(0.1)

        page_s = driver.page_source
        print(page_s)
        if jugde_result_noll(page_s) == False:
            elem = driver.find_element_by_xpath('/html/body/div[2]/form/div[2]/button[1]')
            elem.click()
            return driver,None

        elem = driver.find_element_by_xpath('/html/body/div[2]/form/div/button[1]')
        elem.click()

        return driver, page_s
    else:
        return driver, None


def jugde_result_noll(page_s):
    bs = BeautifulSoup(page_s, "html.parser")
    body = bs.body
    if body.find('div', {'role': 'alert'}) is not None:
        return False
    return True

def get_result(page_s):
    bs = BeautifulSoup(page_s, "html.parser")
    body = bs.body
    tbody = body.find('tbody')
    trs = tbody.find_all('tr')
    all_result = []
    for tr in trs:
        co = []
        all_td = tr.find_all('td')
        for td in all_td:
            co.append(str(td.string))
        all_result.append(co)
    # print(body)
    # print(all_result)
    return all_result

def init_page(z_id, z_password):
    driver = congure_set()
    driver = login(z_id, z_password, driver)
    return driver

def get_capacity(course_code, term,driver):
    driver, page_s = input_course_code(course_code, term, driver)
    if page_s == None:
        return [],driver

    #print(page_s)
    all_result = get_result(page_s)
    return all_result,driver

def deal_order_function(request_order,driver):

    course_code= request_order['course_code']
    term = request_order['term']

    # driver.refresh()
    all_result,driver = get_capacity(course_code, term,driver)


    result_return = {'Undergraduate':[],'Postgraduate':[]}
    #print(all_result)

    for i in all_result:
        if 'Undergraduate' in i:
            result_return['Undergraduate'].append(i)
        if 'Postgraduate' in i:
            result_return['Postgraduate'].append(i)


    seat_list = result_return[request_order['phase']]
    #print('seat_list',seat_list)
    if seat_list == []:
        flag = True
    else:
        flag = space_ava_flag(seat_list)
    result = {'flag':flag,'all_result':seat_list,'message':None}

    return result,driver





print('server is initing!')
z_id, z_password = 'z5142915', 'Fromglentoglen456'
driver = init_page(z_id, z_password)
print('server init completed!')
print("The server is ready to receive")
#listening
start_time = time.time()

search_co_list = {}

def add_in_list(search_co_list,request_order):
    course_code = request_order['course_code']
    email = request_order['email']
    if course_code not in search_co_list:
        search_co_list[course_code] = {'email': [email], 'request_order': request_order,
                                       'created_time': time.time()}
    elif email not in search_co_list[course_code]['email']:
        search_co_list[course_code]['email'].append(email)
    return search_co_list


def remove_out_list(search_co_list):
    time_out_list = []
    k_list = list(search_co_list.keys())
    for k in k_list:
        if time.time() - search_co_list[k]['created_time']>=200:
            time_out_list.append(search_co_list.pop(k))
    return search_co_list,time_out_list

def space_ava_flag(seat_list):
    for seat in seat_list:
        ava = int(seat[-2].split('/')[0].strip())
        total = int(seat[-2].split('/')[1].strip())
        if ava<total:
            return True
    return False

def send_email(capacity,course_code,email_list):
    sendEmail(capacity,course_code,email_list)
    for i in email_list:
        print(f'send {i} done!')

def search_in_refresh_time(search_co_list,driver):
    success_find_list = []
    search_wait_list = list(search_co_list.keys())
    for k in search_wait_list:
        request_order = search_co_list[k]['request_order']
        email_list = search_co_list[k]['email']
        course_code = k

        response_order, driver = deal_order_function(request_order, driver)

        if response_order['flag'] == True:
            capacity = response_order['all_result'][7]
            send_email(capacity,course_code,email_list)
            success_find_list.append(search_co_list.pop(k))
    return search_co_list,driver,success_find_list

start_time_s = time.time()
while True:
    if time.time() - start_time_s >1000:
        break
    try:
        connectionSocket, addr = serverSocket.accept()
        request_pack = connectionSocket.recv(1024)
        print('Get one order')
        request_order = decode_response(request_pack)
        print(request_order)


        response_order,driver = deal_order_function(request_order,driver)
        print('return a response')

        if request_order['query_type_flag'] == 'bind' and response_order['flag'] == False:
            search_co_list = add_in_list(search_co_list, request_order)
            response_order['message'] = 'course binded'
            print('this order is binded')
        elif request_order['query_type_flag'] == 'bind' and response_order['flag'] == True:
            response_order['message'] = 'space available or no that course'
            print('this order is unbinded')
        print(response_order)
        response_pack = encode_request(response_order)
        print()
        connectionSocket.send(response_pack)
        connectionSocket.close()

        search_co_list,time_out_list = remove_out_list(search_co_list)
        print('because courses are time out, remove out them from wait list:')
        print(time_out_list)
        search_co_list, driver,success_find_list = search_in_refresh_time(search_co_list, driver)
        print('because courses are found, remove out them from wait list:')
        print(success_find_list)

    except socket.timeout:
        driver.refresh()
        print('page refreshed')
        search_co_list,time_out_list = remove_out_list(search_co_list)
        print('because courses are time out, remove out them from wait list:')
        print(time_out_list)
        search_co_list, driver,success_find_list = search_in_refresh_time(search_co_list, driver)
        print('because courses are found, remove out them from wait list:')
        print(success_find_list)
        print(f'server has been ran {time.time() - start_time}')
