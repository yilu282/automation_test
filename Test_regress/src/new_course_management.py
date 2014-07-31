# -*- coding: UTF-8 -*-
'''
Created on Aug 12, 2013

@author: yilulu
'''
import re
import time
import login

def course_redirect(cfg, driver, base_url, ctype= 1, isthree=0, upload=1, course_file="", course_title=u"course",course_describe='hello world',course_tags='english\n',course_price=0):
    """
    ctype代表发课类型 1表示点播课程
    upload是发点播课程的时候需要用的，1是存储空间上传，2是本地上传
    isthree代表是不是发三分屏，1代表发三分屏，0代表发的是单视频
    本地上传没了，先留着不去掉了。
    如果是本地上传的话 course_file 是要上传文件的本地路径
    course_title 是要发的课程的课程标题
    course_describe 是课程信息页面的课程详情
    course_tags 标签
    course_price 价格 填0时为免费的课
    
    """
    #进入发课页面
    url = "%s/coursePostRedirect.do?action=courseStepOne"%(base_url)
    driver.get(url)
    driver.implicitly_wait(1)
    
    #发点播课程
    if ctype == 1:        
        #从存储空间上传
        if isthree == 1:#发三分屏
            driver.find_element(cfg.get('courseRedirect','threevideo_by'), cfg.get('courseRedirect','threevideo')).click()
            driver.find_elements(cfg.get('courseRedirect','upload_btn_by'), cfg.get('courseRedirect','upload_btn'))[1].click()
            time.sleep(3)
            driver.execute_script("$(\'.spacefile-name input\').last().click()")
            driver.execute_script("$(\'.dialog-button-container button\').eq(0).click()")
            time.sleep(1)
        
            driver.find_elements(cfg.get('courseRedirect','upload_btn_by'), cfg.get('courseRedirect','upload_btn'))[2].click()
            time.sleep(1)
            driver.execute_script("$(\'.spacefile-name input\').last().click()")
            driver.execute_script("$(\'.dialog-button-container button\').eq(0).click()")
            time.sleep(1)
            
        else:#单视频
            #存储空间上传
            if upload == 1:
                driver.find_element_by_css_selector("span.greenbtn30_text").click()
                time.sleep(3)
                
                #全选 /选最后一个         
                driver.execute_script("$(\'.spacefile-name input\').last().click()")
                #driver.find_element(cfg.get('courseRedirect','select_cfile_by'), cfg.get('courseRedirect','select_cfile')).click()
                
                driver.execute_script("$(\'.dialog-button-container button\').eq(0).click()")
                time.sleep(1)
            #本地上传
            else:        
                #把input显示出来才可以用否则会报当前元素不可见的错
                driver.execute_script("$('.fileinput-button input').eq(0).attr('style','height:20px;opacity:1;display:block;position:static;transform:translate(0px, 0px) scale(1)')")
                driver.implicitly_wait(1)
                input = driver.find_element_by_name("files").send_keys(course_file)
                time.sleep(1)

    driver.find_element(cfg.get('courseRedirect','next_btn_by'), cfg.get('courseRedirect','next_btn')).click()                                 
    #发课第二步-课程信息页面
    time.sleep(1)
    driver.find_element(cfg.get('courseRedirect','ctitle_by'), cfg.get('courseRedirect','ctitle')).click()
    driver.find_element(cfg.get('courseRedirect','ctitle_by'), cfg.get('courseRedirect','ctitle')).send_keys(course_title)
    #设置价格
    if course_price != 0:
        driver.find_element(cfg.get('courseRedirect','chanrge_by'), cfg.get('courseRedirect','chanrge')).click()
        driver.find_element(cfg.get('courseRedirect','price_by'), cfg.get('courseRedirect','price')).send_keys(course_price)            
    #填课程详情
    driver.execute_script("var element=window.document.getElementById('courseDesc-editor_ifr');\
    idocument=element.contentDocument;element=idocument.getElementById('tinymce');element.innerHTML =\'"+course_describe+"\';")
    time.sleep(1)
    #选择服务分类
    driver.execute_script("$(\'li.level2\').click()") 
    driver.execute_script("$(\'li.level3.selected\').click()") 
    time.sleep(1) 
    #填写课程标签
    driver.find_element(cfg.get('courseRedirect','tags_by'), cfg.get('courseRedirect','tags')).send_keys(course_tags)
    #完成
    driver.find_element(cfg.get('courseRedirect','done_btn_by'), cfg.get('courseRedirect','done_btn')).click()
    time.sleep(1)

def class_redirect(cfg, driver, base_url, classname='onlineclass', ctype=1, price=10, course_describe='hello world',course_tags='english\n'):
    '''
    ctype代表发课类型，1代表普通网络班（打包），2代表预售网络班
    '''
    driver.get("%smyOffice.do" %(base_url))
    driver.implicitly_wait(2)
    driver.find_element_by_link_text(u"教学教务").click()
    driver.implicitly_wait(2)
    driver.find_element_by_link_text(u"报班管理").click()
    driver.implicitly_wait(3)
    driver.find_element(cfg.get('classRedirect','redirect_btn_by'), cfg.get('classRedirect','redirect_btn')).click()

    if ctype == 1:
        #classname = "onlineclass"
        driver.find_element(cfg.get('classRedirect','select_course_by'), cfg.get('classRedirect','select_course')).click()
    else:
        driver.find_element_by_link_text(u"课程预售").click()
        time.sleep(2)
        #classname = "onlineclass-presale"
        driver.execute_script("$(\".comp-presell input\").eq(0).attr(\"checked\",\"checked\")")
        driver.find_element(cfg.get('classRedirect','presell_price_by'), cfg.get('classRedirect','presell_price')).send_keys(price)

    driver.find_element(cfg.get('classRedirect','classname_by'), cfg.get('classRedirect','classname')).send_keys(classname)
    driver.implicitly_wait(1)

    #填课程详情
    driver.execute_script("var element=window.document.getElementById('courseDescribe-editor_ifr');\
    idocument=element.contentDocument;element=idocument.getElementById('tinymce');element.innerHTML =\'"+course_describe+"\';")
    driver.find_element_by_css_selector("div.text-layer.clearfix > input[type=\"text\"]").send_keys(course_tags)
    #选择服务分类
    driver.execute_script("$(\'li.level2\').click()") 
    driver.execute_script("$(\'li.level3.selected\').click()") 
    driver.execute_script("$('.greenbtn25_text').click()")
    driver.implicitly_wait(2)

#发布代理课程-没有发布了现在代理人只能编辑代理的课程    
def release_agency_course(cfg, driver, base_url, course_title=u'代理课程'):
    
    driver.get("%smyOffice.do" %(base_url))
    driver.implicitly_wait(2) 
    driver.find_element_by_link_text(u"管理我申请的代理").click()
    driver.implicitly_wait(5)
    driver.find_element_by_link_text(u"管理课程").click()
    driver.implicitly_wait(5)
    driver.find_element_by_link_text(u"编辑").click()
    driver.implicitly_wait(2)
    driver.find_element(cfg.get('courseRedirect','agency_title_by'), cfg.get('courseRedirect','agency_title')).clear()
    driver.find_element(cfg.get('courseRedirect','agency_title_by'), cfg.get('courseRedirect','agency_title')).send_keys(course_title)
    
    try:
        str_price = driver.execute_script("return $('.ablableSNew .colorGreen').text()")
        temp = re.search(r'\d{1,10}.\d',str_price) 
        price = temp.group(0)
        print str_price, price
    
        driver.find_element(cfg.get('courseRedirect','agency_price_by'), cfg.get('courseRedirect','agency_price')).clear()
        driver.find_element(cfg.get('courseRedirect','agency_price_by'), cfg.get('courseRedirect','agency_price')).send_keys(price)
        driver.find_element(cfg.get('courseRedirect','agency_rank_by'), cfg.get('courseRedirect','agency_rank')).clear()
        driver.find_element(cfg.get('courseRedirect','agency_rank_by'), cfg.get('courseRedirect','agency_rank')).send_keys(100)
        driver.implicitly_wait(1)
    except Exception, e:#如果是免费的代理课程会在上面取价格的时候就会报错，免费的直接点发布即可
        pass
    finally:
        driver.find_element(cfg.get('courseRedirect','finish_btn_by'), cfg.get('courseRedirect','finish_btn')).click()
        driver.implicitly_wait(2)


def forsale_couse(driver, base_url):
    filepath = "W:\Testing\auto_test_file\headpic.jpg"
    driver.get(base_url + "myOffice.do")
    driver.implicitly_wait(2)
    driver.find_element_by_link_text(u"发布特惠课程").click()
    driver.implicitly_wait(3)
    driver.find_element_by_id("selectCourseBtn").click()
    driver.implicitly_wait(2)
    driver.find_element_by_xpath("//div[3]/div/div/table/tbody/tr/td[2]/em/button").click()
    driver.implicitly_wait(2)
    price = driver.execute_script("return $('#oldPrice').text()")
    driver.find_element_by_id("asprice_field").send_keys(price)
    driver.find_element_by_id("picFieldName-file").send_keys(filepath)
    driver.find_element_by_xpath("//div[3]/div/div/table/tbody/tr/td[2]/em/button").click()
    driver.find_element_by_id("total_field").send_keys("100")
    driver.find_element_by_id("preset_field").send_keys("0")
    driver.find_element_by_id("ext-gen48").click()