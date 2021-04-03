from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests, time, random, re
import pandas as pd

driver = webdriver.Chrome('C:/Users/Dang Quang/Desktop/chromedriver.exe')
page = 1
data = []


while True:
    time.sleep(random.randrange(3, 6))
    url = 'https://tiki.vn/laptop-may-vi-tinh-linh-kien/c1846?page=' + str(page)
    driver.get(url)

    time.sleep(random.randrange(4, 6))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    main = soup.find('div', {'data-view-id':'product_list_container'})
    products = main.find_all('a', {'class':'product-item'})
    print(url + ' Number of Products: '+ str(len(products)))
    
    if len(products) == 0:
        break

    for product in products:
        try:
            name = product.find('div', {'class':'name'}).text
            if name[0:2] == 'Ad':
                name = name[2:]
            price = product.find('div', {'class':'price-discount__price'}).text
            img = product.img['src']
            purl = product['href']
            
            if 'tiki.vn' in purl:
                purl = 'https:' + purl
            else:
                purl = 'https://tiki.vn' + purl
            if product.find('div', {'class':'price-discount__discount'}):
                discount = product.find('div', {'class':'price-discount__discount'}).text
            else:
                discount = 'No'

            if product.find('div', {'class':'item'}):
                tikinow = 'Yes'
            else:
                tikinow = 'No'

            if product.find('div', {'class':'badge-under-price'}).img:
                badge = 'Yes'
            else:
                badge = 'No'

            if product.find('div', {'class':'badge-benefits'}).img:
                zero = 'Yes'
            else:
                zero = 'No'

            if product.find('div', {'class':'review'}):
                reviews = product.find('div', {'class':'review'}).text[1:-1]
            else:
                reviews = 'Not available'

            if product.find('div', {'class':'rating__average'}):
                stars = int(product.find('div', {'class':'rating__average'})['style'].split()[1][0:-1].rstrip('%'))/20
            else:
                stars = 'N/A'

            if product.find('div', {'class':'freegift-list'}):
                gift = 'Yes'
            else:
                gift = 'No'

        except:
            print('There a error when scrapping')
        d = {'Product':name, 'Price':price, 'Image':img, 'Link':purl, 'Reviews':reviews, 'Stars':stars, 'Discount':discount, 'Tikinow':tikinow, 'Badge under price':badge, 'Installment':zero, 'gift':gift}
        data.append(d)
    page += 1

result = pd.DataFrame(data=data, columns = data[0].keys())

result.to_csv('C:/Users/Dang Quang/Desktop/result.csv', index = False)

# To-do: go to each page
# To-do: Use sleep to fake out
# To-do: make a table of data
