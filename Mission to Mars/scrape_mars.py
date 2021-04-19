from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd


def scrape():
    #retrieve page with requests module

    executable_path = {'executable_path' : ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #create bs object
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    #MARS NEWS########################
    mars = {}
    #Latest News Title and Paragraph text
    mars['title'] = soup.find_all('div', class_='content_title')[0].text
    mars['paragraph'] = soup.find_all('div', class_='article_teaser_body')[0].text

    browser.quit()
    
    #MARS IMAGE########################
    executable_path = {'executable_path' : ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    #image url

    mars['featured_image_url'] = url + soup.find_all('img', class_='headerimage fade-in')[0]['src']
    browser.quit()
    
    #MARS TABLE
    url = 'https://galaxyfacts-mars.com/'
    mars_facts = pd.read_html(url, header=0)[0]
    mars['table_html'] = mars_facts.to_html()
    browser.quit()

    #Hemisphere URLs
    executable_path = {'executable_path' : ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    #mage url string for the full resolution hemisphere image, and the Hemisphere title containing 
    #the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title
    title=[]
    img_url=[]
    hemisphere_image_urls = []
    for x in range(0,4):
        browser.links.find_by_partial_text('Hemisphere')[x].click()
    
        html = browser.html
        soup = bs(html, 'html.parser')
        title.append(soup.find('h2', class_='title').text)
        img_url.append( url + soup.find('img', class_='wide-image')['src'])
        browser.visit(url)
        
        hemisphere_image_urls.append({f'Title' : title[x], f'img_url' : img_url[x]})

    
    browser.quit()

    mars['hemispheres'] = hemisphere_image_urls
    return mars