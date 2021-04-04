!pip install selenium
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
!pip install webdriver-manager
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager #install chromedriver
options = webdriver.ChromeOptions()
options.add_argument('-headless') # since we run selenium on Google Colab so we don't want a chrome browser opens, so it will run in the background
options.add_argument('-no-sandbox')
options.add_argument('-disable-dev-shm-usage')
options.add_argument("--incognito")
driver = webdriver.Chrome('chromedriver',options=options)
# driver.implicitly_wait(30)  # we let selenium to wait for few seconds for all javascript script done before return the result of HTML, but we can use sleep() insteed.

from bs4 import BeautifulSoup
import time, random
import pandas as pd

# driver = webdriver.Chrome('C:/Users/Dang Quang/Desktop/chromedriver.exe')
page = 1
data = []


while True:
  # Everything here at the top is going to search the product category, soup it and strips for two things: a div called "product_list_container" and within 
  # that the target web item: an 'a' tag with the class "product item" that contains needed product info. This is assigned to "products." Once the products are scraped, the page number url advances
  # by one to the next product page to find all the "products."

    time.sleep(random.randrange(3, 6))
    url = 'https://tiki.vn/laptop-may-vi-tinh-linh-kien/c1846?page=' + str(page)
    driver.get(url)

    time.sleep(random.randrange(4, 6))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    main = soup.find('div', {'data-view-id':'product_list_container'})
    products = main.find_all('a', {'class':'product-item'})
    print(url + ' Number of Products: '+ str(len(products)))                        #To keep track which page we are currenly on and number of products on that page

    # If the function finds a page with no "products", then it breaks.
    
    if len(products) == 0:
        break

    #Since products is the section of the web page that contains all the info, we use the individual functions below to scrape the following info individually:
    # *Name, price and url (and whether this requires the addition of the Tiki url to make complete it)
    # *Discount
    # *TikiNow availability
    # *The "Badge Under Price" price guarantee
    # *Whether this is a "hot price" 
    # *The number of reviews, number of stars and gifts.

    for product in products:
        try:
            name = product.find('div', {'class':'name'}).text
            if name[0:2] == 'Ad':                                                   #product name
                name = name[2:]
            price = product.find('div', {'class':'price-discount__price'}).text     #price
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
                reviews = product.find('div', {'class':'review'}).text[1:-1]  
            else:
                reviews = 'Not available'

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

from google.colab import files
result.to_csv('result.csv') 
files.download('result.csv')