from splinter import Browser
from bs4 import BeautifulSoup as bs
import pymongo
import pandas as pd
import time


def init_browser():

    executable_path = {"executable_path":"/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    return browser

def scrape():

    browser = init_browser()
    # collection.drop()

# NASA News Scrape
    

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(3)

    news_html = browser.html
    news_soup= bs(news_html, "html.parser")

    news_title = news_soup.find("div", class_= "list_text").find("div", class_= "content_title").text
    # news_title

    news_p = news_soup.find("div", class_= "list_text").find("div", class_= "article_teaser_body").text
    # news_p
    # print(news_p)

    # browser.quit()

## Mars Featured Image Scrape

    # browser = init_browser()
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    time.sleep(5)

    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(3)

    img_html = browser.html
    img_soup = bs(img_html, "html.parser")

    image = img_soup.find("div", class_="fancybox-inner").find("img", class_="fancybox-image")["src"]
    image

    image_base = "https://www.jpl.nasa.gov"
    featured_image_url = image_base + image
    # featured_image_url

    # browser.quit()

# Mars Facts Scrape

    # browser = init_browser()

    url3 = "https://space-facts.com/mars/"
    browser.visit(url3)
    time.sleep(3)
    mars_table = pd.read_html(url3)
    # mars_table

    mars_facts = mars_table[0]
    mars_facts = mars_facts.set_index(0)
    mars_facts = mars_facts.rename(columns={1: "Mars"})
    mars_facts = mars_facts.to_html()
    mars_facts = mars_facts.replace("\n", "")
    mars_facts = mars_facts.replace("<th>0</th>", "<th>Description</th>")
    # mars_facts

    # browser.quit()

# Mars Hemisphere Images Scrape

    # browser = init_browser()
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    time.sleep(3)
    html = browser.html
    soup = bs(html, "html.parser")

    hemispheres = soup.find_all("div", class_="item")
    hemispheres

    img_urls = []
    img_titles = []

    for hemi in hemispheres:
        titles = hemi.find("h3").text
        browser.click_link_by_partial_text(titles)
        time.sleep(3)
        html = browser.html
        soup = bs(html, "html.parser")
        img_url = soup.find("div", class_="downloads").find("a")["href"]
        browser.back()
        data = {"title": titles,
                "image_url": img_url}
        img_urls.append(data)

    browser.quit()

    mars_update = {
                "News_Title": news_title,
                "News_Paragraph": news_p,
                "Featured_Image": featured_image_url,
                "Mars_Facts": mars_facts,
                "Hemisphere_Titles": img_titles,
                "Hemisphere_URLs":img_urls
                }

    # collection.insert(mars_update)

    return mars_update