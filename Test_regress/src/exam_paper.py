# -*- coding: UTF-8 -*-
'''
Created on Jul 23, 2014

@author: liwen
'''
import random, time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

from PO.exam_paper_page import ClickExamSystem, ExamInfoPage, QuestionInfoPage, PaperRecordPage, ScorePage
from PO.base import Base
from PO.random_exam_page import RandomExamPage
from PO.exam_student_page import ExamStudentListPage


def create_paper(cfg, driver, base_url, exam_name, exam_time,\
                  eoperation, erandom, eopen):
    """
    operation 代表考试时间结束后操作 0代表默认值，自动交卷
                                 1代表 继续答题
    random 代表试题是否随机排序  0代表 否，不随机排序
                             1代表 是，随机排序
    eopen 代表试卷是否对外开放   0 代表否，不对外开放
                             1代表对外开放
    """
    clickexamsystem = ClickExamSystem(driver,cfg)
    clickexamsystem.open_examsystem()
    
    examinfo = ExamInfoPage(driver,cfg)
    examinfo.create_paper()
    examinfo.input_exam_name(exam_name)
    examinfo.input_exam_time(exam_time)
    examinfo.whether_auto_commit(eoperation)
    examinfo.whether_random(erandom)
    examinfo.open_or_no(eopen)
    examinfo.click_next()    
    #添加大题
    auto_creatquestion(cfg, driver, 2)
    time.sleep(2)
    #生成试卷
    submit = QuestionInfoPage(driver,cfg)    
    submit.click_submit_btn()
    time.sleep(2)
    return exam_name   
            
#添加大题
def add_big_question(cfg, driver, qscore, qtype):
    """
    qtype表示大题类型，1=单选题，2=多选题，3=是非题，4=填空题，5=问答题，6=完型填空题，7=综合题
    """
    time.sleep(3)
    qinfo = QuestionInfoPage(driver,cfg)
    qinfo.add_big_question(qtype,qscore)
    qinfo.exam_import_question()
    time.sleep(3)
    
#自动添加题
def auto_creatquestion(cfg, driver, q_num):
    #typel = [1,2,3,4,5,6,7]
    for i in range(q_num):
        qscore = '5'
        qtype = random.randint(1, 7)
        #print qtype
        add_big_question(cfg, driver, qscore, qtype)
   
#随机组卷                        
def random_exam(cfg, driver, base_url, exam_name, exam_time,\
                  eoperation, erandom, eopen):
    clickexamsystem = ClickExamSystem(driver,cfg)
    clickexamsystem.open_examsystem()
    
    randompg = RandomExamPage(driver,cfg)
    randompg.click_random_btn()
    
    examinfo = ExamInfoPage(driver,cfg)
    examinfo.input_exam_name(exam_name)
    examinfo.input_exam_time(exam_time)
    examinfo.whether_auto_commit(eoperation)
    examinfo.whether_random(erandom)
    examinfo.open_or_no(eopen)
    
    auto_create_randomquestion(cfg, driver, 1)
    driver.find_element_by_css_selector("#question_select_1 > #combobox-container > div.cc-box > span.cc-arrow").click()
##    driver.find_element_by_css_selector("li.cc-item.selectedItem").click())
#    driver.find_element_by_css_selector("p.random-q-num-con > input.random-input").clear()
#    driver.find_element_by_css_selector("p.random-q-num-con > input.random-input").send_keys("9")
#    driver.find_element_by_css_selector("p.random-q-score-con > input.random-input").clear()
#    driver.find_element_by_css_selector("p.random-q-score-con > input.random-input").send_keys("5")
##    driver.find_element_by_id("add_random_btn").click()
##    driver.find_element_by_css_selector("#question_select_2 > #combobox-container > div.cc-box > span.cc-arrow").click()
##    driver.find_element_by_xpath("//div[5]/ul/li[2]").click()
##    driver.find_element_by_xpath("(//input[@type='text'])[14]").clear()
##    driver.find_element_by_xpath("(//input[@type='text'])[14]").send_keys("1")
##    driver.find_element_by_xpath("(//input[@type='text'])[15]").clear()
##    driver.find_element_by_xpath("(//input[@type='text'])[15]").send_keys("2")
##    driver.find_element_by_xpath("(//input[@type='text'])[16]").clear()
##    driver.find_element_by_xpath("(//input[@type='text'])[16]").send_keys("1")
    randompg.click_submit_btn()
    time.sleep(2)
    
    
    

#    driver.find_element_by_id("create_step_one").click()
    
#自动添加题
def auto_create_randomquestion(cfg, driver, q_num):
    #typel = [1,2,3,4,5,6,7]
    for i in range(q_num):
#        qscore = '5'
#        qtype = random.randint(1, 7)
        #print qtype
        add_randomq = RandomExamPage(driver,cfg)
        add_randomq.add_question_btn()
        time.sleep(2)
                          
#自动创建试卷
def auto_createpaper(cfg, driver, base_url, eoperation, \
                     erandom, eopen, q_num, exam_num, type):
    ba = Base(driver)
    for i in range(exam_num):
        exam_time = '120'
        if type==1:
            exam_name = 'testpaper_' + ba.rand_name()
            paper_name = create_paper(cfg, driver, base_url, exam_name, exam_time, \
                     eoperation, erandom, eopen)
        else:
            exam_name = 'random_p_' + ba.rand_name()
            paper_name = random_exam(cfg, driver, base_url, exam_name, exam_time,\
                  eoperation, erandom, eopen)
    return paper_name
        #print i      

def exam_result(cfg, driver, base_url, exam_name, etype=1, username=""):
    """
    etype表示需要的操作类型，1为导出分发给学员的试卷统计结果，
                             2为导出作为开放试卷的统计结果,
                             3代表为学员评分
    """
    pp = PaperRecordPage(driver, cfg)
    if not (pp.open(exam_name)):
        return
    pp.click_student_info()

    if etype == 1:
        pp.choose_all_stu()
        pp.output_sendpaper_result()

    elif etype == 2:
        pp.click_open_paper_result()
        pp.choose_all_stu()
        pp.output_opnepaper_result()
        
    else:
        if pp.click_score(username):
            sp = ScorePage(driver, cfg)
            sp.input_score()


    #exam_name = u"未作答（主观题，免费）"
    #username = "sun123"
    # driver.get("%sexam/" %(base_url))
    # driver.implicitly_wait(10)
    # driver.find_element_by_link_text(u"试卷库").click()
    # driver.implicitly_wait(10)
    # driver.find_element(cfg.get('exam', 'paper_search_by'), \
    #     cfg.get('exam', 'paper_search')).send_keys(exam_name)
    # time.sleep(1)
    # exam_href = driver.execute_script(\
    #     "return $(\"a:contains(\'"+exam_name+"\')\").attr('href')")
    # time.sleep(1)
    # driver.get("%sexam/%s" % (base_url, exam_href))
    # driver.find_element_by_link_text("学员信息").click()
    # time.sleep(1)
    # if etype == 2:
    #     driver.find_element_by_link_text(u"作为开放试卷的统计结果").click()
    #     time.sleep(1)
    #     try:
    #         driver.find_element(cfg.get('exam', 'select_stu_by'), \
    #             cfg.get('exam', 'select_stu')).click()
    #         driver.find_element(cfg.get('exam', 'output_open_by'), \
    #             cfg.get('exam', 'output_open')).click()
    #         time.sleep(2)

    #     except:
    #         print u'试卷暂时没有学员购买'

    # elif etype == 1:
    #     try:
    #         driver.find_element(cfg.get('exam', 'select_stu_by'), \
    #             cfg.get('exam', 'select_stu')).click()
    #         driver.find_element(cfg.get('exam', 'output_by'), \
    #             cfg.get('exam', 'output')).click()
    #         time.sleep(2)
    #     except:
    #         print u'试卷暂时没有分发给学员'

    # else:
    #     #取评分链接
    #     time.sleep(2)
    #     stu_name = driver.execute_script(\
    #         "return $(\"a:contains(\'"+username+"\')\").parents('.odd').children().eq(0).children().text()")
    #     time.sleep(1)
    #     if username not in stu_name:
    #         print username + u'该学员不存在,无法评分。。'
    #     else:
    #         grade_href = driver.execute_script(\
    #             "return $(\"a:contains(\'"+username+"\')\").parents('.odd').children().eq(5).children().attr('href')")
    #         time.sleep(2)
    #         driver.get("%sexam/%s" % (base_url, grade_href))
    #         score_input = driver.find_elements(cfg.get('exam', 'input_score_by'), \
    #             cfg.get('exam', 'input_score'))
    #         score = "0.1"
    #         count = 0
    #         for item in score_input:
    #             try:
    #                 item.clear()
    #                 item.send_keys(score)
    #                 count += 1
    #             except:
    #                 continue
    #         driver.find_element(cfg.get('exam', 'score_save_by'), \
    #             cfg.get('exam', 'score_save')).click()
    #         total_score = count * score
    #         return total_score
    # return True

def send_close_paper(cfg, driver, base_url, username, atype=2):
    """
    参数atype为1表示为学员开通试卷，2表示为学员关闭试卷
    """
    ep = ExamStudentListPage(driver, cfg)
    ep.open()
    ep.search_student(username)
    if atype == 1:
        ep.click_send_paper()
        ep.choose_all_paper()
    else:
        ep.click_close_paper()
        ep.choose_one_paper()
    ep.click_save()
 
