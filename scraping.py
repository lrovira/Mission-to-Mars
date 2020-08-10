# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
# Set the executable path and initialize the chrome browser in splinter
# executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
# browser = Browser('chrome', **executable_path)
# create a function to initiate the browser
def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=False)
    # set our news title and paragraph variables
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "mars_hemi_images": hemi_fuction(browser),
        "facts": mars_facts(browser),
        "last_modified": dt.datetime.now()
    }
    # Stop webdriver and return data
    browser.quit()
    return data
def mars_news(browser):
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_p
# ### JPL Space Images Featured Images
def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()
    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()
    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    return img_url
def hemi_fuction(browser):
    # Visit URL
    url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # Parse the resulting html with soup
    html = browser.html
    hemisphere_dict={'title': [],'img_url_hem':[]}
    list_of_dicts=[]
    for i in range(4):
        browser.find_by_css('a.product-item h3')[i].click()
        hemi_html=browser.html
        hemi_soup=BeautifulSoup(hemi_html, 'html.parser')
        title=hemi_soup.find('h2').text
        img_url_hem=hemi_soup.find('a', text='Sample').get('href')
        hems_dictionary={'title':title, "img_url_hem": img_url_hem}
        list_of_dicts.append(hems_dictionary)
        browser.back()
    return list_of_dicts
### Mars Facts
def mars_facts(browser):
    url='https://space-facts.com/mars/'
    browser.visit(url)
    facts_html=browser.html
    facts_soup=BeautifulSoup(facts_html,'html.parser')
    title_facts=facts_soup.findAll('table', {'class':"tablepress-id-p-mars"})
    # text="tablepress-id-p-mars")
    # tables = parsedHTMlPage.findAll('table',{'class':'wikitable'})# facts_dictionary={'title':title, }
    # att={"id":"tablepress-p-mars", ''}
    # Add try/except for error handling
    # try:
        # Use 'read_html' to scrape the facts table into a dataframe
        # df = pd.read_html('https://space-facts.com/mars/', attrs={"id":"tablepress-p-mars"})[0]
    # except BaseException as e:
        # return None
        # print(e)
    # Assign columns and set index of dataframe
    facts_list=[]
    for table in title_facts:
        for tr in table.findAll('tr'):
            col1=tr.findAll('td', {'class':'column-1'})
            col2=tr.findAll('td', {'class':'column-2'})
            temp={"description":col1[0].text, "value":col2[0].text}
            facts_list.append(temp)
            #get back in dataframe
            dict_to_df=pd.DataFrame(facts_list)
        # df.columns=['Description', 'Mars', 'Earth']
        # df.set_index('Description', inplace=True)
        # Convert dataframe into HTML format, add bootstrap
        # return df.to_html(classes="table table-striped")
    return dict_to_df
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())