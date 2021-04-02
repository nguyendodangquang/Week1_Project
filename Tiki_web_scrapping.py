from bs4 import BeautifulSoup
import requests, time

url = 'https://tiki.vn/laptop-may-vi-tinh/c1846?page=1&src=c.1846.hamburger_menu_fly_out_banner'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
r = requests.get(url, headers=headers)
lis = []

soup = BeautifulSoup(r.text, 'html.parser')
print(soup.prettify()[:1000])

main = soup.find('div', {'data-view-id':'product_list_container'})
print(main.prettify())
products = main.find_all('a', {'class':'product-item'})
for product in products:
    name = product.find('div', {'class':'name'}).text
    price = product.find('div', {'class':'price-discount__price'}).text
    img = product.img['src']
    purl = product['href']
    if product.find('div', {'class':'price-discount__discount'}):
        discount = product.find('div', {'class':'price-discount__discount'}).text
    if product.find('div', {'class':'item'}):
        tikinow = product.find('div', {'class':'item'}).img['src']
    if product.find('div', {'class':'badge-under-price'}).img:
        badge = product.find('div', {'class':'badge-under-price'}).img['src']
    if product.find('div', {'class':'badge-benefits'}).img:
        zero = product.find('div', {'class':'badge-benefits'}).img['src']
    if product.find('div', {'class':'review'}).text:
        reviews = product.find('div', {'class':'review'}).text
    if product.find('div', {'class':'rating__average'})['style']:
        stars = product.find('div', {'class':'rating__average'})['style']
    # if product.find('div', {'class':'freegift-list'}):
    #     gift = product.find('div', {'class':'freegift-list'}).img['src']

# To-do: go to each page
# To-do: Use sleep to fake out
# To-do: make a table of data

        