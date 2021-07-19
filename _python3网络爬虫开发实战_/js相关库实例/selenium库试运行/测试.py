"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
class Selenium_firefox():
    @retry(stop_max_attempt_number=3)
    def __init__(self):
        # 设置输出内容目录
        # 下载无弹窗
        path = "F://firefox/Download"
        if not os.path.exists(path):
            os.makedirs(path)
        profile = webdriver.FirefoxProfile()
        # profile.set_preference('browser.download.folderList', 2)
        # logging.info('运行支持')

        profile.set_preference('browser.download.dir', path.strip('\u202a'))
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip,application/octet-stream')
        # 无图
        profile.set_preference('browser.migration.version', 9001)
        profile.set_preference('permissions.default.image', 2)
#        profile.set_preference('user-agent', u()['User-Agent'])


        ops = Options()
        ops.add_argument('--headless')
        ops.add_argument('disable-infobars')
        #capa = DesiredCapabilities.FIREFOX
        #capa["pageLoadStrategy"]="none"
        """网页获取"""
        self.browser = webdriver.Firefox(profile)
        self.wait = WebDriverWait(self.browser, 10,0.1)
        self.browser.get('https://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?pageId=3db4fb747da9705a88f1cbc0ee1e3287&s8=02')
    @retry(stop_max_attempt_number=3)
    def login(self):
        """登录"""
        # 切换框架
        self.browser.refresh()
        wait = self.wait
        frame = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="contentIframe"]')))
        self.browser.switch_to.frame(frame)
        click = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#phoneNumber')))
        click.send_keys("18373281350")
        time.sleep(1)
        click1 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.ng-invalid')))
        click1.send_keys("cao43100~")
        time.sleep(1)
        button_login = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.custom-button')))
        button_login.click()
        time.sleep(1)
        button_login2 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.custom-button')))
        button_login2.click()
        # 必须加上表单退出，否者就是死元素无法定位
        self.browser.switch_to.default_content()
        # 新版改变，导致无法直接进入刑事
        #click1 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.advenced-search')))  # /html/body/div/div[3]/diy:lawyee/div/div[1]/div[1]
        #click1.click()



    def content_change(self,country, index_, keyword):
        wait =self.wait
        self.login()
        """优化为发送country：高级检索 """
        #self.browser.switch_to.window(self.browser.window_handles[1])
        self.browser.refresh()
        click1 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.advenced-search')))#/html/body/div/div[3]/diy:lawyee/div/div[1]/div[1]
        click1.click()
        # 判决结果检索
        #keyword_select = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qbType"]')))
        #keyword_select.click()
        #select = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qwTypeUl"]/li[7]')))
        #select.click()
        send_ = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qbValue"]')))
        send_.clear()
        send_.send_keys(keyword)
        # country限定
        send1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="s2"]')))  # //div[@class ="search-wrapper clearfix"]/div[@class =
        # "search-middle"]/input全文输入
        send1.send_keys(country)
        button_1 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchBtn"]')))
        button_1.click()
        """文书数量：15"""

        button_ = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.pageSizeSelect')))
        button_.click()
        # time.sleep(1)
        button_ = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.pageSizeSelect > option:nth-child(3)')))
        button_.click()
        # 刷新一下
        #self.browser.refresh()

        #except TimeoutException as e:
            #print("没有检索到裁判文书而导致元素找不到")
        """目的：减少遍历次数，进行页数遍历"""

        condition = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="_view_1545184311000"]/div[1]/div[2]/span')))
        #print(condition.text)  # 不能直接//text()原因不明
        conditions = math.ceil(int(condition.text) / 15)  # 最长12，最短6
        # print(conditions)
        if int(condition.text) == 0:
            self.browser.close()
        elif int(conditions) > 40:  # condition本身已经除了15
            with open( './第三次超过600页.txt', 'a+', encoding='utf-8')as file:
                file.write( '出现超过600条的裁判文书,其所在区域为：' + str(country) + '，其数量为：' + str(condition.text) + str(keyword) + '\n')
        else:
            for index in range(conditions):
                for i in range(3, 18):
                    #print(i)
                    k = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="_view_1545184311000"]/div[i]/div[2]/h4/a'))).get_attribute("textContent")
                    print(k)
                    casename = self.browser.find_element_by_xpath('//text()').text
                    print(casename)
                    caseurl = self.browser.find_element_by_xpath(
                        '//*[@id="_view_1545184311000"]/div[i]/div[2]/h4/a').get_attribute("href")
                    court = self.browser.find_element_by_xpath(
                        '//*[@id="_view_1545184311000"]/div[i]/div[3]/span[1]').text
                    casenumber = self.browser.find_element_by_xpath(
                        '//*[@id="_view_1545184311000"]/div[3]/div[3]/span[2]').text
                    times = self.browser.find_element_by_xpath(
                        '//*[@id="_view_1545184311000"]/div[3]/div[3]/span[3]').text
                    reason = self.browser.find_element_by_xpath('//*[@id="_view_1545184311000"]/div[3]/div[4]/p').text
                    message = {"案例名称": casename, "案例url": caseurl, "法院": court, "案例号": casenumber, "判决日期": times,
                               "裁判理由": reason}

                    dataframes = pd.DataFrame(message)
                    output = os.path.dirname(__file__)
                    print(output)
                    writer = pd.ExcelWriter(output + r"案例详情.xls".format(name=title))
                    dataframes.to_excel(writer, sheet_name='公司', index=False)
                    writer.save()

