"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
class Selenium_firefox():

    def __init__(self):
        # 设置输出内容目录
        # 下载无弹窗
        """网页获取"""
        ops = Options()
        ops.add_argument('--headless')
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20,0.1)
        self.path=os.path.dirname(__file__)

    def yzm(self,img):
    # 读取图片函数，注意client.general方法只能识别这种类型的数据，不可以直接用Image方法进行读取，否则会报错
        with open(img, 'rb') as f:
            img = f.read()
        print("已经收到，正在处理，请稍后....")
        # 百度ocr使用的id及密码
        app_id = '22219645'
        api_key = 'gRGCOwHFNjNLlNAscm9f7Bah'
        secret_key = 'YegeOmkQjPBDBpSzy12z1Z2PkLBRVzIV'
        client = AipOcr(app_id, api_key, secret_key)
        # 读取PIL处理后保存图片函数
        # 处理的是函数返回的，(as f: 什么返回的数据)
        dict1 = client.basicGeneral(img)
        # 讲得到的结果值打印，这里是字典格式的数据
        #print(dict1)
        try:
            return dict1["words_result"][0]["words"]
        except:
            pass

    def ip_loggin(self):
        self.browser.get('http://www.lawyee.org/')
        self.browser.maximize_window()
        wait = self.wait
        login = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div[1]/div[3]/div/div/a/span')))
        login.click()
        button= wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ip-btn"]')))
        button.click()
        time.sleep(1)
        """验证码截屏"""
        self.browser.save_screenshot(self.path+"\\全屏截图.png")
        src = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="RefreshValidate2"]')))
        #src=src.get_attribute("src")
        #print(src.location)
        #print(src.size)
        # 获取element的顶点坐标
        xPiont = src.location['x']
        yPiont = src.location['y']
        # 获取element的宽、高
        element_width = xPiont + src.size['width']
        element_height = yPiont + src.size['height']
        picture = Image.open(self.path+"\\全屏截图.png")
        picture = picture.crop((xPiont, yPiont, element_width, element_height))
        picture.save(self.path+"\\yzm.png")
        img = self.path+"\\yzm.png"
        text = self.yzm(img)
        print(text)
        """识别登录"""
        sendcap = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ValidateCode2"]')))
        sendcap.send_keys(text)
        go = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="yz-btn"]/img')))
        go.click()
