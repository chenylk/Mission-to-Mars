#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import splinter and beautiful soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[2]:


#set the executable path and intialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# In[3]:


#visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
#optional delay for loading the page
browser.is_element_present_by_css('ul.item_list li.slide',wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


#use the parent element to find the fist 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


#use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images
# 

# In[8]:


# visit url
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)
    


# In[9]:


#find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[10]:


#find the more info button and clitck that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[11]:


#parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[12]:


#find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get('src')
img_url_rel


# In[13]:


img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# In[14]:


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns = ['description','value']
df.set_index('description',inplace=True)
df


# In[15]:


df.to_html()


# In[16]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[17]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

results = browser.find_by_css('a.product-item h3')
for i in range(len(results)):
    hemisphere = {}
    
    #find element on each loop to avoid a stale element exception 
    browser.find_by_css('a.product-item h3')[i].click()
    
    #find sample image anchor tag and extract href
    sample_element = browser.find_link_by_text('Sample').first
    hemisphere['img_url'] = sample_element['href']
    
    #get hemisphere title
    hemisphere['title'] = browser.find_by_css('h2.title').text
    
    #append the hemisphere_image_urls
    hemisphere_image_urls.append(hemisphere)
    
    browser.back()


# In[18]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[19]:


#5. Quit the browser
browser.quit()


# In[ ]:




