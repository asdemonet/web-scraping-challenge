#!/usr/bin/env python
# coding: utf-8

# In[4]:


from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


# In[6]:

def init_browser():

    executable_path = {"executable_path":"/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    return browser

# In[3]:
def scrape_mars():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(10)


    # In[4]:


    html = browser.html
    soup = bs(html, "html.parser")


    # In[5]:


    # print(soup.prettify())


    # In[6]:


    news_title = soup.find("div", class_= "list_text").find("div", class_= "content_title").text
    news_title


    # In[7]:


    news_p = soup.find("div", class_= "list_text").find("div", class_= "article_teaser_body").text
    news_p


    # In[69]:


    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    time.sleep(10)


    # In[70]:


    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(5)


    # In[71]:


    html = browser.html
    soup = bs(html, "html.parser")


    # In[72]:


    image = soup.find("div", class_="fancybox-inner").find("img", class_="fancybox-image")["src"]
    image


    # In[73]:


    image_base = "https://www.jpl.nasa.gov"
    featured_image_url = image_base + image
    featured_image_url


    # In[19]:


    url3 = "https://space-facts.com/mars/"
    mars_table = pd.read_html(url3)
    mars_table


    # In[20]:


    mars_facts = mars_table[0]
    mars_facts = mars_facts.set_index(0)
    mars_facts = mars_facts.rename(columns={1: "Mars"})
    mars_facts = mars_facts.to_html()
    mars_facts = mars_facts.replace("\n", "")
    mars_facts


    # In[7]:


    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")


    # In[8]:


    # hemispheres = soup.find("div", class_="collapsible-results")
    # hemispheres
    hemispheres = soup.find_all("div", class_="item")
    hemispheres


    # In[10]:


    img_urls = []

    for hemi in hemispheres:
        title = hemi.find("h3").text
        browser.click_link_by_partial_text(title)
        time.sleep(5)
        html = browser.html
        soup = bs(html, "html.parser")
        img_url = soup.find("div", class_="downloads").find("a")["href"]
        browser.back()
        data = {"title": title,
               "image_url": img_url}
        img_urls.append(data)


    # In[11]:


    img_urls



    # In[ ]:
    output = {"News_Title": news_title,
                "News_Paragraph": news_p,
                "Featured_Image": featured_image_url,
                "Mars_Facts": mars_facts,
                "Mars_Hemispheres": img_urls
                }
    return output
    
print(scrape_mars())



