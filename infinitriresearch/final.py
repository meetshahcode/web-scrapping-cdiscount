#importing all necessary library
from selenium import webdriver
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import time

url = r"https://cdiscount.com/bricolage/climatisation/traitement-de-l-air/ioniseur/l-166130303.html"

#getting chrome driver
#please check the path
path = "infinitriresearch\chromedriver.exe"
driver = webdriver.Chrome(path);
#wait for few minitue 
driver.get(url);
#please solve captcha then continue.

ul = []
while True:
    time.sleep(2)
    content = driver.page_source
    soup = BeautifulSoup(content,'html.parser')
    ul = soup.find('ul', attrs= {'id':'lpBloc' , 'class':'lpGrid'})
    if ul:
        break

#only taking list item  which has data-sku attribute
items = [x for x  in ul.find_all('li') if x.has_attr('data-sku')]

#initialize list
id_ls = []
link_ls = []
names_ls = []
number_of_rating_ls =[]
c_discount_ls = []
free_delivery_ls = []
price_ls = []

#looping through each items
for item in items:

    #getting id
    id = item['data-sku']
    id_ls.append(id)

    #getting link
    link = item.find('a')['href']
    link_ls.append(link)

    #getting name
    names = (item.find('span',attrs={'class' : 'prdtTit'}))
    if names:
        name = names.contents[0]
        names_ls.append(name)
    else:
        names_ls.append('')

    #getting numbers of rating
    rating_band = (item.find('div',attrs={'class':'prdtBStar'}))
    number_of_rating = 0
    if rating_band:
        number_of_ratings = rating_band.find('span')
        if number_of_ratings:
            number_of_rating = number_of_ratings.contents[0]
    number_of_rating_ls.append(number_of_rating)

    #is c discount is available
    c_discount = False
    c_discounts_band = item.find('div',attrs={'class' : 'cdavZone'})
    if c_discounts_band:
        c_discounts = c_discounts_band.contents
        if c_discounts:
            if c_discounts[0]=='Eligible':
                c_discount = True
    c_discount_ls.append(c_discount)
    
    #is free delivery is available
    free_delivery_band = item.find('div',attrs={'class' : 'livraisonGratuite'})
    free_delivery = False
    if free_delivery_band:
        free_deliverys = free_delivery_band.contents
        if free_deliverys:
            if free_deliverys[1]=='Livraison gratuite':
                free_delivery = True
    free_delivery_ls.append(free_delivery)
    
    #getting price
    price_span = item.find('span',attrs={'class' : 'price priceColor hideFromPro'})
    price= 0
    if price_span:
        price_tag = price_span.contents
        if price_tag:
            price_text = (price_tag[0]).replace(",","")
            price = int(price_text[:-1])

    price_ls.append(price)

df = pd.DataFrame(
    {
        'Id':id_ls,
        'Link':link_ls,
        'Name':names_ls,
        'number of rating':number_of_rating_ls,
        'C discount':c_discount_ls,
        'Free delivery ls':free_delivery_ls,
        'Price in Euro':price_ls,
    }
) 
df.to_csv('products.csv', encoding='utf-8')