
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    #initiate headless driver for deployment
    browser = Browser('chrome', executable_path='chromedriver',headless=True)
    news_title, news_paragraph = mars_news(browser)
    hemisphere_data = mars_hemispheres(browser)
    #run all scraping functions and store results in dictionary
    data = {
        'news_title':news_title,
        'news_paragraph':news_paragraph,
        'featured_image':featured_image(browser),
        'facts':mars_facts(),
        'last_modified': dt.datetime.now(),
        'hemispheres':hemisphere_data
    }

    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    
    except AttributeError:
        return None, None


    return news_title, news_p

# ## JPL Space Images Featured Image

def featured_image(browser):
    
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # find the relative image url
    try:
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

# ## Mars Facts

def mars_facts():
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
        df.head()
    except BaseException:
        return None

    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    return df.to_html()

def mars_hemispheres(browser):
    
    #visit url
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url) 

    #find and click the hemisphere picture to retrieve jpg image to store in list
    hemisphere_image_urls = []

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
    
    #return the list of dictionaries
    return hemisphere_image_urls


if __name__ == "__main__":
    #if running as script print scraped data
    print(scrape_all())