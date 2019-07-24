# BeautifulSoup, Pandas, and Requests/Splinter
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests

# Check for chrome web driver path
#get_ipython().system('which chromedriver')
# Create Browser instance and pass 'chrome' string

def scrape():
    mars_info = {}
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)

    # Set news browser
    news_url= "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(news_url)
    news_html = browser.html
    news_soup = BeautifulSoup(news_html, 'html.parser')

    # Pretty print 
    #print(news_soup.prettify())

    # NASA Mars News Scraping

    news_title = news_soup.body.find('div', class_='content_title').get_text()
    #print(news_title)

    news_p = news_soup.body.find('div', class_='article_teaser_body').get_text()
    #print(news_p)

    # Set image browser
    image_url= "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    image_html= browser.html
    image_soup = BeautifulSoup(image_html, 'html.parser')
    #print(image_soup.prettify())

    # Set base url 
    base_url = 'https://www.jpl.nasa.gov'

    # Get featured image partial url
    image_url = image_soup.find("a", {"class":"button fancybox"})['data-fancybox-href']

    featured_image_url = base_url + image_url
    #print(featured_image_url)

    # Mars Weather
    # Set weather browser 
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    weather_html = browser.html
    weather_soup = BeautifulSoup(weather_html, 'html.parser')
    #print(weather_soup.prettify())                         

    # Get latest tweet about weather from twitter link 
    mars_weather = weather_soup.find('p', class_= "TweetTextSize").text.split(".")[0]
    #print(mars_weather)

    # Mars Facts
    # Scrape second HTML table with pandas
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts_table = pd.read_html(mars_facts_url)
    mars_facts_table = mars_facts_table[1]
    #print(mars_facts_table)

    # Read table to pandas DataFrame
    mars_facts_df = mars_facts_table
    mars_facts_df.columns = ['Description', 'Value']
    mars_facts_df

    # Convert to HTML table string
    mars_facts_html = mars_facts_df.to_html()
    print(mars_facts_html)

    # Mars Hemisphere Browser
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars' 
    browser.visit(hemisphere_url)
    hemisphere_html = browser.html
    hemisphere_soup = BeautifulSoup(hemisphere_html, 'html.parser')

    response = requests.get(hemisphere_url)
    links = []  # Create list to hold list of links      
    hemisphere_img_urls = []    # Create list to hold img urls

    base_url = "https://astrogeology.usgs.gov" # Store base url in a variable for concatenation

    div_result = hemisphere_soup.find('div', class_='result-list')

    div_items = div_result.findAll('div', class_ = 'item')

    for div_item in div_items:
        hemisphere = {} # Create dictionary to append list of images
        div_content = div_item.find('div', class_='description')
        
        title = div_content.find('h3').text
        hemisphere['title'] = title
        
        href = div_item.find('a', {"class":"itemLink product-item"})['href']
        links.append(base_url + href)

        for link in links:
            response = requests.get(link)
            hemisphere_soup = BeautifulSoup(response.text, 'html.parser')

            img_src = hemisphere_soup.find("img", {"class":"wide-image"})['src']
            img_url = base_url + img_src
            hemisphere['img_url'] = img_url
            
        hemisphere_img_urls.append(hemisphere)
        
    hemisphere_img_urls

    mars_info = {
        "title" : news_title,
        "paragraph": news_p,
        "image" : featured_image_url,
        "weather" : mars_weather,
        "facts" : mars_facts_table,
        "hemispheres" : hemisphere_img_urls
    }

    browser.quit()

    return mars_info