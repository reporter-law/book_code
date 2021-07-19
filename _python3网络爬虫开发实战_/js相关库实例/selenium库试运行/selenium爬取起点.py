# -*-  coding: utf-8 -*-
# Author: xxx
# Datetime : 2019/12/12 10:25
# software: PyCharm
# usage:
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from lxml import etree
import pymongo
from tqdm import tqdm
from selenium.common.exceptions import TimeoutException


driver = webdriver.Firefox()
wait = WebDriverWait(driver,10)

def click_page(page):
    """

    :param page:
    :return:
    """
    try:
        input_1 = wait.until(EC.presence_of_element_located((By.ID, "PAGINATION-INPUT")))
        input_1.clear()
        input_1.send_keys(page)
        button = driver.find_element_by_xpath('//*[@id="PAGINATION-BUTTON"]')
        time.sleep(1)
        button.click()
        return driver.page_source
    except TimeoutException:
        print('失败')

    #return driver.page_source#不用return进行解析直接执行下一个函数！！
    # element = browser.find_element_by_xpath('//*[@id="ctl00"]/table/tbody/tr[3]/td/table/tbody/tr/td/div/a[9]')
    # time.sleep(10)
    # 可能是在最后面，节点尚未出现
    # element.click()
    # print(browser.page_source)


#click_page(1)

    # browser.get('')
    # time.sleep(3)
    # browser.close()

def get_browser_text(html):
    """获取内容"""
    #print('ok')#确实可以这样执行函数！即前一个函数嵌套下一个函数。是不是选项卡没有跳转过来
    #driver.switch_to.window(driver.window_handles[2])
    #title = driver.find_element_by_xpath('/html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]/div[2]/h4/a').text
    #print(title)
    '''首先要进行返回html'''
    try:
        #texts = driver.find_elements_by_xpath('/html/body/div[1]/div[5]/div[2]/div[2]/div/ul')
        #print(texts)#不是不能对xpath进行遍历，TypeError: 'WebElement' object is not iterable，而是element必须为elements
        html = etree.HTML(html)
        notget = html.xpath('/html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li[1]')#属性限定，防止上海网警
    #print(type(notget))#<class 'list'>
    #print(notget)
        for texts in notget:
        #print(type(texts)) <class 'lxml.etree._Element'>
            story = {'titles' : texts.xpath('//div/h4/a/text()'),
                    'authors' :texts.xpath('//div/p[@class="author"]/a/text()'),
        #假设不用按序选择？可以，有些不在a中,直接在p中也不行，因为没有选中
        #没有a少掉连载状态
                    'intros' : texts.xpath('//div/p[@class="intro"]/text()')
                         }
            #print(story)
            print(type(story))
            return story
        #print(type(titles))<class 'list'>
        #for title in titles:
        #print(type(title))<class 'lxml.etree._ElementUnicodeResult'>
        '''由于是element,先将之作为字符串？'''#存在缩进的并排
        #print(type(intros))<class 'list'>
        #多了一段上海网警，但是不应该有
    except:
        print('获取失败')

#ValueError: too many values to unpack (expected 3),将没有zip的变量视为元组
#print(type(intro)) <class 'lxml.etree._ElementUnicodeResult'>

MONGO_URL ='localhost'
MONGO_DB ='qidian'
MONGO_COLLECTION = 'storys'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
#collection =
def save_to_mongo(story):
    #存至mongo
    #print('ok?')
    """result = db[MONGO_COLLECTION].insert(story)
    print(type(result))
    print(result)"""
    try:
        if db[MONGO_COLLECTION].insert_one(story):
            print('保存成功')
    except Exception:
        print('存储失败')
        #存储失败是由于result的插入导致的id重复


def main():
    driver.get('https://www.qidian.com')
    # 切换选项卡
    # driver.execute_script('window.open()')新开一个选项卡
    # print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[0])  # 选项卡切换

    # 动作链
    actions = ActionChains(driver)

    click_1 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/kehuan"]')))
    actions.move_to_element(click_1).send_keys("18373281350")
    time.sleep(3)
    # time.sleep(2)
    # actions.double_click(click_1)
    click_1.click()
    # print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[1])
    # cli = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/kehuan"]')))
    # cli.click()
    # print(browser.page_source)
    # browser.forward()

    # browser.get('https://www.qidian.com/kehuan')
    # browser.switch_to.frame('frame')
    cli_2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="//www.qidian.com/all?chanId=9"]')))
    # click = driver.find_element_by_css_selector('div>a[href="//www.qidian.com/rank?chn=9"]')
    # print(click)
    # actions.move_to_element(cli_2).perform()
    cli_2.click()  # 为什么找不到？根据上面情况，可能是节点选择错误，但是pyquery又找得到！似乎是iframe的缘故
    # print可以出来但是是非utf-8解码的
    # 可能程序仍在初始页面？
    # 是的，仍在初始页面_注释似乎不能在程序前面要债最开始？
    # 再次切换选项卡


    driver.switch_to.window(driver.window_handles[2])
    #若是放在前面导致需要不停切换选项卡
    for page in tqdm(range(1,6)):#不能从0开始
        time.sleep(2)
        html =click_page(page)
        story = get_browser_text(html)
        save_to_mongo(story)


main()
#通过之前requests这样函数分类也行
'''同样需要主函数'''
'''
总结：成功
1、数据结构问题
2、为了防止数据转化类型需要将数据提取放在数据结构中，list、dict中
3、数据库id不要重复，实验可以放在实验中单独做
'''