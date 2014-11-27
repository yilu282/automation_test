# -*- coding: UTF-8 -*-
'''
Created on Sep. 24, 2012

@author: yilulu
'''
import unittest, ConfigParser, random, time, os, logging, MySQLdb
import traceback
from selenium import webdriver
import login, new_course_management, course_management, student_management, \
card_management, cate_management, admin_management, user_management, exam_paper, exam_questions, exam_cate_management
import exam_user_management
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import HTMLTestRunner


class Test(unittest.TestCase):
    
       

    def setUp(self):
        
        self.browser = "Chrome"
        cfg_file = 'config.ini'
        self.cfg = ConfigParser.RawConfigParser()
        self.cfg.read(cfg_file)
        self.verificationErrors = []
        self.org_name = self.cfg.get("env_para", "org_name")
        self.org_password = self.cfg.get("env_para", "org_password")
        self.user_name = self.cfg.get("env_para", "user_name")
        self.user_password = self.cfg.get("env_para", "user_password")
        self.base_url = self.cfg.get("env_para", "base_url")

        self.total = 0

        #一些回归过程中需要用到的变量
        #课程购买链接，跑发课流程时取的,后面购买课程需要用到
        self.course_href = ""
        self.course_href_2 = ""

        #一些使用卡相关变量，前置条件：管理员先创建卡，给变量赋值，用户才可获取卡号登录使用卡号
        #充值卡-卡号、密码
        self.p_card_num = 0
        self.p_card_pwd = 0
        #充课卡-卡号、密码
        self.c_card_num = 0
        self.c_card_pwd = 0
        #补课卡-卡号、密码
        self.ca_card_num = 0
        self.ca_card_pwd = 0
        #试听卡-考号、密码
        self.l_card_num = 0
        self.l_card_pwd = 0
        #考试卡-卡号
        self.examcard_num = 0

        #注册的时候会把第一个值赋给它
        self.import_name = ""

        if os.path.exists("C:\\test_rs_pic") != True:
                os.system("mkdir C:\\test_rs_pic")

        if self.browser == 'ie':
            self.driver = webdriver.Ie()
        elif self.browser == 'firefox':
            self.driver = webdriver.Firefox()
        elif self.browser == 'Chrome':
            chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
            os.environ["webdriver.chrome.driver"] = chromedriver
            self.driver = webdriver.Chrome(chromedriver)
        elif self.browser == "Html":
            self.driver = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.HTMLUNIT.copy())
        else:
            self.driver = webdriver.Ie()

        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        cookie1 = self.cfg.get('env_para', 'cookie1')
     
        if(cookie1 == 'no'):
            login.login_by_logindo(self.cfg, self.driver, self.base_url, self.org_name, self.org_password)
            self.cfg.set('env_para','cookie1',self.driver.get_cookie('ASUSS'))
            #本来还有一个叫RM的cookie，但是值都是rm不变所以不取了
        else:
            self.driver.add_cookie({'name':'ASUSS', 'value':cookie1})
            self.driver.add_cookie({'name':'RM', 'value':'rm'})

    def verify_course(self, title): #去课程中心检查是否存在
        
        self.driver.get(self.base_url + "myOffice.do")
        self.driver.find_element_by_link_text(u"教学教务").click()
        self.driver.find_element_by_link_text(u"课程管理").click()
        rs = self.is_element_present(By.LINK_TEXT, title)
        if rs == False:
            self.driver.find_element("name", "courseSearch").send_keys(title)
            self.driver.find_element("class name", "searchBtn").click()
            rs = self.is_element_present(By.LINK_TEXT, title)
        return rs


    def test_release_normal_course(self):

        rand_name = str(random.randint(1000, 9999))
        title = u"course" + rand_name#在标题中加入随机数字确保课件标题的唯一性
        try:
            new_course_management.course_redirect(self.cfg, self.driver, self.base_url, course_title=title, course_price=10)
            try:
                rs = self.verify_course(title)
                self.assertEqual(True, rs, "fail to release course!")
            except AssertionError, e:
                self.verificationErrors.append(str(e))
        except Exception, e:       
            print traceback.format_exc() 
        finally:
            self.driver.save_screenshot(r'C:/test_rs_pic/2_normal_course.png')
            print "image:C://test_rs_pic//2_normal_course.png"


        # self.normal_course = title#待用-在数据库中查是否转换失败

          
        #取链接待后面购买
        # course_href = self.driver.execute_script("return $(\"a:contains(\'"+title+"\')\").attr('href')")
        # time.sleep(1)
        # if course_href:
        #     self.course_href = self.base_url + course_href
        # else:
        #     self.course_href = ""

                   

    def tearDown(self): #在每个测试方法执行后调用，这个地方做所有清理工作
        self.driver.quit()
        # fail_num = len(self.verificationErrors)
        # print "total case:%s, %s failures.detail:%s"%(self.total, fail_num, self.verificationErrors)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    # unittest.main()
    testsuite = unittest.TestSuite()
    testsuite.addTest(Test("test_release_normal_course"))
    #file_name = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time())) + '.html'
    fp = file("my_report.html", 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                title='My unit test',
                description='This demonstrates the report output by HTMLTestRunner.'
                )

    # Use an external stylesheet.
    # See the Template_mixin class for more customizable options
    # runner.STYLESHEET_TMPL = '<link rel="stylesheet" href="my_stylesheet.css" type="text/css">'

    # run the test
    runner.run(testsuite)
