# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time

def scrape():
    return{
        "mars_title": findNews(),
        "mars_paragraph": findPar(),
        "mars_image": findImage(),
        "mars_weather": findTweet(),
        "mars_facts": marsFacts(),
        "mars_hemispheres": marsHemispheres()
    }


def findNews():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #Scrape the NASA Mars News Site and collect the latest News Title
    news_title = soup.find('div', class_="image_and_description_container").h3.text
    browser.quit()
    return(news_title)
    

def findPar():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #Scrape the NASA Mars News Site and collect the latest News Paragraph Text
    news_p=soup.find('div', class_="article_teaser_body").text
    browser.quit()
    return(news_p)

def findImage():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    #Use splinter to navigate the site and find the image url for the current Featured Mars Image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    browser.click_link_by_partial_text('FULL IMAGE')
    #scrape featured image
    url = 'https://www.jpl.nasa.gov'+soup.find('a', class_="button fancybox").get("data-link")
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image_url = "https://www.jpl.nasa.gov" +soup.find('figure', class_='lede').a.img.get('src')
    browser.quit()
    return(featured_image_url)

def findTweet():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather = soup.body.find('div',{"class":["css-901oao","r-hkyrab","r-1qd0xha","r-a023e6","r-16dba41","r-ad9z0x","r-bcqeeo","r-bnwqim","r-qvutc0"]}, lang='en').find('span', {"class":["css-901oao","css-16my406","r-1qd0xha","r-ad9z0x","r-bcqeeo","r-qvutc0"]}).text
    browser.quit()
    return(mars_weather)
    
def marsFacts():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    mars_facts_df = pd.read_html(html)
    mars_facts_df = mars_facts_df[0].rename(columns={0:'Description',1:'Value'})
    mars_facts_df.to_html("Mars_Facts.html")
    browser.quit()
    return(mars_facts_df.to_html)

def marsHemispheres():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title_list = []
    img_url_list = []
    for name in soup.body.find_all('h3'):
        title_list.append(name.text)
        browser.click_link_by_partial_text(name.text[0:6])
        time.sleep(1)
        browser.click_link_by_partial_text('Sample')
        browser.windows[1].is_current=True      
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')        
        img_url_list.append(soup.img.get('src'))
        browser.windows[1].close()
        browser.back()
        time.sleep(1)
    hemisphere_image_urls =[]
    for i in range(0,4):
        myDict = {"title":title_list[i],"img_url":img_url_list[i]}
        hemisphere_image_urls.append(myDict)
    browser.quit()
    return(hemisphere_image_urls)

