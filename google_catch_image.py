from urllib import request
from selenium import webdriver
import time 
import requests
import os

class GoogleCatchImage():
    def __init__(self):
        return
    def connect_page(self,url,bool_headless):
        if bool_headless:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            self.driver = webdriver.Chrome(options=options)
            self.driver.get(url)
        else:
            self.driver = webdriver.Chrome()
            self.driver.get(url)
    def download_images(self,keyword,round):
        pickpath = './data/'+ keyword
        if not os.path.exists(pickpath): os.makedirs(pickpath)
        img_url_dic = []
        count = 0
        pos = 0
        for i in range(round):
            pos += 500
            js = 'var q=document.documentElement.scrollTop=' + str(pos)
            self.driver.execute_script(js)
            time.sleep(1)
            img_elements = self.driver.find_elements_by_tag_name('img')
            for img_element in img_elements:
                img_url = img_element.get_attribute('src')
                if isinstance(img_url, str) and len(img_url)<=200 and 'images' in img_url and img_url not in img_url_dic:
                    try: 
                        img_url_dic.append(img_url)
                        filename = pickpath+"/" + str(count) + ".jpg"
                        r = requests.get(img_url)
                        with open(filename, 'wb') as f:
                            f.write(r.content)
                            f.close()
                        count += 1
                        print('this is ' + str(count) + 'st img')
                        time.sleep(0.2)
                    except:
                        print('failure')
    def close(self):
        try:
            self.driver.close()
            self.driver.quit()
        except Exception as e:
            print(e)
connect_page = GoogleCatchImage()
connect_page.connect_page("https://www.google.com.hk/search?q=%27+dog+%27&tbm=isch",False)
connect_page.download_images("dog", 1)
connect_page.close()
