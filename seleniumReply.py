from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
import logging,time,logging.handlers,sys,codecs

WAIT_TIME = 2
FOLDER_PATH = r'C:\Users\gao_xiaolin\Desktop\reply\log' + '\\'
FILE_NAME = 'seleniumReply.log'

class chromeDriver:
    def __init__(self):
        #  加载profile，可以免登陆
        options = webdriver.ChromeOptions()
        userDir = r'C:\Users\gao_xiaolin\AppData\Local\Google\Chrome\User Data2'
        options.add_argument('--user-data-dir=' + userDir)
        #options.add_argument('--headless') #  会被百度发现，悲伤

        chrome_service = service.Service(executable_path = ChromeDriverManager().install())
        driver = webdriver.Chrome(service = chrome_service, options = options)
        self.driver = driver
        self.driver.maximize_window()
        self.driver.implicitly_wait(20) # 只需调用一次
        self.hasError = False

        '''
        #输出日志：因由python标准输出改为系统输出，将python标准输出行注释掉
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        rh = logging.handlers.RotatingFileHandler(
            FOLDER_PATH + FILE_NAME, 
            encoding='utf-8',
            mode = 'w',
            maxBytes=1000000,
            backupCount=3,
        )
        rh_formatter = logging.Formatter('%(asctime)s : %(levelname)s - %(filename)s - %(message)s')
        rh.setFormatter(rh_formatter)
        logger.addHandler(rh)
        self.logger = logger
        '''
    
    def reply(self,pageStr):
        try:
            #  访问页面
            self.driver.get(pageStr)
            
            #  输入回复
            time.sleep(WAIT_TIME)
            self.driver.find_element(By.ID, "ueditor_replace").click()
            writeReply ="document.getElementById('ueditor_replace').innerHTML='dd'" # java script
            self.driver.execute_script(writeReply)     

            #  提交回复
            time.sleep(WAIT_TIME)          
            buttonReply = 'document.querySelector("#tb_rich_poster > div.poster_body.editor_wrapper > div.poster_component.editor_bottom_panel.clearfix > div > a").click()' #  用javascript回复；具体代码可F12后右键复制为javascript代码
            self.driver.execute_script(buttonReply)     
            successStr = pageDic[pageStr] + ' 已顶帖'     
            print(successStr)
            #self.logger.debug(successStr) #  因由python标准输出改为系统输出，将python标准输出行注释掉
            
            
        except Exception as ex:
            print("ERROR:{}".format(ex))
            #self.logger.debug("ERROR:{}".format(ex))
            #failStr = pageDic[pageStr] + ' 未成功顶帖'
            #self.logger.debug(failStr) #  因由python标准输出改为系统输出，将python标准输出行注释掉
            self.hasError = True
        time.sleep(WAIT_TIME)

    def quit(self):
        #self.logger.handlers.clear()
        self.driver.quit()


#设置输出格式为utf-8
if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# 前三个是我的，后两个是阿睿的
pageDic = {'https://tieba.baidu.com/p/7836447213': '语c吧·第一性','https://tieba.baidu.com/p/7836243922':'宫斗吧·第一性', 'https://tieba.baidu.com/p/7977019554':'演绎吧·第一性','https://tieba.baidu.com/p/7762268308':'原创语c吧·第一性', 'https://tieba.baidu.com/p/7906257480':'语c吧·女孩乌托邦', 'https://tieba.baidu.com/p/7910096424': '演绎吧·女孩乌托邦'}

driver1 = chromeDriver()
for page in pageDic:
    if driver1.hasError:
        break  
    driver1.reply(page)

driver1.quit()




