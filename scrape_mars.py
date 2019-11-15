
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
from selenium import webdriver
import time 

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless = False)
  
def scrape():
    browser = init_browser()
    mars_data = {}

    # NASA MARS NEWS

    news_url = "https://mars.nasa.gov/news/"
    
    browser.visit(news_url)
 
    html = browser.html
    news_soup = bs(html, "html.parser")
    
    news_title = news_soup.find("div", class_ = "content_title").text.strip()
    
    news_p = news_soup.find("div", class_ = "rollover_description_inner").text.strip()
    
    mars_data["news_title"] = news_title
    mars_data["news_para"] = news_p

    # JPL MARS SPACE IMAGES 
    
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    
    browser.visit(image_url)
    browser.visit(image_url)
    browser.find_by_text("FULL IMAGE")
    browser.find_by_text("more info")

    image_html = browser.html
    image_soup = bs(image_html, "html.parser")
    featured_img_url_raw = image_soup.find("div", class_="carousel_items").find("article")["style"]
    featured_img_url = featured_img_url_raw.split("'")[1]
    featured_img_url = ("https://www.jpl.nasa.gov"+ featured_img_url)
        
    mars_data["featured_img"] = featured_img_url

    # MARS WEATHER
    
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    
    tweet_html = requests.get(tweet_url)
    
    tweet_soup = bs(tweet_html.text, "html.parser")
    
    mars_weather = tweet_soup.find("p", class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip()
    
    mars_data["weather"] = mars_weather

    # MARS FACTS
    
    facts_url = "http://space-facts.com/mars/"

    facts_table = pd.read_html(facts_url)
    facts_df = facts_table[0]
    facts_df.columns = ["Attribute", "Values"]
    facts_df.set_index("Attribute", inplace = True)
    facts_df

    facts_table = facts_df.to_html()
    facts_table = facts_table.replace("\n", "")
    
    
    mars_data["facts_table"] = facts_table
    

    # MARS HEMISPHERES

    hemisphere_img_urls = []
    hemisphere_dict = {"title": [] , "img_url": []}

    hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hem_url)
    time.sleep(1)

    hem_html = browser.html
    hem_soup = bs(hem_html, "html.parser")
    results = hem_soup.find_all("h3")

    for result in results:
        raw_title = result.text
        title = raw_title[:-9]
        browser.click_link_by_partial_text(raw_title)
        time.sleep(1)
        img_url = browser.find_link_by_partial_href("download")["href"]
        print(img_url)
        hemisphere_dict = {"title": title, "img_url": img_url}
        hemisphere_img_urls.append(hemisphere_dict)
        time.sleep(1)
        browser.visit(hem_url)

    mars_data["hemi_imgs"] = hemisphere_img_urls

    return mars_data