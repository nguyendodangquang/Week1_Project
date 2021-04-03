from bs4 import BeautifulSoup
import requests, time, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

page = 1
driver = webdriver.Chrome('C:/Users/Dang Quang/Desktop/chromedriver.exe')
data = []

while True:
    time.sleep(random.randrange(3, 6))
    url = 'https://tiki.vn/laptop-may-vi-tinh-linh-kien/c1846?page=' + str(page)
    driver.get(url)
    time.sleep(3)

    # driver.implicitly_wait(50)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    main = soup.find('div', {'data-view-id':'product_list_container'})
    products = main.find_all('a', {'class':'product-item'})
    if len(products) == 0:
        break

    print(url + ' Number of products: ' + str(len(products)))
    for product in products:
        try:
            name = product.find('div', {'class':'name'}).text
            price = product.find('div', {'class':'price-discount__price'}).text
            img = product.img['src']
            purl = product['href']
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
                stars = int(product.find('div', {'class':'rating__average'})['style'][6:][0:-1])
            else:
                stars = 'Not available'
                
            if product.find('div', {'class':'freegift-list'}):
                gift = 'Yes'
            else:
                gift = 'No'
            d = {'Product name': name, 'Price': price, 'Product Image': img, 'Product Url': purl, 'Discount': discount, 'Tikinow': tikinow, 'Badge under price':badge, 'Installment': zero, 'Reviews': reviews, 'Number of Stars': stars, 'Gift': gift}
            data.append(d)
        except:
            print('There is an error when scrapping')
        
    page += 1

productdata = pd.DataFrame(data=data, columns = data[0].keys())
productdata.to_csv('C:/Users/Dang Quang/Desktop/result.csv', index=False)

# To-do: go to each page
# To-do: Use sleep to fake out
# To-do: make a table of data

        