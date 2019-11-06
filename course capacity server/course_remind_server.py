import socket
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
    driver = webdriver.Chrome('/usr/local/bin/chromedriver',options=chrome_options)

    # driver = webdriver.Chrome()
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
    if term == 'Term1':
        print(term)
        elem = driver.find_element_by_xpath('//*[@id="term5203Link"]')
        elem.click()
        time.sleep(0.2)
        elem = driver.find_element_by_xpath('//*[@id="term5203"]/form/div[2]/div/div/input')
        elem.send_keys(course_code)
        time.sleep(0.1)
        elem = driver.find_element_by_xpath('//*[@id="formSearchBtn5203"]')
        elem.click()
        page_s = driver.page_source
        if jugde_result_noll(page_s) == False:
            return driver,None
        elem = driver.find_element_by_xpath('/html/body/div[2]/form/div/button[1]')
        elem.click()

        return driver, page_s

    elif term == 'Term2':
        print(term)
        elem = driver.find_element_by_xpath('//*[@id="term5206Link"]')
        elem.click()
        time.sleep(0.3)
        elem = driver.find_element_by_xpath('//*[@id="term5206"]/form/div[2]/div/div/input')
        elem.send_keys(course_code)
        elem = driver.find_element_by_xpath('//*[@id="formSearchBtn5206"]')
        elem.click()
        page_s = driver.page_source
        if jugde_result_noll(page_s) == False:
            return driver,None
        elem = driver.find_element_by_xpath('/html/body/div[2]/form/div/button[1]')
        elem.click()
        return driver, page_s

    elif term == 'Term3':
        print(term)
        elem = driver.find_element_by_xpath('//*[@id="term5209Link"]')
        elem.click()
        time.sleep(0.4)
        elem = driver.find_element_by_xpath('//*[@id="term5209"]/form/div[2]/div/div/input')
        elem.send_keys(course_code)
        elem = driver.find_element_by_xpath('//*[@id="formSearchBtn5209"]')
        elem.click()
        page_s = driver.page_source
        if jugde_result_noll(page_s) == False:
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
        return [None],driver
    '''
    time.sleep(0.1)
    elem = driver.find_element_by_xpath('//*[@id="pt1:pt_gl3j_id_1"]')
    elem.click()
    time.sleep(0.1)
    elem = driver.find_element_by_xpath('//*[@id="pt1:r49ab54:0:i5::icon"]')
    elem.click()
    time.sleep(0.1)
    '''

    all_result = get_result(page_s)
    return all_result,driver




def deal_order_function(request_order,driver):

    course_code= request_order[0]
    term = request_order[1]

    # driver.refresh()
    all_result,driver = get_capacity(course_code, term,driver)
    return all_result,driver

print('server is initing!')
z_id, z_password = 'z5142915', 'Fromglentoglen456'
driver = init_page(z_id, z_password)
print('server init completed!')
print("The server is ready to receive")
#listening
start_time = time.time()
while 1:
    try:
        connectionSocket, addr = serverSocket.accept()
        request_pack = connectionSocket.recv(1024)
        print('Get one order')
        request_order = decode_response(request_pack)
        print(request_order)

        response_order,driver = deal_order_function(request_order,driver)
        print('return a response')
        print(response_order)

        response_pack = encode_request(response_order)
        print()
        connectionSocket.send(response_pack)
        connectionSocket.close()
    except socket.timeout:
        driver.refresh()
        print('page refreshed')
        print(f'server has been ran {time.time() - start_time}')
