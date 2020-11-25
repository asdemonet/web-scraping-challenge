from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def init_browser():

    executable_path = {"executable_path":"/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    return browser

def scrape_mars():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(10)

    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.find("div", class_= "list_text").find("div", class_= "content_title").text
    news_title

    news_p = soup.find("div", class_= "list_text").find("div", class_= "article_teaser_body").text
    news_p

    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    time.sleep(10)

    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(5)

    html = browser.html
    soup = bs(html, "html.parser")

    image = soup.find("div", class_="fancybox-inner").find("img", class_="fancybox-image")["src"]
    image

    image_base = "https://www.jpl.nasa.gov"
    featured_image_url = image_base + image
    featured_image_url

    url3 = "https://space-facts.com/mars/"
    mars_table = pd.read_html(url3)
    mars_table

    mars_facts = mars_table[0]
    mars_facts = mars_facts.set_index(0)
    mars_facts = mars_facts.rename(columns={1: "Mars"})
    mars_facts = mars_facts.to_html()
    mars_facts = mars_facts.replace("\n", "")
    mars_facts


    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")

    hemispheres = soup.find_all("div", class_="item")
    hemispheres

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

    output = {"News_Title": news_title,
                "News_Paragraph": news_p,
                "Featured_Image": featured_image_url,
                "Mars_Facts": mars_facts,
                "Mars_Hemispheres": img_urls
                }
    return output
    




