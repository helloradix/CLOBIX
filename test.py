from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import os
import time
import urllib.request

if __name__=="__main__":

    # 찾고자 하는 검색어를 url로 만들어 준다.
    searchterm = '다현 사진'
    url = "https://www.google.com/search?q=" + searchterm + "&source=lnms&tbm=isch"
    # chrom webdriver 사용하여 브라우저를 가져온다.
    browser = webdriver.Chrome('/Users/iotpc/Downloads/chromedriver.exe')
    browser.get(url)

    # User-Agent를 통해 봇이 아닌 유저정보라는 것을 위해 사용
    header = {
        #'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
        'User-Agent': "Chrome/76.0.3809.132"}
    # 이미지 카운트 (이미지 저장할 때 사용하기 위해서)
    counter = 0
    fail_count = 0
    succounter = 0

    print(os.path)
    # 소스코드가 있는 경로에 '검색어' 폴더가 없으면 만들어준다.(이미지 저장 폴더를 위해서)
    if not os.path.exists(searchterm):
        os.mkdir(searchterm)

    for _ in range(500):
        # 가로 = 0, 세로 = 10000 픽셀 스크롤한다.
        browser.execute_script("window.scrollTo(0, 50000)")
        try:
            browser.find_element_by_id("smb").click()
        except:
            print("Read more ... button not found this page")
        # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # div태그에서 class name이 rg_meta인 것을 찾아온다
    for x in browser.find_elements_by_xpath('//div[contains(@class,"rg_meta")]'):
        counter = counter + 1
        print("Total Count:", counter)
        print("Succsessful Count:", succounter)
        print("URL:", json.loads(x.get_attribute('innerHTML'))["ou"])

        # 이미지 url
        img = json.loads(x.get_attribute('innerHTML'))["ou"]
        # 이미지 확장자
        imgtype = json.loads(x.get_attribute('innerHTML'))["ity"]

        urls = json.loads(x.get_attribute('innerHTML'))["ou"]
        savename = str(counter)+".jpg"
        try:
            urllib.request.urlretrieve(urls, savename)
            succounter += 1
            if counter == 600:
                break;
        except:
            print("get img failed")
            fail_count += 1
            continue

    print(succounter, "succesfully downloaded")
    print(fail_count, "failed to downloaded")
    browser.close()