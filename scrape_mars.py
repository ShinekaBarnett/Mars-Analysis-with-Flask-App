# BeautifulSoup, Pandas, and Requests/Splinter
from bs4 import BeautifulSoup
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import requests
from lxml import html 


# Create Browser instance and pass 'chrome' string
def browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

browser = browser()

def scrape():
    
    mars_data ={}

    news_url= "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(news_url)

    html = browser.html

    info_soup = BeautifulSoup(html, 'lxml')

    print(info_soup.prettify())

    # NASA Mars News Scraping

    def nasa_mars_news_title():
        latest_news_title = info_soup.body.find('div', class_='content_title').get_text()
        return latest_news_title 
    latest_title = nasa_mars_news_title()
    latest_title

    def nasa_mars_paragraph_text():
        latest_news_p = info_soup.body.find('div', class_='article_teaser_body').get_text()
        return latest_news_p 
    latest_news_p = nasa_mars_paragraph_text()
    latest_news_p

    # JPL Mars Space Images - Featured Image Scraping

    mars_url= "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_url)
    mars_html=browser.html
    mars_soup = BeautifulSoup(mars_html, 'lxml')
    browser.click_link_by_partial_text('FULL IMAGE')
    # print(mars_soup.prettify())

    base_url = 'https://www.jpl.nasa.gov'
    img_url = mars_soup.find("a", {"class":"button fancybox"})['data-fancybox-href']

    featured_img_url = base_url + img_url
    # print(featured_img_url)


    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    mars_weather_html = browser.html
    mars_weather_soup = BeautifulSoup(mars_weather_html, 'lxml')
    # print(mars_weather_soup.prettify())                         


    tweets= mars_weather_soup.find('div', class_="js-tweet-text-container")
    mars_weather = tweets.find('p', class_="js-tweet-text").text
    # print(mars_weather)   

    # Mars Facts

    # Read HTML to table
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts_table = pd.read_html(mars_facts_url)
    mars_facts_table = mars_facts_table[1]

    print(mars_facts_table)

    # Read table to pandas DataFrame
    mars_facts_df = mars_facts_table
    mars_facts_df.columns = ['Description', 'Value']
    mars_facts_df

    # Convert to HTML string
    mars_facts_html = mars_facts_df.to_html()
    print(mars_facts_html)


    # Mars Hemispheres
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars' 
    response = requests.get(hemisphere_url)
    hemisphere_soup = BeautifulSoup(response.text, 'lxml')

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    response = requests.get(url)

    hemisphere_soup = BeautifulSoup(response.text, 'lxml')
    links = []       
    hemisphere_img_urls = []    

    base_url = "https://astrogeology.usgs.gov"

    div_result = hemisphere_soup.find('div', class_='result-list')
    div_items = div_result.findAll('div', class_='item')

    for div_item in div_items:
        hemisphere = {}
        div_content = div_item.find('div', class_='description')
        
        title = div_content.find('h3').text
        hemisphere['title'] = title
        
        href = div_item.find('a', {"class":"itemLink product-item"})['href']
        links.append(base_url + href)

        for link in links:
            response = requests.get(link)
            hemisphere_soup = BeautifulSoup(response.text, 'lxml')

            img_src = hemisphere_soup.find("img", {"class":"wide-image"})['src']
            img_url = base_url + img_src
            hemisphere['img_url'] = img_url
            
        hemisphere_img_urls.append(hemisphere)
            
    for item in hemisphere_img_urls:
        print(item)

    mars_data = {
        "news_title" : latest_title,
        "paragraph_text": latest_news_p,
        "featured_img_url" : featured_img_url,
        "mars_weather" : mars_weather,
        "mars_facts" : mars_facts_table,
        "hemisphere_img_urls" : hemisphere_img_urls
    }

    browser.quit()

    return mars_data



