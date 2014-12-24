# -*- coding: UTF-8 -*-
'''
Created on Dec. 23, 2014

@author: yilulu
'''

import unittest, ConfigParser, random, time, os, logging, MySQLdb
import traceback

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import HTMLTestRunner

from PO.base import Base
import login, new_course_management

class CourseTest(unittest.TestCase):

    def setUp(self):

        self.cfg_file = 'config.ini'
        self.cfg = ConfigParser.RawConfigParser()
        self.cfg.read(self.cfg_file)
        self.browser = self.cfg.get("env_para", "browser")
        self.org_name = self.cfg.get("env_para", "org_name")
        self.org_password = self.cfg.get("env_para", "org_password")
        self.user_name = self.cfg.get("env_para", "user_name")
        self.user_password = self.cfg.get("env_para", "user_password")
        self.base_url = self.cfg.get("env_para", "base_url")
        self.dbhost = self.cfg.get("env_para", "dbhost")

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

        self.driver.implicitly_wait(3)
        self.driver.maximize_window()
        self.driver.get(self.base_url)

        cookie1 = self.cfg.get('env_para', 'cookie1')
        if(cookie1 == 'no'):
            login.login_by_logindo(self.cfg, self.driver, self.base_url, self.org_name, self.org_password)
            self.cfg.set("env_para", "cookie1", str(self.driver.get_cookie('ASUSS')['value']))
            self.cfg.write(open(self.cfg_file, "w"))
           
            #本来还有一个叫RM的cookie，但是值都是rm不变所以不取了
            # path=/; domain=.ablesky.com
        else:
            self.driver.add_cookie({'name':'ASUSS', 'value':cookie1, 'path':'/', 'domain':'.ablesky.com'})
            self.driver.add_cookie({'name':'RM', 'value':'rm'})

	    # @unittest.skip("test")
    def test_release_normal_course(self):      
        ba = Base(self.driver)
        title = "course" + ba.rand_name()
        new_course_management.course_redirect(self.cfg, self.driver, self.base_url, course_title=title, course_price=10)
        
        rs = ba.is_element_present("link text", u"查看课程")
        filename = ba.save_screenshot()
        print "image:"+filename
        self.assertEqual(True, rs)

    # @unittest.skip("test")
    def test_release_three_video(self):
        ba = Base(self.driver)
        title = "coursethree" + ba.rand_name()
        new_course_management.course_redirect(self.cfg, self.driver, self.base_url, course_title=title)
        
        rs = ba.is_element_present("link text", u"查看课程")
        filename = ba.save_screenshot()
        print "image:"+filename
        self.assertEqual(True, rs)

    # @unittest.skip("test")
    def test_release_two_video(self):
        ba = Base(self.driver)
        title = "two_video" + ba.rand_name()
        new_course_management.course_redirect(self.cfg, self.driver, self.base_url, course_title=title, course_price=10)
        
        rs = ba.is_element_present("link text", u"查看课程")
        filename = ba.save_screenshot()
        print "image:"+filename
        self.assertEqual(True, rs)

    # @unittest.skip("test")
    def test_presaleclass(self):
        ba = Base(self.driver)
        title = "presaleclass" + ba.rand_name()
        new_course_management.class_redirect(self.cfg, self.driver, self.base_url, ctype=2, classname=title)

        course = self.driver.find_element("link text", title)
        #若发课成功了取出课程链接存入文件中供后面的购买流程用
        rs = False
        if course:
            rs = True
            self.cfg.set("env_para", "course_href1", course.get_attribute("href"))
            self.cfg.write(open(self.cfg_file, "w"))
        
        filename = ba.save_screenshot()
        print "image:"+filename

        self.assertEqual(True, rs)

    # @unittest.skip("test")
    def test_onlineclass(self):
        ba = Base(self.driver)
        title = "onlineclass" + ba.rand_name()
        new_course_management.class_redirect(self.cfg, self.driver, self.base_url, classname=title)

        # rs = ba.is_element_present("link text", title)
        course = self.driver.find_element("link text", title)
        #若发课成功了取出课程链接存入文件中供后面的购买流程用
        rs = False
        if course:
            rs = True
            self.cfg.set("env_para", "course_href2", course.get_attribute("href"))
            self.cfg.write(open(self.cfg_file, "w"))

        filename = ba.save_screenshot()
        print "image:"+filename
        self.assertEqual(True, rs)

    # @unittest.skip("test")
    def test_agency_course(self):
        ba = Base(self.driver)
        title = "agency" + ba.rand_name()
        new_course_management.release_agency_course(self.cfg, self.driver, self.base_url, course_title=title)

        rs = ba.is_element_present("link text", title)
        filename = ba.save_screenshot()
        print "image:"+filename
        self.assertEqual(True, rs)

    def tearDown(self): #在每个测试方法执行后调用，这个地方做所有清理工作
        self.driver.quit()