# -*- coding: UTF-8 -*-
'''
Created on Jun 2, 2012

@author: yilulu
'''
import time, random
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from PO.org_student_page import OrgStudentManagePage

def is_element_present(driver, how, what):
    try: driver.find_element(by=how, value=what)
    except NoSuchElementException, e: return False
    return True

def import_one_student(cfg, driver, stu_name):
    ogstumanage = OrgStudentManagePage(driver, cfg)
    ogstumanage.open()
    ogstumanage.input_studentname(stu_name)
    ogstumanage.click_import()

def import_multi_student(cfg, driver, base_url, org_name, stu_txt):

    ogstumanage = OrgStudentManagePage(driver, cfg)
    ogstumanage.open()
    ogstumanage.click_import_multi()
    ogstumanage.click_importchoose()
    ogstumanage.click_importfile(stu_txt)
    ogstumanage.click_importmulti()

def create_student(cfg, driver, base_url, org_name, stu_txt):

    ogstumanage = OrgStudentManagePage(driver, cfg)
    ogstumanage.open()
    ogstumanage.click_create_multi()
    ogstumanage.click_createchoose()
    ogstumanage.click_createfile(stu_txt)
    ogstumanage.click_createmulti()

def auto_create_student(cfg, driver, base_url, org_name, stu_num):
    #自动生成用户名文件创建学员
    #stu_num为需要创建学员的数量
    prefix = chr(random.randint(97, 122)) + chr(random.randint(97, 122)) \
     + chr(random.randint(97, 122))
    stu_txt = r"C:\create_stu.txt"
    stu_file = open(stu_txt, 'w')
    for i in range(stu_num):
        stu_name = 'stu_' + prefix + str(i)
        stu_psw = '1234aa'
        if i == 0:
            stu_file.writelines(" \n")
        stu_file.writelines(stu_name + " " + stu_psw + "\n")
    stu_file.close()
    time.sleep(2)
    create_student(cfg, driver, base_url, org_name, stu_txt)
    time.sleep(5)
    
def open_course_for_one(cfg, driver, base_url, org_name):
    
    ogstumanage = OrgStudentManagePage(driver, cfg)
    ogstumanage.open()
    ogstumanage.click_open_course()
    ogstumanage.click_opencate()
    ogstumanage.click_openchoose()
    ogstumanage.click_openok()
    ogstumanage.click_opensure()

def open_course_for_multi(cfg, driver, base_url, org_name):
    
    ogstumanage = OrgStudentManagePage(driver, cfg)
    ogstumanage.open()
    ogstumanage.click_open_list()
    ogstumanage.click_open_choose()
    ogstumanage.click_open_check()
    ogstumanage.click_open_apply()
    ogstumanage.click_opencate()
    ogstumanage.click_openchoose()
    ogstumanage.click_openok()
    ogstumanage.click_openkeep()
    ogstumanage.click_openaway()

#管理播放授权数
#管理播放授权数页面操作
def manage_course_numdetail(cfg, driver, base_url ,user_name):
    ogstumanage = OrgStudentManagePage(driver, cfg)
    ogstumanage.open()
    try:
        ogstumanage.click_pushcourse()
        ogstumanage.click_pushcontent()
        try:
            ogstumanage.click_changenum()
            ogstumanage.click_coursenum_change()
            ogstumanage.click_coursenum_key()
            ogstumanage.click_save()
        except:
            pass
    except:
        pass
    ogstumanage.click_coursenum_all()
    ogstumanage.click_coursenum_allnum()
    ogstumanage.click_coursenum_apply()   
#学员管理页面操作
def manage_course_num(cfg, driver, base_url ,user_name):
    ogstumanage = OrgStudentManagePage(driver, cfg)
    ogstumanage.open()
    ogstumanage.click_stu_select()
    ogstumanage.click_stu_selectuser()
    ogstumanage.click_stu_selectinput(user_name)
    ogstumanage.click_stu_selectsearch()
    try:
        ogstumanage.click_managenum()
        try:
            ogstumanage.click_pushcourse()
            ogstumanage.click_pushcontent()
            try:
                ogstumanage.click_changenum()
                ogstumanage.click_coursenum_change()
                ogstumanage.click_coursenum_key()
                ogstumanage.click_save()
            except:
                pass
        except:
            pass
        ogstumanage.click_coursenum_all()
        ogstumanage.click_coursenum_allnum()
        ogstumanage.click_coursenum_apply()
    except:
        ogstumanage.self_dr_refresh()
        ogstumanage.click_managenum()
        try:
            ogstumanage.click_pushcourse()
            ogstumanage.click_pushcontent()
            try:
                ogstumanage.click_changenum()
                ogstumanage.click_coursenum_change()
                ogstumanage.click_coursenum_key()
                ogstumanage.click_save()
            except:
                pass
        except:
            pass
        ogstumanage.click_coursenum_all()
        ogstumanage.click_coursenum_allnum()
        ogstumanage.click_coursenum_apply()

#购买开通授权数 bnum为购买的数量
def buy_open_num(cfg, driver, base_url, org_name):
    
    ogstumanage = OrgStudentManagePage(driver, cfg)
    ogstumanage.open_buyopennum()
    ogstumanage.click_inputclick()
    ogstumanage.click_inputclear()
    ogstumanage.click_inputkey()
    ogstumanage.click_buy()
    #判断余额是否充足
    re = is_element_present(driver, By.XPATH, "//div[1]/p/span[2]")
    if re = True:
        pass
    else:
        ogstumanage.click_sure()
