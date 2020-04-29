# Mission to Mars

![mission_to_mars](Images/mission_to_mars.png)

This web application scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.

## Scraping

The initial scraping is done by using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.

The Jupyter Notebook file called `mission_to_mars.ipynb` has all of the  scraping and analysis tasks.

### NASA Mars News

The latest News Title and Paragraph Text is scraped and collected from the [NASA Mars News Site](https://mars.nasa.gov/news/).

### JPL Mars Space Images - Featured Image

The url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars) is visited and Splinter is used to navigate the site and find the image url for the current Featured Mars Image.

### Mars Weather

The url for Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) is visited and the latest Mars weather tweet is scraped from the page.

### Mars Facts

The url for Mars Facts webpage [here](https://space-facts.com/mars/) is visited and Pandas is used to scrape the table containing facts about the planet including Diameter, Mass, etc. Pandas is also used to convert the data to a HTML table string.

### Mars Hemispheres

The url for USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) is visted and used to obtain high resolution images for each of Mar's hemispheres.

The image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name is saved and a Python dictionary is used to store the data using the keys.

- - -

## MongoDB and Flask Application

MongoDB with Flask templating is used to create a new HTML page that displays all of the information that was scraped from the URLs above.

The Jupyter notebook is converted into a Python script called `scrape_mars.py` with a function called `scrape` that executes all of the scraping code and returns one Python dictionary containing all of the scraped data.

The Template HTML file called `index.html` takes the mars data dictionary and displays all of the data in the appropriate HTML elements.
