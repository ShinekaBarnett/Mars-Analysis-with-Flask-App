# BeautifulSoup, Pandas, and Requests/Splinter
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import time 

# Check for chrome web driver path
# !which chromedriver

# Create Browser instance and pass 'chrome' string
def init_Browswer():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless = False)

def scrape():
    browser = init_Browswer()
    # Assign news url to variable
    news_url= "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(news_url)

    time.sleep(3)

    news_html = browser.html
    news_soup = BeautifulSoup(news_html, 'html.parser')

    # Pretty print 
    # print(news_soup.prettify())

    # NASA Mars News Scraping
    news_title = news_soup.body.find('div', class_='content_title').get_text()
    news_title

    news_p = news_soup.body.find('div', class_='article_teaser_body').get_text()
    news_p

    # Set image browser
    image_url= "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    time.sleep(3)

    image_html= browser.html
    image_soup = BeautifulSoup(image_html, 'lxml')
    # print(image_soup.prettify())

    # Set base url 
    base_url = 'https://www.jpl.nasa.gov'

    # Get featured image partial url
    image_url = image_soup.find("a", {"class":"button fancybox"})['data-fancybox-href']

    featured_image_url = base_url + image_url
    featured_image_url
    # print(featured_image_url)
    # print(base_url)

    # Mars Weather

    # Set weather browser 
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)

    time.sleep(3)

    weather_html = browser.html
    weather_soup = BeautifulSoup(weather_html, 'lxml')
    # print(weather_soup.prettify())                         

    # Get latest tweet about weather from twitter link 
    mars_weather = weather_soup.find('p', class_= "TweetTextSize").text.split(".")[0]
    mars_weather
    # print(mars_weather)

    # Mars Facts
    # Scrape second HTML table with pandas
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts_table = pd.read_html(mars_facts_url)
    mars_facts_table = mars_facts_table[1]
    # print(mars_facts_table)

    # Read table to pandas DataFrame
    mars_facts_df = mars_facts_table
    mars_facts_df.columns = ['Description', 'Value']
 



    # Convert to HTML table string
    mars_facts_html = mars_facts_df.to_html()
    mars_facts_html

    # Mars Hemisphere Browser
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars' 
    browser.visit(hemisphere_url)

    time.sleep(3)

    hemisphere_html = browser.html
    hemisphere_soup = BeautifulSoup(hemisphere_html, 'lxml')

    # Create list to hold list of links      
    links = []  

    # Create list to hold img urls
    hemisphere_image_urls = []    

    # Store base url in a variable for concatenation
    base_url = "https://astrogeology.usgs.gov" 

    result = hemisphere_soup.find('div', class_='result-list')
    result

    items = result.findAll('div', class_ = 'item')
    items

    #loop through divs
    for item in items:
        # Create dictionary to append list of images
        hemisphere = {} 
        
        content = item.find('div', class_='description')
        
        title = content.find('h3').text
        hemisphere['title'] = title
        
        href = item.find('a', {"class":"itemLink product-item"})['href']
        links.append(base_url + href)
        
    #loop through links
        for link in links:
            response = requests.get(link)
            hemisphere_soup = BeautifulSoup(response.text, 'lxml')

            img_src = hemisphere_soup.find("img", {"class":"wide-image"})['src']
            image_url = base_url + img_src
            hemisphere['img_url'] = image_url
            
        hemisphere_image_urls.append(hemisphere)
        
    hemisphere_image_urls

    mars= {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()

    return mars