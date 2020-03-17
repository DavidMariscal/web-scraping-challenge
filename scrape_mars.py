#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Import Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time
from urllib.parse import urlsplit



# In[3]:

def init_browser():
    executable_path = {"executable_path":"/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless = False)

# mars_scraped_data = {}
# In[4]:

def scrape():
    browser = init_browser()
    mars_scraped_data = dict()
# assigning the url page
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(3)

# In[5]:


#using bs to write it into html
    html = browser.html
    soup = bs(html,"html.parser")


# In[6]:


    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    mars_scraped_data["news_title"] = news_title
    mars_scraped_data["news_paragraph"] = news_paragraph


# In[7]:


## JPL Mars Space Images - Featured Image


# In[8]:


# Get Mars Space Images through splinter module

# HTML Object 
    image_url_featured = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
    browser.visit(image_url_featured)
    time.sleep(3)
    html_image = browser.html
 

# Parse HTML with Beautiful Soup
    soup = bs(html_image, 'html.parser')

# Retrieve background-image url from style tag 
   # featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    featured_image_url= soup.find("img", class_="fancybox-image")["src"]
# Website Url 
    main_url = 'https://www.jpl.nasa.gov'

# Concatenate website url with scrapped route
    featured_image_url = main_url + featured_image_url

# Display full link to featured image
    mars_scraped_data["featured_image_url"] = featured_image_url


# In[11]:


## Mars Weather


# In[12]:


#Get mars weather's latest tweet from the website
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)


# In[14]:


    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')
    weather_tweet = []
# Retrieve all elements that contain news title in the specified range
# Look for entries that display weather related words to exclude non weather related tweets 
    for tweet in latest_tweets: 
       weather_tweet = tweet.find('p').text
       if 'sol' and 'pressure' in weather_tweet:
          print(weather_tweet)
          break
       else: 
          pass
  # Dictionary entry from Weather Tweet
    mars_scraped_data["weather_tweet"] = weather_tweet
# In[15]:


## Mars Facts


# In[16]:


    url_facts = "https://space-facts.com/mars/"


# In[17]:


# Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(url_facts)

# Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

# Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

# Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    # Save html code to folder Assets
    data = mars_df.to_html()

    # Dictionary entry 
    mars_scraped_data["mars_facts"] = data
 #   mars_df


# In[19]:


# In[20]:


## Mars Hemispheres


# In[30]:


    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)


# In[31]:


    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for item in items: 
        # Store title
        title = item.find('h3').text
        
        # Store link that leads to full image website
        partial_img_url = item.find('a', class_='itemLink product-item')['href']
        
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
        
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
        
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = bs( partial_img_html, 'html.parser')
        
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        

    # Display hemisphere_image_urls
        mars_scraped_data["hemisphere_image_urls"] = hemisphere_image_urls
        
        return mars_scraped_data

# In[ ]:




