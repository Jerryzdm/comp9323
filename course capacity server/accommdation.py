
from bs4 import BeautifulSoup

import urllib.request




def make_url(input_requset_dir):
    url = 'https://www.realestate.com.au/rent/property-%s-between-%s-%s-in-%s/list-1?maxBeds=%s&source=refinement'\
          %(input_requset_dir['propertyType'],input_requset_dir['minPrice'],
            input_requset_dir['maxPrice'],input_requset_dir['where'],input_requset_dir['maxBeds'])
    return url


def congure_set(url):
    page = urllib.request.urlopen(url)
    contents = page.read()
    bs = BeautifulSoup(contents, "html.parser")
    return bs


def get_house_info(url):
    bs = congure_set(url)
    body = bs.body

    icon_info = body.find('ul',{'class':'general-features rui-clearfix'})
    all_features = icon_info.find_all('li', {'class': 'general-features__feature'})

    beds = all_features[0]['aria-label']
    try:
        bathrooms = all_features[1]['aria-label']
    except:
        bathrooms = '0 bathrooms'
    try:
        cars = all_features[2]['aria-label']
    except:
        cars = '0 parking'

    addr = body.find('h1', {'class': 'property-info-address'}).string
    type = body.find('span', {'class': 'property-info__property-type'}).string
    price = body.find('span', {'class': 'property-price property-info__price'}).string
    dir = {'price':price,'type':type,'addr':addr,'beds':beds,'bathrooms':bathrooms,'cars':cars,'url':url}
    return dir


def get_info_house(input_requset_dir):
    url = make_url(input_requset_dir)
    bs = congure_set(url)
    body = bs.body
    #print(body)
    links = body.find('div',{'class':'tiered-results tiered-results--exact'})
    all_links = links.find_all('a')
    #print(links)
    main_url = 'https://www.realestate.com.au'
    respo_info = []
    kk = []
    for i in all_links:
        new_link = main_url + i['href']
        if new_link not in kk:
            kk.append(new_link)
            try:
                dir = get_house_info(new_link)
                respo_info.append(dir)
            except:
                pass
            if len(respo_info) == 5:
                break

    return respo_info


#respo_info = get_info_house(input_requset_dir)
#print(respo_info)




