from splinter import Browser
from bs4 import BeautifulSoup as bs


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    #Open the web browser
    browser.visit('https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest')
    #Create the soup 
    soup=bs(browser.html,'lxml')
    #find the classes
    news=soup.find('div',class_='list_text')
    #Assign the variables value
    headline= news.find('div',class_='content_title').text
    paragraph= news.find('div',class_='article_teaser_body').text



    #Open the web browser
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    #click on the picture
    browser.find_by_xpath('//*[@id="full_image"]').click()
    #click to make it bigger
    browser.find_by_xpath('//*[@id="fancybox-lock"]/div/div[1]/a[3]').click()
    #create the soup
    soup=bs(browser.html,'html.parser')
    #extraxt the picture url
    image=soup.find('div',class_='fancybox-inner fancybox-skin fancybox-dark-skin fancybox-dark-skin-open')
    image = image.find('img',class_='fancybox-image')
    image = image['src']
    main='https://www.jpl.nasa.gov'
    img_url=f"{main}{image}"

    #Open the web browser
    browser.visit('https://twitter.com/marswxreport?lang=en')
    #check uf the element is present 
    browser.is_element_present_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div/div/div/div[2]/section/div/div/div/div[1]/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]/div/span')
    #create the soup
    soup=bs(browser.html,'html.parser')
    #go for the tweet
    tweet = soup.find('div',class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
    tweet =tweet.find('span',class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text

    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    hemisphere_image_urls =[]
    for i in range(1,5):
        soup=bs(browser.html,'html.parser')
        image_head=soup.find_all('div',class_='description')[i-1]
        image_head=image_head.find('h3').text
        browser.find_by_xpath(f'//*[@id="product-section"]/div[2]/div[{i}]/div/a').click()
        browser.find_by_xpath('//*[@id="wide-image-toggle"]').click()
        soup=bs(browser.html,'html.parser')
        image_link=soup.find('img',class_='wide-image')['src']
        main_url='https://astrogeology.usgs.gov'
        image_link=f"{main_url}{image_link}"
        image_dict={
            'title':image_head,
            'link':image_link
        }
        hemisphere_image_urls.append(image_dict)
        browser.back()

    dict_mars_new={ 
        'headline':headline,
        'paragraph':paragraph,
        'url_image':img_url,
        'tweet':tweet,
        'pictures':hemisphere_image_urls
    }



    browser.quit()

    return dict_mars_new


    