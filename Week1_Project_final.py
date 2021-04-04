from bs4 import BeautifulSoup
from selenium import webdriver
import time, random, re
import pandas as pd

driver = webdriver.Chrome('C:/Users/Dang Quang/Desktop/chromedriver.exe') # need to download chromedriver.exe and change the path
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
            if name[0:2] == 'Ad':                                                         #product name
                name = name[2:]
            price = int(re.sub('\.', '', product.find('div', {'class':'price-discount__price'}).text[0:-1]))    #price
            img = product.img['src']                                                #product image
            purl = product['href']                                                  #url
            if 'tiki.vn' in purl:                                                   #some scraped URLs don't contain the Tiki.vn, so this adds them when needed
                purl = 'https:' + purl
            else:
                purl = 'https://tiki.vn' + purl
            if product.find('div', {'class':'price-discount__discount'}):           #Price Discount
                discount = product.find('div', {'class':'price-discount__discount'}).text
            else:
                discount = 'No'

            if product.find('div', {'class':'item'}):                               #TikiNow
                tikinow = 'Yes'
            else:
                tikinow = 'No'

            if product.find('div', {'class':'badge-under-price'}).img:              #Re Hon Hoan Tien
                badge = 'Yes'
            else:
                badge = 'No'

            if product.find('div', {'class':'badge-benefits'}).img:                 #Hot price badge
                zero = 'Yes'
            else:
                zero = 'No'

            if product.find('div', {'class':'review'}):                             #Reviews
                reviews = int(product.find('div', {'class':'review'}).text[1:-1])  
            else:
                reviews = 0

            if product.find('div', {'class':'rating__average'}):
                stars = int(product.find('div', {'class':'rating__average'})['style'].split()[1][0:-1].rstrip('%'))/20
            else:
                stars = 'Not available'

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

result.to_csv('C:/Users/Dang Quang/Desktop/result.csv', index = False) # need to change the path to save file .csv
