import re
import time
from PyQt5.QtCore import Qt, QSizeF, QEvent
from PyQt5.QtGui import QFont, QTextDocument, QTextCursor
from PyQt5.QtPrintSupport import QPageSetupDialog, QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, uic
from libe.share import SI
import pymysql
import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets


# 数据库操作
class Mysql_act:
    # 连接数据库
    def connect_mysql(self):
        conn = pymysql.connect(host='localhost', user='root', password='123', database='中药', charset='utf8')
        cur = conn.cursor()
        return cur,conn

    def connect_mysql_prescription(self):
        cur,conn = self.connect_mysql()
        sql = 'select 处方名称 from 已有处方信息表'
        df = pd.read_sql(sql, con=conn)
        df1 = np.array(df)  # 先使用array()将DataFrame转换一下  
        df2 = df1.tolist()  # 再将转换后的数据用tolist()转成列表
        cur.close()
        conn.close()
        return df2

    # 连接药材库
    def connect_mysql_medicine(self):
        cur, conn = self.connect_mysql()
        sql = 'select 中药材名称 from 药材库数据表'
        df = pd.read_sql(sql, con=conn)
        df1 = np.array(df)
        df2 = df1.tolist()
        cur.close()
        conn.close()
        return df2

    # 显示到表格
    def show(self,tableWidget,text,count):
        tableWidget.setRowCount(0)          # 格式化行
        tableWidget.setColumnCount(count)   # 格式化列
        for i in range(len(text)):
            item = text[i]
            row = tableWidget.rowCount()
            tableWidget.insertRow(row)
            for j in range(len(item)):
                item = QTableWidgetItem(str(text[i][j]))
                tableWidget.setItem(row, j, item)
                item.setTextAlignment(Qt.AlignCenter)


# 登录界面
class Win_Login(Mysql_act):
    def __init__(self):
        self.ui = uic.loadUi("welcome.ui")
        self.ui.btn_login_pre.clicked.connect(self.onSignIn_pre)
        self.lineEdit_change()

    def onSignIn_pre(self):
        try:
            # user_num = self.ui.lineEdit.text()
            # user_password = self.ui.lineEdit_2.text()
            # cur,conn = self.connect_mysql()
            # sql = 'select * from 账号信息表'
            # df = pd.read_sql(sql, conn)
            # user = np.array(df)
            # for i in user:
            #     if user_num == i[0]:
            #         if user_num == i[0] and user_password == i[1]:
            #             SI.mainWin = Win_Main()
            #             SI.mainWin.ui.show()
            #             self.ui.close()
            #         else:
            #             msg_box = QMessageBox(QMessageBox.Information , '提示', '账号或密码错误')
            #             msg_box.exec_()
            SI.mainWin = Win_Main()
            SI.mainWin.ui.show()
            self.ui.close()
        except:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '账号或密码错误')
            msg_box.exec_()

    def lineEdit_change(self):
        self.ui.lineEdit.returnPressed.connect(self.ui.lineEdit_2.setFocus)
        self.ui.lineEdit_2.returnPressed.connect(self.onSignIn_pre)


# 主界面
class Win_Main(Mysql_act, QWidget):

    def __init__(self):
        super(Win_Main, self).__init__()
        self.printer = QPrinter()      # 打印
        self.ui = uic.loadUi('main_new.ui')   # 主界面
        self.ui.treeWidget.clicked.connect(self.change_page)  # 页面切换
        self.tableWidget_not_write()  # 表格禁止编辑
        self.tableWidget_all_hold()   # 表格铺满
        self.show_all_line()          # 表格显示整行
        self.pre_create_function()    # 处方生成部分函数
        self.supplier_function()      # 供货单位部分函数
        self.med_function()           # 药材管理部分函数
        self.clinical_function()      # 接诊部分函数
        self.send_med_function()      # 缴费与发药部分函数
        self.print_function()         # 打印部分函数
        self.sick_function()          # 患者信息部分函数
        self.account_function()       # 账号管理部分函数
        self.reg_function()           # 挂号部分函数
        self.doctor_function()        # 医生信息部分函数
        self.lineEdit_change()
        self.pre_form()               # 处方模板函数
        self.ill_setting_function()   # 疾病史管理函数
        self.history_ill_function()   # 历史病历函数
        self.help_function()          # 帮助部分函数

    # 页面切换
    def change_page(self):
        i = self.ui.treeWidget.currentItem()
        if i.text(0) == '患者列表':
            self.ui.stackedWidget.setCurrentIndex(1)
        elif i.text(0) == '接诊列表':
            self.ui.stackedWidget.setCurrentIndex(0)
        elif i.text(0) == '药品管理':
            self.ui.stackedWidget.setCurrentIndex(2)
        elif i.text(0) == '供货单位管理':
            self.ui.stackedWidget.setCurrentIndex(3)
        elif i.text(0) == '处方生成':
            self.ui.stackedWidget.setCurrentIndex(5)
        elif i.text(0) == '已有处方':
            self.ui.stackedWidget.setCurrentIndex(4)
        elif i.text(0) == '首页':
            self.ui.stackedWidget.setCurrentIndex(7)
        elif i.text(0) == '收费列表':
            self.ui.stackedWidget.setCurrentIndex(8)
        elif i.text(0) == '发药列表':
            self.ui.stackedWidget.setCurrentIndex(9)
        elif i.text(0) == '账号管理':
            self.ui.stackedWidget.setCurrentIndex(10)
        elif i.text(0) == '处方模板':
            self.ui.stackedWidget.setCurrentIndex(15)
        elif i.text(0) == '疾病史管理':
            self.ui.stackedWidget.setCurrentIndex(18)
        elif i.text(0) == '帮助':
            self.ui.stackedWidget.setCurrentIndex(19)

    # 表格禁止编辑
    def tableWidget_not_write(self):
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 挂号病人信息表格禁止编辑
        self.ui.tableWidget_3.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 病人信息表格禁止编辑
        self.ui.tableWidget_5.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 供货单位表格禁止编辑
        self.ui.tableWidget_6.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 处方表格禁止编辑
        self.ui.tableWidget_7.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 处方详情表格禁止编辑
        self.ui.tableWidget_8.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 药材表格禁止编辑
        self.ui.tableWidget_9.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 药品信息表格禁止编辑
        self.ui.tableWidget_11.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 收费表格禁止编辑
        self.ui.tableWidget_12.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 药品内容禁止编辑
        self.ui.tableWidget_13.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 发药表格禁止编辑
        self.ui.tableWidget_14.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 药品内容表格禁止编辑
        self.ui.tableWidget_15.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 账号信息表格禁止编辑
        self.ui.tableWidget_16.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 患者处方详情信息表格禁止编辑
        self.ui.tableWidget_17.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 医生信息表格禁止编辑

    # 表格铺满
    def tableWidget_all_hold(self):
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 挂号病人信息表格铺满整个QTableWidget控件
        self.ui.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 处方信息表格铺满整个QTableWidget控件
        self.ui.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 病人信息表格铺满整个QTableWidget控件
        self.ui.tableWidget_4.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 药材表格铺满整个QTableWidget控件
        self.ui.tableWidget_5.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 供货单位表格铺满整个QTableWidget控件
        self.ui.tableWidget_6.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 处方表格铺满整个QTableWidget控件
        self.ui.tableWidget_7.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 处方详情表格铺满整个QTableWidget控件
        self.ui.tableWidget_8.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 药材表格铺满整个QTableWidget控件
        self.ui.tableWidget_9.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 药品信息表格铺满整个QTableWidget控件
        self.ui.tableWidget_10.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 西药品表格铺满整个QTableWidget控件
        self.ui.tableWidget_11.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 收费表格铺满整个QTableWidget控件
        self.ui.tableWidget_12.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 药品内容表格铺满整个QTableWidget控件
        self.ui.tableWidget_13.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 发药表格铺满整个QTableWidget控件
        self.ui.tableWidget_14.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 药品内容表格铺满整个QTableWidget控件
        self.ui.tableWidget_15.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 账号信息表格铺满整个QTableWidget控件
        self.ui.tableWidget_16.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 患者处方详情信息表格铺满整个QTableWidget控件
        self.ui.tableWidget_17.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 医生信息表格铺满整个QTableWidget控件
        self.ui.tableWidget_18.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 处方模板信息表格铺满整个QTableWidget控件
        self.ui.tableWidget_19.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 处方模板中药处方表格铺满整个QTableWidget控件
        self.ui.tableWidget_20.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 处方模板西药处方表格铺满整个QTableWidget控件

    # 表格显示整行
    def show_all_line(self):
        self.ui.tableWidget_6.setSelectionBehavior(QAbstractItemView.SelectRows)  # 处方表格显示整行
        self.ui.tableWidget_4.setSelectionBehavior(QAbstractItemView.SelectRows)  # 药材表格显示整行
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 候诊病人信息表格显示整行
        self.ui.tableWidget_18.setSelectionBehavior(QAbstractItemView.SelectRows)  # 处方模板信息表格显示整行

    # 处方生成部分函数
    def pre_create_function(self):
        self.show_prescription()  # 展示处方
        self.ui.tableWidget_6.cellPressed.connect(self.get_prescription_name)  # 点击返回处方名称
        self.ui.tableWidget_8.cellPressed.connect(self.get_medicine_name)  # 点击返回药材名称
        self.ui.btn_delete_4.clicked.connect(self.delete_pre)  # 删除处方
        self.ui.btn_seek_2.clicked.connect(self.select_pre)  # 查找处方
        self.ui.lineEdit_26.returnPressed.connect(self.select_pre)  # 回车查找
        self.ui.btn_update_1.clicked.connect(self.show_prescription)  # 更新处方
        self.show_medicine()  # 处方生成里药材展示
        self.ui.btn_seek_3.clicked.connect(self.select_medicine)  # 查找药材
        self.ui.lineEdit_29.returnPressed.connect(self.select_medicine)  # 回车查找
        self.ui.btn_update_2.clicked.connect(self.show_medicine)  # 更新药材
        self.ui.btn_create_4.clicked.connect(self.write_in_prescription)  # 写入处方
        self.ui.lineEdit_30.returnPressed.connect(self.write_in_prescription)  # 回车写入
        self.ui.btn_create_2.clicked.connect(self.creat_prescription)  # 生成处方
        self.ui.lineEdit_28.returnPressed.connect(self.creat_prescription)  # 回车生成
        self.ui.btn_eighteen.clicked.connect(self.eighteen_against)  # 十八反
        self.ui.btn_ninteen.clicked.connect(self.nineteen_fear)  # 十九畏
        self.ui.btn_clear_1.clicked.connect(self.clear_textEdit)  # 清空处方文本
        self.ui.btn_create_3.clicked.connect(self.pre_text)  # 点击详情
        self.ui.lineEdit_27.setFont(QFont("黑体", 16))
        self.ui.lineEdit_27.setAlignment(QtCore.Qt.AlignCenter)

    # 供货单位部分函数
    def supplier_function(self):
        self.show_supplier()  # 展示供货单位
        self.ui.btn_updata_1.clicked.connect(self.show_supplier)  # 更新供货单位
        self.ui.btn_create_1.clicked.connect(self.add_supplier)  # 添加供货单位
        self.ui.tableWidget_5.cellPressed.connect(self.get_supplier_name)  # 点击返回企业名称
        self.ui.btn_delete_2.clicked.connect(self.delete_supplier)  # 删除企业
        self.ui.btn_seek_1.clicked.connect(self.seek_supplier)  # 查找企业
        self.ui.lineEdit_25.returnPressed.connect(self.seek_supplier)  # 回车查找
        self.ui.btn_delete_1.clicked.connect(self.empty_supplier_text)  # 清空企业文本

    # 药材管理部分函数
    def med_function(self):
        self.show_med()  # 展示药材
        self.show_west_med()  # 展示西药品信息
        self.ui.btn_add_1.clicked.connect(self.add_east_med)  # 添加药材
        self.ui.btn_add_2.clicked.connect(self.add_west_med)  # 添加西药品
        self.ui.btn_select_med_2.clicked.connect(self.select_east_med)  # 查找药材
        self.ui.lineEdit_31.returnPressed.connect(self.select_east_med)  # 回车查找
        self.ui.btn_select_med.clicked.connect(self.select_west_med)  # 查找药品
        self.ui.lineEdit_31.returnPressed.connect(self.select_west_med)  # 回车查找
        self.ui.btn_delete_3.clicked.connect(self.empty_med_text)  # 清空药材文本
        self.ui.btn_delete_5.clicked.connect(self.empty_west_text)  # 清空西药品文本

    # 接诊部分函数
    def clinical_function(self):
        self.wait_sick_info()  # 显示候诊病人信息
        self.ui.tableWidget.cellPressed.connect(self.get_wait_sick)  # 点击展示候诊病人信息
        self.ui.btn_wait_sick.clicked.connect(self.wait_sick_info)  # 点击候诊
        self.ui.btn_sick.clicked.connect(self.sick_info)  # 显示已珍病人信息
        self.ui.btn_east_pre.clicked.connect(self.east_pre)  # 点击中药处方
        self.ui.btn_west_pre.clicked.connect(self.west_pre)  # 点击西药处方
        self.ui.btn_add_east_pre.clicked.connect(self.add_pre)  # 添加药方
        self.ui.btn_add_east_pre_2.clicked.connect(self.add_med)  # 添加西药
        self.ui.btn_create_new.clicked.connect(self.clear_sick_text)  # 清空病人信息
        self.ui.btn_sick_text_sure.clicked.connect(self.add_sick_info)  # 将病人信息添加到数据库
        self.show_ill_history()            # 显示疾病

    # 挂号部分函数
    def reg_function(self):
        self.ui.btn_reg.clicked.connect(self.reg_page)   # 跳转挂号页面
        self.ui.btn_reg_sure.clicked.connect(self.reg_text_add)  # 挂号信息添加

    # 缴费与发药部分函数
    def send_med_function(self):
        self.show_wait_sick_list()  # 展示未缴费列表
        self.show_no_send_list()  # 展示未发药列表
        self.ui.tableWidget_11.cellPressed.connect(self.show_cost_list)  # 点击展示缴费病人所需药品
        self.ui.tableWidget_13.cellPressed.connect(self.show_send_list)  # 点击展示发药病人所需药品
        self.ui.btn_wait_pay.clicked.connect(self.show_wait_sick_list)  # 展示未缴费病人列表
        self.ui.btn_wait_get_med.clicked.connect(self.show_no_send_list)  # 展示未发药病人列表
        self.ui.btn_med_need_sure.clicked.connect(self.sick_pay_sure)  # 确认缴费
        self.ui.btn_pay.clicked.connect(self.show_already_pay)  # 已缴费病人列表
        self.ui.btn_seek_wait_sick.clicked.connect(self.seek_wait_sick)  # 搜索缴费病人
        self.ui.lineEdit_42.returnPressed.connect(self.seek_wait_sick)
        self.ui.btn_seek_get_med.clicked.connect(self.seek_send_med_sick)  # 搜索发药病人
        self.ui.lineEdit_45.returnPressed.connect(self.seek_send_med_sick)
        self.ui.btn_already_get_med.clicked.connect(self.show_send_sick_list)  # 展示已发药列表
        self.ui.btn_get_med_sure.clicked.connect(self.sick_get_med_sure)  # 确定发药

    # 患者信息部分函数
    def sick_function(self):
        self.show_sick_text()
        self.ui.btn_select_sick.clicked.connect(self.select_sick)  # 查找患者
        self.ui.lineEdit_11.returnPressed.connect(self.select_sick)  # 回车查找
        self.ui.lineEdit_12.returnPressed.connect(self.select_sick)  # 回车查找
        self.ui.lineEdit_13.returnPressed.connect(self.select_sick)  # 回车查找
        self.ui.btn_update_sick.clicked.connect(self.show_sick_text)  # 更新患者信息
        self.ui.tableWidget_3.cellPressed.connect(self.key_text_clicked)  # 点击显示患者详细信息
        self.ui.back_sick_text.clicked.connect(self.back_sick_text_page)  # 点击返回

    # 账号管理部分函数
    def account_function(self):
        self.show_user()  # 展示账号信息
        self.ui.btn_seek_user.clicked.connect(self.seek_user)  # 账号查找
        self.ui.lineEdit_48.returnPressed.connect(self.seek_user)  # 回车查找
        self.ui.tableWidget_15.cellPressed.connect(self.clicked_delete_user)   # 点击删除账号
        self.ui.btn_add_user.clicked.connect(self.add_user)  # 添加账号
        self.ui.btn_updata_user.clicked.connect(self.show_user)  # 更新账号信息
        self.ui.btn_clear_user.clicked.connect(self.clear_user_text)  # 清空信息

    # 医生信息部分函数
    def doctor_function(self):
        self.ui.btn_doctor.clicked.connect(self.doctor_page)  # 跳转医生页面
        self.show_doctor_text()   # 展示医生信息
        self.ui.btn_seek_doctor.clicked.connect(self.seek_doctor)  # 查找医生
        self.ui.lineEdit_71.returnPressed.connect(self.seek_doctor)  # 回车查找
        self.ui.tableWidget_17.cellPressed.connect(self.doctor_text_page)   # 点击跳转医生详细信息页面
        self.ui.btn_back_doctor_page.clicked.connect(self.doctor_page)   # 返回医生信息页面

    # 打印部分函数
    def print_function(self):
        self.ui.btn_print.clicked.connect(self.print_fun)  # 打印页面

    # 处方模板函数
    def pre_form(self):
        self.ui.btn_pre_form.clicked.connect(self.pre_form_page)    # 切换处方模板页面
        self.show_pre_form()   # 显示处方模板
        self.ui.btn_seek_pre_form.clicked.connect(self.seek_pre_form)  # 查找模板
        self.ui.comboBox_2.currentIndexChanged.connect(self.change_form)
        self.ui.btn_add_form.clicked.connect(self.add_form)   # 添加模板
        self.ui.btn_add_east_pre_3.clicked.connect(self.form_add_east_pre)    # 添加中药品
        self.ui.btn_add_east_pre_4.clicked.connect(self.form_add_west_pre)    # 添加西药品
        self.ui.btn_back_form_1.clicked.connect(self.back_set_page)       # 返回
        self.ui.btn_back_form_2.clicked.connect(self.back_set_page)       # 返回
        self.ui.btn_add_east_form.clicked.connect(self.add_east_form)    # 添加中药处方模板
        self.ui.btn_add_west_form.clicked.connect(self.add_west_form)    # 添加西药处方模板
        self.ui.btn_delete_form.clicked.connect(self.delete_form)     # 删除模板

    # 疾病管理函数
    def ill_setting_function(self):
        self.show_ill_setting()    # 在设置展示疾病史
        self.ui.btn_ill_add.clicked.connect(self.add_allergy_ill)   # 添加过敏史
        self.ui.btn_ill_add_1.clicked.connect(self.add_past_ill)   # 添加既往史
        self.ui.btn_ill_add_2.clicked.connect(self.add_heredity_ill)   # 添加遗传史

    # 历史病历函数
    def history_ill_function(self):
        self.ui.btn_sick_history_text.clicked.connect(self.history_ill_page)     # 历史病历页面

    # 帮助部分函数
    def help_function(self):
        self.ui.listWidget_4.itemClicked.connect(self.help_page)

    # 展示供货单位
    def show_supplier(self):
        cur, conn = self.connect_mysql()
        sql = 'select 企业名称,企业类型,单位地址,单位电话,许可证号,营业执照,GMP,备注 from 供货单位管理表'
        df = pd.read_sql(sql, con=conn)
        df1 = np.array(df)
        df2 = df1.tolist()
        cur.close()
        conn.close()
        self.ui.tableWidget_5.setRowCount(0)  # 格式化行
        self.ui.tableWidget_5.setColumnCount(8)  # 格式化列
        for i in range(len(df2)):
            item = df2[i]
            row = self.ui.tableWidget_5.rowCount()
            self.ui.tableWidget_5.insertRow(row)
            for j in range(len(item)):
                item = QTableWidgetItem(str(df2[i][j]))
                self.ui.tableWidget_5.setItem(row, j, item)
                item.setTextAlignment(Qt.AlignCenter)

    # 添加供货单位
    def add_supplier(self):
        self.reply = QMessageBox(QMessageBox.Question, '提交', '确定提交？')
        yes = self.reply.addButton('确定', QMessageBox.YesRole)
        no = self.reply.addButton('取消', QMessageBox.NoRole)
        self.reply.show()
        self.reply.exec_()
        if self.reply.clickedButton() == yes:
            ls = [self.ui.lineEdit_24.text(), self.ui.lineEdit_19.text(), self.ui.lineEdit_20.text(),
                  self.ui.lineEdit_22.text(), self.ui.lineEdit_23.text(), self.ui.lineEdit_18.text(),
                  self.ui.lineEdit_21.text(), self.ui.textEdit_2.toPlainText()]
            cur, conn = self.connect_mysql()
            sql = 'insert into 供货单位管理表(企业名称,企业类型,单位地址,单位电话,许可证号,营业执照,GMP,备注) values ("%s","%s","%s","%s","%s","%s","%s","%s")' % (
                ls[0], ls[1], ls[2], ls[3], ls[4], ls[5], ls[6], ls[7])
            rows = cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            ls.clear()
            self.show_supplier()

    # 删除供货单位
    def delete_supplier(self):
        self.reply = QMessageBox(QMessageBox.Question, '删除', '确定删除？')
        yes = self.reply.addButton('确定', QMessageBox.YesRole)
        no = self.reply.addButton('取消', QMessageBox.NoRole)
        self.reply.show()
        self.reply.exec_()
        if self.reply.clickedButton() == yes:
            cur, conn = self.connect_mysql()
            sql = 'delete from 供货单位管理表 where 企业名称 = "%s"' % SI.supplier_name_text
            rows = cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            self.show_supplier()

    # 获得企业名称
    def get_supplier_name(self, row, col):
        try:
            content = self.ui.tableWidget_5.item(row, col).text()  # 点击处方名获得文本
            SI.supplier_name_text = content  # 将处方名放入变量pre_name_text
        except:
            print('选中内容为空')

    # 获得候诊病人信息
    def get_wait_sick(self, row, col):
        try:
            sick_num = self.ui.tableWidget.item(row,0).text()
            cur,conn = self.connect_mysql()
            sql = 'select * from 挂号病人信息表  where 门诊编号 = "%s"'%sick_num
            df = pd.read_sql(sql,conn)
            sick_text = np.array(df)
            self.ui.lineEdit.setText(sick_text[0][1])
            self.ui.lineEdit_2.setText(sick_text[0][2])
            self.ui.lineEdit_9.setText(sick_text[0][3])
        except:
            print('选中内容为空')

    # 显示处方名
    def show_prescription(self):
        pre_name = self.connect_mysql_prescription()  # 连接到处方库并将处方名转换为列表
        self.show(self.ui.tableWidget_6, pre_name, 1)  # 将处方名显示到表格1

    # 显示药材名
    def show_medicine(self):  # 显示药材名
        med_name = self.connect_mysql_medicine()
        self.show(self.ui.tableWidget_8, med_name, 1)  # 将药材名显示到表格2

    # 获得处方名
    def get_prescription_name(self, row, col):  # 获得处方名
        try:
            content = self.ui.tableWidget_6.item(row, col).text()  # 点击处方名获得文本
            SI.pre_name_text = content  # 将处方名放入变量pre_name_text
            self.ui.lineEdit_27.setText(content)
            cur, conn = self.connect_mysql()
            sql = 'select 处方详情 from 已有处方信息表 where 处方名称 = "%s"' % content
            df = pd.read_sql(sql, con=conn)
            df1 = np.array(df)
            pre_need = df1[0][0]
            str1 = re.sub("[\!\%\[\]\,\。]", "",pre_need)
            str2 = str1.replace("'", "")  # 去除单引号
            text = re.split(r'[\s:]+', str2.strip())
            self.ui.tableWidget_7.setRowCount(0)
            self.ui.tableWidget_7.setColumnCount(2)
            i = 0
            while i < len(text):
                row = self.ui.tableWidget_7.rowCount()
                self.ui.tableWidget_7.insertRow(row)
                item = QTableWidgetItem(str(text[i]))
                item1 = QTableWidgetItem(str(text[i + 1]))
                item.setTextAlignment(Qt.AlignCenter)
                item1.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_7.setItem(row, 0, item)
                self.ui.tableWidget_7.setItem(row, 1, item1)
                i += 2
            conn.commit()
            cur.close()
            conn.close()
        except:
            print('选中内容为空')

    # 获得药材名
    def get_medicine_name(self, row, col):  # 获得药材名
        try:
            content = self.ui.tableWidget_8.item(row, col).text()  # 点击药材名获得文本
            SI.medicine_name_text = content  # 将药材名放入变量medicine_name_text
        except:
            print('选中内容为空')

    # 删除处方
    def delete_pre(self):  # 删除处方
        self.reply = QMessageBox(QMessageBox.Question, '删除', '确定删除？')
        yes = self.reply.addButton('确定', QMessageBox.YesRole)
        no = self.reply.addButton('取消', QMessageBox.NoRole)
        self.reply.show()
        self.reply.exec_()
        if self.reply.clickedButton() == yes:
            cur, conn = self.connect_mysql()
            sql = "delete from 已有处方信息表 where 处方名称 = (%s) "  # 删除处方的sql语句
            rows = cur.execute(sql, SI.pre_name_text)
            conn.commit()
            cur.close()
            conn.close()
            self.show_prescription()

    # 删除处方的点击事件
    def delete_show(self):  # 删除处方的点击事件
        self.reply = QMessageBox(QMessageBox.Question, '删除', '确定删除？')
        yes = self.reply.addButton('确定', QMessageBox.YesRole)
        no = self.reply.addButton('取消', QMessageBox.NoRole)
        self.reply.show()
        self.reply.exec_()
        if self.reply.clickedButton() == yes:
            self.delete_pre()

    # 查找药材
    def select_medicine(self):  # 查找药材
        text = self.ui.lineEdit_29.text()
        df = self.connect_mysql_medicine()
        self.ui.tableWidget_8.setRowCount(0)
        self.ui.tableWidget_8.setColumnCount(1)
        for i in df:
            if text in i[0]:
                row = self.ui.tableWidget_8.rowCount()
                self.ui.tableWidget_8.insertRow(row)
                for j in range(len(i)):
                    item = QTableWidgetItem(str(i[j]))
                    self.ui.tableWidget_8.setItem(row, j, item)
                    item.setTextAlignment(Qt.AlignCenter)

    # 查找处方
    def select_pre(self):  # 查找处方
        text = self.ui.lineEdit_26.text()
        pre_name = self.connect_mysql_prescription()
        self.ui.tableWidget_6.setRowCount(0)
        self.ui.tableWidget_6.setColumnCount(1)
        for i in pre_name:
            if text in i[0]:
                row = self.ui.tableWidget_6.rowCount()
                self.ui.tableWidget_6.insertRow(row)
                for j in range(len(i)):
                    item = QTableWidgetItem(str(i[j]))
                    self.ui.tableWidget_6.setItem(row, j, item)
                    item.setTextAlignment(Qt.AlignCenter)

    # 写入处方
    def write_in_prescription(self):  # 写入处方
        try:
            medicine_num = self.ui.lineEdit_30.text()
            medicine_name = SI.medicine_name_text
            cur, conn = self.connect_mysql()
            sql = 'select 中药材名称 from 药材库数据表'
            df = pd.read_sql(sql, con=conn)
            df1 = np.array(df)
            df2 = df1.tolist()
            cur.close()
            conn.close()
            ls = []
            for i in df2:
                ls.append(i[0])
            if medicine_name not in ls:  # 判断是否点击药材名
                title = '提示'
                obj = '请点击药材名'
                self.warn_text(title, obj)
            else:
                self.ui.textEdit_3.append(medicine_name)  # 将药材名加到文本框中
                self.ui.textEdit_3.append(medicine_num + 'g')  # 将数量加到文本框中
                SI.pre_med_name.append(medicine_name)  # 将药材名加到列表pre_med_name中
                SI.pre_med_name.append(medicine_num)  # 将数量加到列表pre_med_name中
        except:
            title = '提示'
            obj = '请输入数量'
            self.warn_text(title, obj)

    # 生成处方
    def creat_prescription(self):  # 生成处方
        try:
            pre_text = self.ui.textEdit_3.toPlainText()
            print(pre_text)
            print(len(pre_text ))
            if  pre_text:
                conn = pymysql.connect(host='localhost', user='root', password='123', database='中药', charset='utf8')
                cur = conn.cursor()
                pre_name = self.ui.lineEdit_28.text()
                all_cost = 0
                i = 0
                while i < len(SI.pre_med_name):
                    sql = 'select 价格 from 药材库数据表 where 中药材名称 = "%s"' %(SI.pre_med_name[i])
                    df = pd.read_sql(sql,conn)
                    money = np.array(df)
                    all_cost += int(money[0][0]) * int(SI.pre_med_name[i+1])
                    i += 2
                sql1 = 'insert into 已有处方信息表(处方名称,处方详情,价格) values ("%s","%s","%s")'%(pre_name,SI.pre_med_name ,str(all_cost))
                rows = cur.execute(sql1)
                conn.commit()
                self.ui.lineEdit_27.setText(pre_name)  # 将处方名打印到处方名lineEdit
                cur.close()
                conn.close()
                self.ui.tableWidget_7.setRowCount(0)
                self.ui.tableWidget_7.setColumnCount(2)
                i = 0
                while i < len(SI.pre_med_name):
                    row = self.ui.tableWidget_7.rowCount()
                    self.ui.tableWidget_7.insertRow(row)
                    item = QTableWidgetItem(str(SI.pre_med_name[i]))
                    item1 = QTableWidgetItem(str(SI.pre_med_name[i+1]))
                    self.ui.tableWidget_7.setItem(row, 0, item)
                    self.ui.tableWidget_7.setItem(row, 1, item1)
                    item.setTextAlignment(Qt.AlignCenter)
                    item1.setTextAlignment(Qt.AlignCenter)
                    i += 2
                self.reply = QMessageBox(QMessageBox.Information, '提示', '处方已生成')
                yes = self.reply.addButton('确定', QMessageBox.YesRole)
                self.reply.show()
                self.reply.exec_()
            else:
                title = '警告'
                obj = '请输入处方信息'
                self.warn_text(title, obj)

        except:
            title = '警告'
            obj = '请输入处方信息'
            self.warn_text(title, obj)

    # 清空文本
    def clear_textEdit(self):  # 清空文本
        self.ui.textEdit_3.clear()
        self.ui.lineEdit_28.clear()
        SI.pre_med_name.clear()

    # 十八反
    def eighteen_against(self):  # 十八反
        if '乌头' in SI.pre_med_name:
            name = ['半夏', '瓜蒌', '贝母', '白蔹', '白芨']
            for i in name:
                if i in SI.pre_med_name:
                    title = '警告'
                    warn = '该处方违反了十八反：乌头（贝母、瓜蒌、半夏、白蔹、白芨）'
                    self.warn_text(title, warn)
        elif '甘草' in SI.pre_med_name:
            name = ['海藻', '京大戟', '甘遂', '芫花']
            for i in name:
                if i in SI.pre_med_name:
                    title = '警告'
                    warn = '该处方违反了十八反：甘草(甘遂、京大戟、海藻、芫花)'
                    self.warn_text(title, warn)
        elif '藜芦' in SI.pre_med_name:
            name = ['人参', '沙参', '丹参', '玄参', '细辛', '芍药']
            for i in name:
                if i in SI.pre_med_name:
                    title = '警告'
                    warn = '该处方违反了十八反：藜芦（人参、沙参、丹参、玄参、细辛、芍药）'
                    self.warn_text(title, warn)
        else:
            title = '提示'
            warn = '该处方没有违反十八反'
            self.warn_text(title, warn)

    # 十九畏
    def nineteen_fear(self):  # 十九畏
        ls = [['硫磺', '朴硝'], ['水银', '砒霜'], ['狼毒', '密陀僧'], ['巴豆', '牵牛'], ['郁金', '丁香'], ['川乌', '犀角'], ['草乌', '犀角'],
              ['牙硝', '三棱'], ['官桂', '石脂'], ['人参', '五灵脂']]
        num = 0
        for i in ls:
            count = 0
            for j in SI.pre_med_name:
                if j in i:
                    count += 1
            if count >= 2:
                title = '警告'
                warn = '该处方违反了十九畏：%s-%s' % (i[0], i[1])
                self.warn_text(title, warn)
                num += 1
        if num == 0:
            title = '提示'
            warn = '该处方没有违反十九畏'
            self.warn_text(title, warn)

    # 处方详情点击
    def pre_text(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    # 警告提示框
    def warn_text(self, obj, obj1):
        msg_box = QMessageBox(QMessageBox.Warning, obj, obj1)
        msg_box.exec_()

    # 查找供货单位
    def seek_supplier(self):
        text = self.ui.lineEdit_25.text()
        cur, conn = self.connect_mysql()
        sql = 'select 企业名称,企业类型,单位地址,单位电话,许可证号,营业执照,GMP,备注 from 供货单位管理表'
        df = pd.read_sql(sql, con=conn)
        df1 = np.array(df)
        df2 = df1.tolist()
        cur.close()
        conn.close()
        self.ui.tableWidget_5.setRowCount(0)
        self.ui.tableWidget_5.setColumnCount(8)
        for i in df2:
            if text in i[0]:
                row = self.ui.tableWidget_5.rowCount()
                self.ui.tableWidget_5.insertRow(row)
                for j in range(len(i)):
                    item = QTableWidgetItem(str(i[j]))
                    self.ui.tableWidget_5.setItem(row, j, item)
                    item.setTextAlignment(Qt.AlignCenter)

    # 清空供货单位信息
    def empty_supplier_text(self):
        self.ui.textEdit_2.clear()
        self.ui.lineEdit_18.clear()
        self.ui.lineEdit_19.clear()
        self.ui.lineEdit_20.clear()
        self.ui.lineEdit_21.clear()
        self.ui.lineEdit_22.clear()
        self.ui.lineEdit_23.clear()
        self.ui.lineEdit_24.clear()

    # 展示药材
    def show_med(self):
        cur, conn = self.connect_mysql()
        sql = 'select * from 药材库数据表'
        df = pd.read_sql(sql, con=conn)
        df1 = np.array(df)
        df2 = df1.tolist()
        cur.close()
        conn.close()
        med_name = df2
        self.show(self.ui.tableWidget_4, med_name, 7)

    # 展示药品
    def show_west_med(self):
        cur, conn = self.connect_mysql()
        sql = 'select * from 西药品信息表'
        df = pd.read_sql(sql, con=conn)
        df1 = np.array(df)
        df2 = df1.tolist()
        cur.close()
        conn.close()
        med_name = df2
        self.show(self.ui.tableWidget_9, med_name, 7)

    # 添加药材
    def add_east_med(self):
        self.reply = QMessageBox(QMessageBox.Question, '添加', '确定添加？')
        yes = self.reply.addButton('确定', QMessageBox.YesRole)
        no = self.reply.addButton('取消', QMessageBox.NoRole)
        self.reply.show()
        self.reply.exec_()
        if self.reply.clickedButton() == yes:
            ls = [self.ui.lineEdit_16.text(), self.ui.lineEdit_17.text(), self.ui.lineEdit_15.text(),
                  self.ui.lineEdit_14.text(),self.ui.lineEdit_37.text()]
            cur, conn = self.connect_mysql()
            sql = 'insert into 药材库数据表(中药材名称,中药材类别,当前库存,备注,价格) values ("%s","%s","%s","%s","%s")' % (
                ls[0], ls[1], ls[2], ls[3], ls[4])
            rows = cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            ls.clear()
            self.show_med()

    # 添加药品
    def add_west_med(self):
        self.reply = QMessageBox(QMessageBox.Question, '添加', '确定添加？')
        yes = self.reply.addButton('确定', QMessageBox.YesRole)
        no = self.reply.addButton('取消', QMessageBox.NoRole)
        self.reply.show()
        self.reply.exec_()
        if self.reply.clickedButton() == yes:
            ls = [self.ui.lineEdit_32.text(), self.ui.lineEdit_33.text(), self.ui.lineEdit_34.text(),
                  self.ui.lineEdit_35.text(),self.ui.lineEdit_8.text()]
            cur, conn = self.connect_mysql()
            sql = 'insert into 西药品信息表(药品名称,类别,当前库存,规格,价格) values ("%s","%s","%s","%s","%s")' % (ls[0], ls[1], ls[2], ls[3],ls[4])
            rows = cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            ls.clear()
            self.show_west_med()

    # 药材信息清空
    def empty_med_text(self):
        self.ui.lineEdit_14.clear()
        self.ui.lineEdit_15.clear()
        self.ui.lineEdit_16.clear()
        self.ui.lineEdit_17.clear()
        self.ui.lineEdit_37.clear()

    # 药品信息清空
    def empty_west_text(self):
        self.ui.lineEdit_32.clear()
        self.ui.lineEdit_33.clear()
        self.ui.lineEdit_34.clear()
        self.ui.lineEdit_35.clear()
        self.ui.lineEdit_8.clear()

    # 病人信息清空
    def clear_sick_text(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit_5.clear()
        self.ui.lineEdit_6.clear()
        self.ui.lineEdit_9.clear()
        self.ui.lineEdit_10.clear()
        self.ui.tableWidget_2.setRowCount(0)
        self.ui.tableWidget_10.setRowCount(0)
        self.ui.tableWidget_2.setColumnCount(0)
        self.ui.tableWidget_10.setColumnCount(0)

    # 展示候诊病人信息
    def wait_sick_info(self):
        cur, conn = self.connect_mysql()
        sql = "select 门诊编号,姓名,年龄 from 候诊病人信息表"
        df = pd.read_sql(sql, con=conn)
        df1 = np.array(df)
        df2 = df1.tolist()
        conn.commit()
        cur.close()
        conn.close()
        self.ui.tableWidget.setRowCount(0)  # 格式化行
        self.ui.tableWidget.setColumnCount(3)  # 格式化列
        for i in range(len(df2)):
            item = df2[i]
            row = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row)
            for j in range(len(item)):
                item = QTableWidgetItem(str(df2[i][j]))
                self.ui.tableWidget.setItem(row, j, item)
                item.setTextAlignment(Qt.AlignCenter)

    # 展示已珍病人信息表
    def sick_info(self):
        cur, conn = self.connect_mysql()
        sql = "select 门诊编号,姓名,年龄 from 已诊病人信息表"
        df = pd.read_sql(sql, con=conn)
        df1 = np.array(df)
        df2 = df1.tolist()
        conn.commit()
        cur.close()
        conn.close()
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(3)
        for i in range(len(df2)):
            item = df2[i]
            row = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row)
            for j in range(len(item)):
                item = QTableWidgetItem(str(df2[i][j]))
                self.ui.tableWidget.setItem(row, j, item)
                item.setTextAlignment(Qt.AlignCenter)

    # 中药处方
    def east_pre(self):
        self.ui.stackedWidget_2.setCurrentIndex(0)
        if  self.ui.tableWidget_2.item(0,0) == None:
            self.ui.tableWidget_2.setRowCount(0)
            self.ui.tableWidget_2.setColumnCount(5)
            self.ui.tableWidget_2.setHorizontalHeaderLabels(['处方名','方剂数','频次/天','单价/元','总价/元'])
            pre_name = self.connect_mysql_prescription()  # 连接到处方库并将处方名转换为列表
            ls = []
            for i in pre_name:
                ls.append(i[0])
            self.ui.comboBox_5.clear()
            self.ui.comboBox_5.addItems(ls)
            self.ui.comboBox_5.setCurrentIndex(-1)

    # 西药处方
    def west_pre(self):
        self.ui.stackedWidget_2.setCurrentIndex(1)
        if self.ui.tableWidget_10.item(0, 0) == None:
            self.ui.tableWidget_10.setRowCount(0)
            self.ui.tableWidget_10.setColumnCount(6)
            self.ui.tableWidget_10.setHorizontalHeaderLabels(['药品名', '数量', '规格','频次/天','单价/元','总价/元'])
            cur,conn = self.connect_mysql()
            sql = 'select 药品名称,规格 from 西药品信息表'
            df = pd.read_sql(sql,conn)
            med_name = np.array(df)
            ls = []
            for i in med_name:
                ls.append(i[0])
            self.ui.comboBox_6.clear()
            self.ui.comboBox_6.addItems(ls)
            self.ui.comboBox_6.setCurrentIndex(-1)

    # 添加处方
    def add_pre(self):
        try:
            pre_text = self.ui.comboBox_5.currentText()
            cur, conn = self.connect_mysql()
            sql = 'select 价格 from 已有处方信息表 where 处方名称 = "%s" ' % pre_text
            df = pd.read_sql(sql, conn)
            pre = np.array(df)
            num = self.ui.lineEdit_40.text()
            all_cost = int(num) * int(pre[0][0])
            row = self.ui.tableWidget_2.rowCount()
            self.ui.tableWidget_2.insertRow(row)
            item = QTableWidgetItem(str(pre_text))
            item1 = QTableWidgetItem(str(pre[0][0]))
            item2 = QTableWidgetItem(str(all_cost))
            item3 = QTableWidgetItem(str(num))
            self.ui.tableWidget_2.setItem(row,0,item)
            self.ui.tableWidget_2.setItem(row,1,item3)
            self.ui.tableWidget_2.setItem(row,3,item1)
            self.ui.tableWidget_2.setItem(row,4,item2)
            item.setTextAlignment(Qt.AlignCenter)
            item1.setTextAlignment(Qt.AlignCenter)
            item2.setTextAlignment(Qt.AlignCenter)
            item3.setTextAlignment(Qt.AlignCenter)
            SI.all_med_cost += all_cost
            self.ui.lineEdit_7.setText(str(SI.all_med_cost))
            cur.close()
            conn.close()
        except:
            msg_box = QMessageBox(QMessageBox.Information, "提示", "请输入有效信息")
            msg_box.exec_()

    # 添加药品
    def add_med(self):
        try:
            med_text = self.ui.comboBox_6.currentText()
            med_num = self.ui.lineEdit_39.text()
            cur, conn = self.connect_mysql()
            sql = 'select 规格,价格 from 西药品信息表 where 药品名称 = "%s" '%med_text
            df = pd.read_sql(sql, conn)
            med = np.array(df)
            all_cost = int(med_num) * int(med[0][1])
            row = self.ui.tableWidget_10.rowCount()
            self.ui.tableWidget_10.insertRow(row)
            item = QTableWidgetItem(str(med_text))
            item2 = QTableWidgetItem(str(med_num))
            item4 = QTableWidgetItem(str(all_cost))
            item1 = QTableWidgetItem(str(med[0][0]))
            item3 = QTableWidgetItem(str(med[0][1]))
            self.ui.tableWidget_10.setItem(row, 0, item)
            self.ui.tableWidget_10.setItem(row, 1, item2)
            self.ui.tableWidget_10.setItem(row, 2, item1)
            self.ui.tableWidget_10.setItem(row, 4, item3)
            self.ui.tableWidget_10.setItem(row, 5, item4)
            item.setTextAlignment(Qt.AlignCenter)
            item1.setTextAlignment(Qt.AlignCenter)
            item2.setTextAlignment(Qt.AlignCenter)
            item3.setTextAlignment(Qt.AlignCenter)
            item4.setTextAlignment(Qt.AlignCenter)
            SI.all_med_cost += int(all_cost)
            self.ui.lineEdit_7.setText(str(SI.all_med_cost))
            cur.close()
            conn.close()
        except:
            msg_box = QMessageBox(QMessageBox.Information, "提示", "请输入有效信息")
            msg_box.exec_()

    # 展示患者信息
    def show_sick_text(self):
        cur,conn = self.connect_mysql()
        sql = 'select 门诊编号,姓名,性别,年龄,手机号,接诊时间,医生,既往病史,遗传病史,诊断 from 病人信息表'
        df = pd.read_sql(sql,conn)
        sick_text = np.array(df)
        self.show(self.ui.tableWidget_3, sick_text, 11)
        text="详情"
        item = QTableWidgetItem(str(text))
        for i in range(len(sick_text)):
            item = QTableWidgetItem(text)
            self.ui.tableWidget_3.setItem(i, 10, item)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFont(QFont('Times', 10, QFont.Black))
        cur.close()
        conn.close()

    # 查询函数
    def select_way(self,sql):
        cur, conn = self.connect_mysql()
        df = pd.read_sql(sql, conn)
        sick_text = np.array(df)
        if len(sick_text) != 0:
            self.show(self.ui.tableWidget_3, sick_text, 11)
            text = "详情"
            item = QTableWidgetItem(str(text))
            for i in range(len(sick_text)):
                item = QTableWidgetItem(text)
                self.ui.tableWidget_3.setItem(i, 10, item)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(QFont('Times', 10, QFont.Black))
        else:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '查无此人')
            msg_box.exec_()
        cur.close()
        conn.close()

    # 查询患者
    def select_sick(self):
        try:
            key_text = self.ui.lineEdit_11.text()
            time = self.ui.lineEdit_12.text()
            doctor_name = self.ui.lineEdit_13.text()
            if key_text and time and doctor_name:
                if key_text.isdigit() :
                    sql = 'select * from 病人信息表 where 门诊编号 like "%%%s%%" and 接诊时间 like "%%%s%%" and 医生 like "%%%s%%"' % (key_text, time, doctor_name)
                    self.select_way(sql)
                else :
                    sql = 'select * from 病人信息表 where 姓名 like "%%%s%%" and 接诊时间 like  "%%%s%%" and 医生 like "%%%s%%"' % (key_text, time, doctor_name)
                    self.select_way(sql)
            elif key_text and time:
                if key_text.isdigit():
                    sql = 'select * from 病人信息表 where 门诊编号 like "%%%s%%" and 接诊时间 like "%%%s%%"' % (key_text, time)
                    self.select_way(sql)
                else:
                    sql = 'select * from 病人信息表 where 姓名 like "%%%s%%" and 接诊时间 like "%%%s%%" ' % (key_text, time)
                    self.select_way(sql)
            elif time and doctor_name:
                sql = 'select * from 病人信息表 where 接诊时间 like "%%%s%%" and 医生 like "%%%s%%"' % (time, doctor_name)
                self.select_way(sql)
            elif key_text and doctor_name:
                if key_text.isdigit():
                    sql = 'select * from 病人信息表 where 门诊编号 like "%%%s%%" and 医生 like "%%%s%%"' % (key_text, doctor_name)
                    self.select_way(sql)
                else:
                    sql = 'select * from 病人信息表 where 姓名 like "%%%s%%" and 医生 like "%%%s%%" ' % (key_text, doctor_name)
                    self.select_way(sql)
            elif key_text :
                if key_text.isdigit() :
                    sql = 'select * from 病人信息表 where 门诊编号 like "%%%s%%"'%key_text
                    self.select_way(sql)
                else :
                    sql = 'select * from 病人信息表 where 姓名 like "%%%s%%"' % key_text
                    self.select_way(sql)
            elif time:
                sql = 'select * from 病人信息表 where 接诊时间 like "%%%s%%"' % time
                self.select_way(sql)
            elif doctor_name:
                sql = 'select * from 病人信息表 where 医生 like "%%%s%%"' % doctor_name
                self.select_way(sql)
            else:
                msg_box = QMessageBox(QMessageBox.Information, '提示', '请输入关键信息')
                msg_box.exec_()
        except:
            msg_box = QMessageBox(QMessageBox.Warning , '警告', '请输入正确信息')
            msg_box.exec_()

    # 药材查询
    def select_east_med(self):
        key_text = self.ui.lineEdit_31.text()
        cur,conn = self.connect_mysql()
        sql = 'select * from 药材库数据表 where 中药材名称 like "%%%s%%" or 中药材类别 like "%%%s%%"'%(key_text,key_text)
        df = pd.read_sql(sql,conn)
        med_text = np.array(df)
        if len(med_text) != 0:
            self.show(self.ui.tableWidget_4, med_text, 6)
        else:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '无该（类）药材')
            msg_box.exec_()
        cur.close()
        conn.close()

    # 药品查询
    def select_west_med(self):
        key_text = self.ui.lineEdit_36.text()
        cur, conn = self.connect_mysql()
        sql = 'select * from 西药品信息表 where 药品名称 like "%%%s%%" or 类别 like "%%%s%%"' % (key_text, key_text)
        df = pd.read_sql(sql, conn)
        med_text = np.array(df)
        if len(med_text) != 0:
            self.show(self.ui.tableWidget_9, med_text, 6)
        else:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '无该（类）药品')
            msg_box.exec_()
        cur.close()
        conn.close()

    # 病人所需药品或处方信息
    def sick_need_text(self):
        column = self.ui.tableWidget_2.columnCount()  # 获取当前表格共有多少列
        row = self.ui.tableWidget_2.rowCount()  # 获取当前表格共有多少行
        pre_text = []
        num = 2
        for i in range(row):
            for j in range(column):
                pre_text.append(self.ui.tableWidget_2.item(i, j).text())
            pre_text.insert(num,'None')
            num += 6
        column1 = self.ui.tableWidget_10.columnCount()  # 获取当前表格共有多少列
        row1 = self.ui.tableWidget_10.rowCount()  # 获取当前表格共有多少行
        med_text = []
        for i in range(row1):
            for j in range(column1):
                med_text.append(self.ui.tableWidget_10.item(i, j).text())
        sick_need = pre_text + med_text
        cur, conn = self.connect_mysql()
        sql = 'select 门诊编号 from 挂号病人信息表  where 姓名 = "%s"' % self.ui.lineEdit.text()
        df = pd.read_sql(sql, conn)
        sick_num = np.array(df)[0][0]
        state = '未缴费'
        state2 = '未发药'
        sql = 'insert into 病人所需药品信息表(门诊编号,姓名,所需药品,状态) values("%s","%s","%s","%s")' % (sick_num,self.ui.lineEdit.text(),sick_need,state )
        rows = cur.execute(sql)
        conn.commit()
        sql1 = 'insert into 未发药病人信息表(门诊编号,姓名,所需药品,状态) values("%s","%s","%s","%s")' % (sick_num,self.ui.lineEdit.text(),sick_need,state2 )
        rows1 = cur.execute(sql1)
        conn.commit()
        cur.close()
        conn.close()
        return sick_need

    # 患者信息加入数据库
    def add_sick_info(self):
        try:
            self.sick_need_text()
            self.reply = QMessageBox(QMessageBox.Question, '确定', '是否确定？')
            yes = self.reply.addButton('确定', QMessageBox.YesRole)
            no = self.reply.addButton('取消', QMessageBox.NoRole)
            self.reply.show()
            self.reply.exec_()
            SI.all_med_cost == 0
            if self.ui.radioButton_4.isChecked():
                sick_x = "男"
            else:
                sick_x = "女"
            cur, conn = self.connect_mysql()
            sql = 'select 门诊编号 from 挂号病人信息表  where 姓名 = "%s"' % self.ui.lineEdit.text()
            df = pd.read_sql(sql, conn)
            sick_num = np.array(df)[0][0]
            fd = time.gmtime()
            act_time = time.strftime("%Y/%m/%d", fd)
            if self.reply.clickedButton() == yes:
                ls = [sick_num,self.ui.lineEdit.text(), sick_x , self.ui.lineEdit_2.text(),
                      self.ui.lineEdit_9.text(), act_time ,self.ui.lineEdit_10.text(),self.ui.lineEdit_4.text(),self.ui.comboBox.lineEdit().text(),self.ui.comboBox_7.lineEdit().text(),self.ui.comboBox_8.lineEdit().text(),self.ui.lineEdit_6.text()]
                cur, conn = self.connect_mysql()
                sql = 'insert into 病人信息表(门诊编号,姓名,性别,年龄,手机号,接诊时间,医生,地址,过敏史,既往病史,遗传病史,诊断) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                    ls[0], ls[1], ls[2], ls[3], ls[4], ls[5], ls[6], ls[7], ls[8], ls[9],ls[10],ls[11])
                rows = cur.execute(sql)
                conn.commit()
                sql1 = 'delete from 候诊病人信息表 where 门诊编号 = "%s"'% sick_num
                rows = cur.execute(sql1)
                conn.commit()
                sql2 = 'insert into 已诊病人信息表(门诊编号,姓名,年龄,电话) values ("%s","%s","%s","%s")'% (sick_num,self.ui.lineEdit.text(),self.ui.lineEdit_2.text(),self.ui.lineEdit_9.text())
                rows = cur.execute(sql2)
                conn.commit()
                cur.close()
                conn.close()
                ls.clear()
                self.wait_sick_info()
                self.show_med()
                self.show_wait_sick_list()  # 展示未缴费列表
                self.show_no_send_list()  # 展示未发药列表
                self.ill_add()       # 添加新的过敏史、既往史、遗传史
        except:
            msg_box = QMessageBox(QMessageBox.Warning,'提示', '有关键信息未填！')
            msg_box.exec_()

    # 打印函数
    def print_fun(self):
        self.reply = QMessageBox(QMessageBox.Information, '提示', '打印')
        yes = self.reply.addButton('打印设置', QMessageBox.YesRole)
        no = self.reply.addButton('打印', QMessageBox.NoRole)
        self.reply.show()
        self.reply.exec_()
        if self.reply.clickedButton() == yes:
            self.show_print_setting()
        elif self.reply.clickedButton() == no:
            self.show_print_page()
            msg_box = QMessageBox(QMessageBox.Information, '提示', '打印成功！')
            msg_box.exec_()

    # 打印页面
    def show_print_page(self):
        try:
            need = self.sick_need_text()
            sick_need = []
            count = 0
            while count < len(need):
                sick_need.append(need[count])
                sick_need.append(need[count + 1])
                count += 6

            sick_name = self.ui.lineEdit.text()
            sick_year = self.ui.lineEdit_7.text()
            cur,conn = self.connect_mysql()
            sql = 'select 门诊编号 from 挂号病人信息表  where 姓名 = "%s"' % self.ui.lineEdit.text()
            df = pd.read_sql(sql, conn)
            sick_num = np.array(df)[0][0]
            fd = time.gmtime()
            date_year = time.strftime("%Y", fd)
            date_month = time.strftime("%m",fd)
            date_day = time.strftime("%d",fd)
            if self.ui.radioButton_4.isChecked():
                sick_x = "男"
            else:
                sick_x = "女"
            sick_ill = self.ui.lineEdit_6.text()
            doctor = self.ui.lineEdit_10.text()
            all_cost = self.ui.lineEdit_7.text()
            the_html = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
            <html><head><meta name="qrichtext" content="1" /><style type="text/css">
            p, li { white-space: pre-wrap; }
            </style></head><body style=" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;">
            <p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">                 <span style=" font-size:12pt; font-weight:600;">      </span><span style=" font-size:24pt; font-weight:600;">   XXX医院处方笺</span></p>
            <p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;"><br /></p>
            <p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;"><br /></p>
            <p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;"><br /></p>'''
            the_html += '''<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:14pt; font-weight:600;">门诊/住院病历号： {}  </span><span style=" font-weight:600;">                </span><span style=" font-size:14pt; font-weight:600;">{}年  {} 月  {} 日</span></p>
            <p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;"><br /></p>
            <p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">—————————————————————————————————————————————————</span></p>
            <p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:14pt; font-weight:600;">姓名：  {}     性别：  {}       年龄：  {}     费别：{}</span></p>
            <p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">—————————————————————————————————————————————————</span></p>
            <p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:14pt; font-weight:600;">临床诊断：       {}                 科别：{}</span></p>
            <p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">—————————————————————————————————————————————————</span></p>
            <p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:24pt; font-weight:600;">R</span><span style=" font-size:22pt; font-weight:600;">p</span></p>'''.format(
                sick_num , date_year, date_month , date_day , sick_name , sick_x , sick_year , "公", sick_ill, "外科    ")
            the_html += '''<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;"><br /></p>
            <p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;"><br /></p>
            <p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;"><br /></p>
            <p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;"><br /></p>
            <p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;"><br /></p>'''
            j = 0
            for i in range(int(len(sick_need) / 2)):
                the_html += '''<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:14pt; font-weight:600;">        {}           {}</span></p>
                <p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;"><br /></p>'''.format(
                    sick_need[j], sick_need[j + 1])
                j += 2
            a = 34 - 5 - int(len(sick_need))
            for i in range(a - 1):
                the_html += '''<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;"><br /></p>'''
            the_html += '''<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:14pt; font-weight:600;">医师：      {}                          药品金额：{}</span><span style=" font-size:24pt; font-weight:600;"> </span></p>
            <p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">—————————————————————————————————————————————————</span></p>
            <p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:14pt; font-weight:600;">审核： {}    调配：   {}    核对：   {}      发药：{}</span><span style=" font-weight:600;">            </span></p>
            <p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">          </span></p></body></html>'''.format(
                doctor, all_cost , "xxx ", "xxx ", "xxx ", "xxx ")
            self.ui.textEdit_4.setHtml(the_html )
            self.show_print()
        except:
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '有关键信息未填！')
            msg_box.exec_()

    # 打印返回
    def back_main(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    # 显示打印设置
    def show_print_setting(self):
        try :
            printDialog = QPageSetupDialog(self.printer,self)
            printDialog.exec()
        except:
            print(4)

    # 显示打印对话框
    def show_print(self):
        try :
            print_dialog = QPrintDialog(self.printer,self)
            if QDialog.Accepted == print_dialog.exec():
                self.ui.textEdit_4.print(self.printer)
        except:
            print("打印失败")

    # 展示待收费病人名单
    def show_wait_sick_list(self):
        cur,conn = self.connect_mysql()
        sql = 'select 门诊编号,姓名,状态 from 病人所需药品信息表'
        df = pd.read_sql(sql , conn)
        df2 = np.array(df)
        cur.close()
        conn.close()
        self.ui.tableWidget_11.setRowCount(0)  # 格式化行
        self.ui.tableWidget_11.setColumnCount(3)  # 格式化列
        for i in range(len(df2)):
            item = df2[i]
            row = self.ui.tableWidget_11.rowCount()
            self.ui.tableWidget_11.insertRow(row)
            for j in range(len(item)):
                item = QTableWidgetItem(str(df2[i][j]))
                self.ui.tableWidget_11.setItem(row, j, item)
                item.setTextAlignment(Qt.AlignCenter)

    # 展示缴费药品信息
    def show_need_med_text(self,sql,num,name,tableWidget):
        self.ui.lineEdit_43.setText(num)
        self.ui.lineEdit_44.setText(name)
        cur, conn = self.connect_mysql()
        df = pd.read_sql(sql, conn)
        sick_need_text = np.array(df)
        sick_need = sick_need_text[0][2]
        str1 = re.sub("[\!\%\[\]\,\。]", "", sick_need)
        str2 = str1.replace("'", "")  # 去除单引号
        text = re.split(r'[\s:]+', str2.strip())
        tableWidget.setRowCount(0)  # 格式化行
        tableWidget.setColumnCount(5)  # 格式化列
        a = 3
        txt = []
        for i in range(len(text)):
            if i == a:
                a += 6
                continue
            else:
                txt.append(text[i])
        x = 0
        count = len(txt) / 5
        for i in range(int(count)):
            row = tableWidget.rowCount()
            tableWidget.insertRow(row)
            for j in range(5):
                item = QTableWidgetItem(txt[x])
                x += 1
                tableWidget.setItem(row, j, item)
                item.setTextAlignment(Qt.AlignCenter)
        row = tableWidget.rowCount()
        tableWidget.insertRow(row)
        all_cost = 0
        for i in range(row):
            all_cost += int(tableWidget.item(i, 4).text())
        item = QTableWidgetItem(str(all_cost))
        tableWidget.setItem(row, 4, item)
        item.setTextAlignment(Qt.AlignCenter)
        cur.close()
        conn.close()

    # 展示发药药品信息
    def show_send_med_text(self,sql,num,name,tableWidget):
        self.ui.lineEdit_46.setText(num)
        self.ui.lineEdit_47.setText(name)
        cur, conn = self.connect_mysql()
        df = pd.read_sql(sql, conn)
        sick_need_text = np.array(df)
        sick_need = sick_need_text[0][2]
        str1 = re.sub("[\!\%\[\]\,\。]", "", sick_need)
        str2 = str1.replace("'", "")  # 去除单引号
        text = re.split(r'[\s:]+', str2.strip())
        tableWidget.setRowCount(0)  # 格式化行
        tableWidget.setColumnCount(4)  # 格式化列
        a = 4
        b = 5
        txt = []
        for i in range(len(text)):
            if i == a :
                a += 6
                continue
            if i == b:
                b += 6
                continue
            else:
                txt.append(text[i])
        x = 0
        count = len(txt) / 4
        for i in range(int(count)):
            row = tableWidget.rowCount()
            tableWidget.insertRow(row)
            for j in range(4):
                item = QTableWidgetItem(txt[x])
                x += 1
                tableWidget.setItem(row, j, item)
                item.setTextAlignment(Qt.AlignCenter)
        cur.close()
        conn.close()

    # 收费点击展示药品信息
    def show_cost_list(self,row,col):
        wait_pay_sick_name = self.ui.tableWidget_11.item(row,1).text()
        wait_pay_sick_num = self.ui.tableWidget_11.item(row,0).text()
        try:
            sql = 'select * from 病人所需药品信息表 where 门诊编号 = "%s"' % wait_pay_sick_num
            self.show_need_med_text(sql,wait_pay_sick_num,wait_pay_sick_name,self.ui.tableWidget_12)
        except:
            sql = 'select * from 已缴费病人信息表 where 门诊编号 = "%s"' % wait_pay_sick_num
            self.show_need_med_text(sql, wait_pay_sick_num, wait_pay_sick_name,self.ui.tableWidget_12)

    # 发药点击展示药品信息
    def show_send_list(self,row,col):
        wait_get_sick_name = self.ui.tableWidget_13.item(row,1).text()
        wait_get_sick_num = self.ui.tableWidget_13.item(row,0).text()
        try:
            sql = 'select * from 未发药病人信息表 where 门诊编号 = "%s"' % wait_get_sick_num
            self.show_send_med_text(sql,wait_get_sick_num,wait_get_sick_name,self.ui.tableWidget_14)
        except:
            sql = 'select * from 已发药病人信息表 where 门诊编号 = "%s"' % wait_get_sick_num
            self.show_send_med_text(sql, wait_get_sick_num, wait_get_sick_name,self.ui.tableWidget_14)

    # 缴费确定
    def sick_pay_sure(self):
        try:
            sick_num = self.ui.lineEdit_43.text()
            sick_name = self.ui.lineEdit_44.text()
            cur,conn = self.connect_mysql()
            sql = 'delete from 病人所需药品信息表 where 门诊编号 = "%s"'%sick_num
            sql2 = 'select 所需药品 from 病人所需药品信息表 where 门诊编号 = "%s"'%sick_num
            df = pd.read_sql(sql2,conn)
            text = np.array(df)
            need_med = text[0][0]
            rows = cur.execute(sql)
            conn.commit()
            state = '已缴费'
            sql1 = 'insert into 已缴费病人信息表(门诊编号,姓名,所需药品,状态) values ("%s","%s","%s","%s") '%(sick_num,sick_name,need_med,state)
            rows = cur.execute(sql1)
            conn.commit()
            cur.close()
            conn.close()
            self.show_wait_sick_list()
            msg_box = QMessageBox(QMessageBox.Information, '提示', '缴费成功！')
            msg_box.exec_()
        except:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '请选择未缴费人员')
            msg_box.exec_()

    # 展示已缴费病人列表
    def show_already_pay(self):
        cur,conn = self.connect_mysql()
        sql = 'select 门诊编号,姓名,状态 from 已缴费病人信息表'
        df = pd.read_sql(sql,conn)
        df2 = np.array(df)
        self.ui.tableWidget_11.setRowCount(0)  # 格式化行
        self.ui.tableWidget_11.setColumnCount(3)  # 格式化列
        for i in range(len(df2)):
            item = df2[i]
            row = self.ui.tableWidget_11.rowCount()
            self.ui.tableWidget_11.insertRow(row)
            for j in range(len(item)):
                item = QTableWidgetItem(str(df2[i][j]))
                self.ui.tableWidget_11.setItem(row, j, item)
                item.setTextAlignment(Qt.AlignCenter)
        cur.close()
        conn.close()

    # 搜索缴费病人
    def seek_wait_sick(self):
        key_word = self.ui.lineEdit_42.text()
        cur,conn = self.connect_mysql()
        sql = 'select 门诊编号,姓名,状态 from 病人所需药品信息表 where 门诊编号 like "%%%s%%" or 姓名 like "%%%s%%" ' %(key_word ,key_word )
        sql1 = 'select 门诊编号,姓名,状态 from 已缴费病人信息表 where 门诊编号 like "%%%s%%" or 姓名 like "%%%s%%" ' %(key_word ,key_word )
        df = pd.read_sql(sql, conn)
        sick_text = np.array(df)
        df1 = pd.read_sql(sql1, conn)
        sick_text1 = np.array(df1)
        if len(sick_text) != 0:
            self.show(self.ui.tableWidget_11, sick_text, 3)
        elif len(sick_text1) != 0:
            self.show(self.ui.tableWidget_11, sick_text1, 3)
        else:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '查无此人！')
            msg_box.exec_()
        cur.close()
        conn.close()

    # 搜索发药病人
    def seek_send_med_sick(self):
        key_word = self.ui.lineEdit_45.text()
        cur,conn = self.connect_mysql()
        sql = 'select 门诊编号,姓名,状态 from 未发药病人信息表 where 门诊编号 like "%%%s%%" or 姓名 like "%%%s%%" ' %(key_word ,key_word )
        sql1 = 'select 门诊编号,姓名,状态 from 已发药病人信息表 where 门诊编号 like "%%%s%%" or 姓名 like "%%%s%%" ' %(key_word ,key_word )
        df = pd.read_sql(sql, conn)
        sick_text = np.array(df)
        df1 = pd.read_sql(sql1, conn)
        sick_text1 = np.array(df1)
        if len(sick_text) != 0:
            self.show(self.ui.tableWidget_13, sick_text, 3)
        elif len(sick_text1) != 0:
            self.show(self.ui.tableWidget_13, sick_text1, 3)
        else:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '查无此人！')
            msg_box.exec_()
        cur.close()
        conn.close()

    # 展示未发药列表
    def show_no_send_list(self):
        cur, conn = self.connect_mysql()
        sql = 'select 门诊编号,姓名,状态 from 未发药病人信息表'
        df = pd.read_sql(sql, conn)
        df2 = np.array(df)
        cur.close()
        conn.close()
        self.ui.tableWidget_13.setRowCount(0)  # 格式化行
        self.ui.tableWidget_13.setColumnCount(3)  # 格式化列
        for i in range(len(df2)):
            item = df2[i]
            row = self.ui.tableWidget_13.rowCount()
            self.ui.tableWidget_13.insertRow(row)
            for j in range(len(item)):
                item = QTableWidgetItem(str(df2[i][j]))
                self.ui.tableWidget_13.setItem(row, j, item)
                item.setTextAlignment(Qt.AlignCenter)

    # 展示已发药列表
    def show_send_sick_list(self):
        cur, conn = self.connect_mysql()
        sql = 'select 门诊编号,姓名,状态 from 已发药病人信息表'
        df = pd.read_sql(sql, conn)
        df2 = np.array(df)
        cur.close()
        conn.close()
        self.ui.tableWidget_13.setRowCount(0)  # 格式化行
        self.ui.tableWidget_13.setColumnCount(3)  # 格式化列
        for i in range(len(df2)):
            item = df2[i]
            row = self.ui.tableWidget_13.rowCount()
            self.ui.tableWidget_13.insertRow(row)
            for j in range(len(item)):
                item = QTableWidgetItem(str(df2[i][j]))
                self.ui.tableWidget_13.setItem(row, j, item)
                item.setTextAlignment(Qt.AlignCenter)

    # 发药确定
    def sick_get_med_sure(self):
        try:
            sick_num = self.ui.lineEdit_46.text()
            sick_name = self.ui.lineEdit_47.text()
            cur, conn = self.connect_mysql()
            sql = 'delete from 未发药病人信息表 where 门诊编号 = "%s"' % sick_num
            sql2 = 'select 所需药品 from 未发药病人信息表 where 门诊编号 = "%s"' % sick_num
            df = pd.read_sql(sql2, conn)
            text = np.array(df)
            need_med = text[0][0]
            rows = cur.execute(sql)
            conn.commit()
            state = '已发药'
            sql1 = 'insert into 已发药病人信息表(门诊编号,姓名,所需药品,状态) values ("%s","%s","%s","%s") ' % (sick_num, sick_name, need_med, state)
            rows1 = cur.execute(sql1)
            conn.commit()
            cur.close()
            conn.close()
            self.show_no_send_list()
            msg_box = QMessageBox(QMessageBox.Information, '提示', '取药成功！')
            msg_box.exec_()
        except:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '请选择未取药人员')
            msg_box.exec_()

    # 点击详情显示患者详细信息
    def key_text_clicked(self,row,col):
        text = self.ui.tableWidget_3.item(row,col).text()
        if text == "详情" :
            self.key_information(row)

    # 返回病人信息页面
    def back_sick_text_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    # 显示患者具体内容
    def key_information(self,row):
        try:
            self.ui.stackedWidget.setCurrentIndex(11)
            sick_num = self.ui.tableWidget_3.item(row,0).text()
            cur,conn = self.connect_mysql()
            sql = 'select 地址,过敏史 from 病人信息表 where 门诊编号 = "%s" '%sick_num
            df = pd.read_sql(sql,conn)
            text = np.array(df)
            self.ui.lineEdit_57.setText(self.ui.tableWidget_3.item(row,1).text())
            self.ui.lineEdit_58.setText(self.ui.tableWidget_3.item(row,2).text())
            self.ui.lineEdit_59.setText(self.ui.tableWidget_3.item(row,3).text())
            self.ui.lineEdit_60.setText(self.ui.tableWidget_3.item(row,4).text())
            self.ui.lineEdit_64.setText(text[0][0])  # 地址
            self.ui.lineEdit_61.setText(text[0][1])  # 过敏史
            self.ui.lineEdit_62.setText(self.ui.tableWidget_3.item(row,7).text())
            self.ui.lineEdit_63.setText(self.ui.tableWidget_3.item(row,8).text())
            self.ui.lineEdit_65.setText(self.ui.tableWidget_3.item(row,9).text())
            self.ui.lineEdit_68.setText(self.ui.tableWidget_3.item(row,6).text())
            sql1 = 'select 所需药品 from 已发药病人信息表 where 门诊编号 = "%s"'%sick_num
            sql2 = 'select 处方名称 from 已有处方信息表 '
            sql3 = 'select 药品名称 from 西药品信息表 '
            df1 = pd.read_sql(sql1,conn)
            df2 = pd.read_sql(sql2,conn)
            df3 = pd.read_sql(sql3,conn)
            med_need = np.array(df1)
            pre_name = np.array(df2)
            med_name = np.array(df3)
            pre = []
            for i in pre_name :
                pre.append(i[0])
            med = []
            for i in med_name :
                med.append(i[0])
            sick_need = med_need[0][0]
            str1 = re.sub("[\!\%\[\]\,\。]", "", sick_need)
            str2 = str1.replace("'", "")  # 去除单引号
            text1 = re.split(r'[\s:]+', str2.strip())
            need = []
            a = 0
            for i in range(len(text1)):
                for j in pre:
                    if text1[i] == j:
                        need.append(text1[i])
                        need.append("中药")
                        need.append(text1[i+1])
                        break
                    else:
                        a = 1
                if a == 1:
                    for n in med:
                        if text1[i] == n:
                            need.append(text1[i])
                            need.append("西药")
                            need.append(text1[i + 1])
            self.ui.tableWidget_16.setRowCount(0)  # 格式化行
            self.ui.tableWidget_16.setColumnCount(3)  # 格式化列
            x = 0
            for i in range(int(len(need)/3)):
                row = self.ui.tableWidget_16.rowCount()
                self.ui.tableWidget_16.insertRow(row)
                for j in range(3):
                    item = QTableWidgetItem(str(need[x]))
                    self.ui.tableWidget_16.setItem(row, j, item)
                    item.setTextAlignment(Qt.AlignCenter)
                    x += 1
            cur.close()
            conn.close()
        except:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '未知错误')
            msg_box.exec_()

    # 跳转挂号页面
    def reg_page(self):
        self.ui.stackedWidget.setCurrentIndex(12)

    # 展示账号信息
    def show_user(self):
        cur, conn = self.connect_mysql()
        sql = 'select * from 账号管理表'
        df = pd.read_sql(sql, conn)
        user_text = np.array(df)
        self.show(self.ui.tableWidget_15, user_text, 8)
        text = "删除"
        item = QTableWidgetItem(str(text))
        for i in range(len(user_text)):
            item = QTableWidgetItem(text)
            self.ui.tableWidget_15.setItem(i, 7, item)
            item.setFont(QFont('Times', 10, QFont.Black))
            item.setTextAlignment(Qt.AlignCenter)
        self.ui.lineEdit_48.clear()
        cur.close()
        conn.close()

    # 挂号信息采集
    def reg_text_add(self):
        try:
            cur, conn = self.connect_mysql()
            sql = ' select 门诊编号 from 挂号病人信息表 '
            df1 = pd.read_sql(sql , conn)
            num = np.array(df1)
            num_2 = num[-1][0]
            sick_text = [self.ui.lineEdit_66.text(),self.ui.lineEdit_67.text(),self.ui.lineEdit_69.text() ]
            fd = time.gmtime()
            act_time = time.strftime("%Y%m%d", fd)
            if act_time in num_2:
                a = int(num_2[9:10])
                a += 1
                if a <10:
                    sick_num = act_time + '0' + str(a)
                else:
                    sick_num = act_time + str(a)
            else:
                a = 1
                sick_num = sick_num = act_time + '0' + str(a)
            cur,conn = self.connect_mysql()
            sql = 'insert into 挂号病人信息表(门诊编号,姓名,年龄,电话) values ("%s","%s","%s","%s")' %(sick_num,sick_text[0],sick_text[1],sick_text[2])
            sql1 = 'insert into 候诊病人信息表(门诊编号,姓名,年龄,电话) values ("%s","%s","%s","%s")' %(sick_num,sick_text[0],sick_text[1],sick_text[2])
            rows = cur.execute(sql)
            conn.commit()
            rows1 = cur.execute(sql1)
            conn.commit()
            cur.close()
            conn.close()
            SI.reg_sick_symptom[sick_num] = self.ui.lineEdit_70.text()
            self.wait_sick_info()
            msg_box = QMessageBox(QMessageBox.Information, '提示', '挂号成功！')
            msg_box.exec_()
        except:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '有关键信息未填')
            msg_box.exec_()

    # 搜索账号
    def seek_user(self):
        key_word = self.ui.lineEdit_48.text()
        cur,conn = self.connect_mysql()
        sql = 'select * from 账号管理表 where 姓名 like "%%%s%%" or 联系方式 like "%%%s%%"'%(key_word ,key_word )
        df = pd.read_sql(sql,conn)
        user_text = np.array(df)
        self.show(self.ui.tableWidget_15, user_text, 8)
        text = "删除"
        item = QTableWidgetItem(str(text))
        for i in range(len(user_text)):
            item = QTableWidgetItem(text)
            self.ui.tableWidget_15.setItem(i, 7, item)
            item.setFont(QFont('Times', 10, QFont.Black))
        cur.close()
        conn.close()

    # 点击删除账号
    def clicked_delete_user(self,row,col):
        text = self.ui.tableWidget_15.item(row,col).text()
        if text == "删除":
            self.reply = QMessageBox(QMessageBox.Question, '删除', '确定删除？')
            yes = self.reply.addButton('确定', QMessageBox.YesRole)
            no = self.reply.addButton('取消', QMessageBox.NoRole)
            self.reply.show()
            self.reply.exec_()
            if self.reply.clickedButton() == yes:
                self.delete_user(row)

    # 删除函数
    def delete_user(self,row):
        print(self.ui.tableWidget_15.item(row,0).text())
        cur,conn = self.connect_mysql()
        sql = 'delete from 账号管理表 where 账号 = "%s"' %self.ui.tableWidget_15.item(row,0).text()
        sql1 = 'delete from 账号信息表 where 账号 = "%s"' %self.ui.tableWidget_15.item(row,0).text()
        rows = cur.execute(sql)
        conn.commit()
        rows1 = cur.execute(sql1)
        conn.commit()
        cur.close()
        conn.close()
        self.show_user()
        msg_box = QMessageBox(QMessageBox.Information, '提示', '删除成功！')
        msg_box.exec_()

    # 添加账号
    def add_user(self):
        user_text = [self.ui.lineEdit_55.text(),self.ui.lineEdit_49.text(),self.ui.lineEdit_50.text(),self.ui.lineEdit_52.text(),self.ui.lineEdit_51.text(),self.ui.lineEdit_53.text(),self.ui.lineEdit_54.text(),self.ui.lineEdit_56.text()]
        print(user_text)
        cur,conn = self.connect_mysql()
        sql = 'insert into 账号管理表(账号,姓名,性别,联系方式,角色,科别,备注) values ("%s","%s","%s","%s","%s","%s","%s")'%(user_text[0],user_text[1],user_text[2],user_text[3],user_text[4],user_text[5],user_text[6])
        sql1 = 'insert into 账号信息表(账号,密码) values ("%s","%s")'%(user_text[0],user_text[7])
        rows = cur.execute(sql)
        conn.commit()
        rows1 = cur.execute(sql1)
        conn.commit()
        cur.close()
        conn.close()
        self.show_user()
        msg_box = QMessageBox(QMessageBox.Information, '提示', '添加成功！')
        msg_box.exec_()

    # 清空内容
    def clear_user_text(self):
        self.ui.lineEdit_49.clear()
        self.ui.lineEdit_50.clear()
        self.ui.lineEdit_51.clear()
        self.ui.lineEdit_53.clear()
        self.ui.lineEdit_52.clear()
        self.ui.lineEdit_54.clear()
        self.ui.lineEdit_55.clear()
        self.ui.lineEdit_56.clear()

    # 医生信息页面
    def doctor_page(self):
        self.ui.stackedWidget.setCurrentIndex(13)

    # 展示函数
    def show_doctor(self,sql):
        cur, conn = self.connect_mysql()
        df = pd.read_sql(sql, conn)
        doctor_text = np.array(df)
        self.show(self.ui.tableWidget_17, doctor_text, 5)
        text = "详情"
        item = QTableWidgetItem(str(text))
        for i in range(len(doctor_text)):
            item = QTableWidgetItem(text)
            self.ui.tableWidget_17.setItem(i, 4, item)
            item.setFont(QFont('Times', 10, QFont.Black))
            item.setTextAlignment(Qt.AlignCenter)
        cur.close()
        conn.close()

    # 展示医生信息
    def show_doctor_text(self):
        sql = 'select 姓名,年龄,电话,科室 from 医生信息表'
        self.show_doctor(sql)

    # 搜索医生
    def seek_doctor(self):
        key_word = self.ui.lineEdit_71.text()
        print(key_word )
        sql = 'select 姓名,年龄,电话,科室 from 医生信息表 where 姓名 like "%%%s%%"' %key_word
        self.show_doctor(sql)

    # 跳转医生详情页面
    def doctor_text_page(self,row,col):
        text = self.ui.tableWidget_17.item(row,col).text()
        if text == "详情" :
            cur, conn = self.connect_mysql()
            sql = 'select 生涯,职位 from 医生信息表 where 姓名 = "%s"' % self.ui.tableWidget_17.item(row,0).text()
            df = pd.read_sql(sql, conn)
            doctor_text = np.array(df)
            self.ui.lineEdit_72.setText(self.ui.tableWidget_17.item(row,0).text())
            self.ui.lineEdit_73.setText(self.ui.tableWidget_17.item(row,1).text())
            self.ui.lineEdit_74.setText(self.ui.tableWidget_17.item(row,2).text())
            self.ui.lineEdit_75.setText(self.ui.tableWidget_17.item(row,3).text())
            self.ui.lineEdit_76.setText(doctor_text[0][1])
            self.ui.textEdit.setText(doctor_text[0][0])
            self.ui.stackedWidget.setCurrentIndex(14)

    # lineEdit跳转
    def lineEdit_change(self):
        self.ui.lineEdit_16.returnPressed.connect(self.ui.lineEdit_17.setFocus)
        self.ui.lineEdit_17.returnPressed.connect(self.ui.lineEdit_15.setFocus)
        self.ui.lineEdit_15.returnPressed.connect(self.ui.lineEdit_14.setFocus)
        self.ui.lineEdit_14.returnPressed.connect(self.ui.lineEdit_37.setFocus)
        self.ui.lineEdit_32.returnPressed.connect(self.ui.lineEdit_33.setFocus)
        self.ui.lineEdit_33.returnPressed.connect(self.ui.lineEdit_34.setFocus)
        self.ui.lineEdit_34.returnPressed.connect(self.ui.lineEdit_35.setFocus)
        self.ui.lineEdit_35.returnPressed.connect(self.ui.lineEdit_8.setFocus)
        self.ui.lineEdit_24.returnPressed.connect(self.ui.lineEdit_19.setFocus)
        self.ui.lineEdit_19.returnPressed.connect(self.ui.lineEdit_20.setFocus)
        self.ui.lineEdit_20.returnPressed.connect(self.ui.lineEdit_22.setFocus)
        self.ui.lineEdit_22.returnPressed.connect(self.ui.lineEdit_23.setFocus)
        self.ui.lineEdit_23.returnPressed.connect(self.ui.lineEdit_18.setFocus)
        self.ui.lineEdit_18.returnPressed.connect(self.ui.lineEdit_21.setFocus)
        self.ui.lineEdit_21.returnPressed.connect(self.ui.textEdit_2.setFocus)
        self.ui.lineEdit_49.returnPressed.connect(self.ui.lineEdit_50.setFocus)
        self.ui.lineEdit_50.returnPressed.connect(self.ui.lineEdit_52.setFocus)
        self.ui.lineEdit_52.returnPressed.connect(self.ui.lineEdit_51.setFocus)
        self.ui.lineEdit_51.returnPressed.connect(self.ui.lineEdit_53.setFocus)
        self.ui.lineEdit_53.returnPressed.connect(self.ui.lineEdit_54.setFocus)
        self.ui.lineEdit_54.returnPressed.connect(self.ui.lineEdit_55.setFocus)
        self.ui.lineEdit_55.returnPressed.connect(self.ui.lineEdit_56.setFocus)
        self.ui.lineEdit_66.returnPressed.connect(self.ui.lineEdit_67.setFocus)
        self.ui.lineEdit_67.returnPressed.connect(self.ui.lineEdit_69.setFocus)
        self.ui.lineEdit_69.returnPressed.connect(self.ui.lineEdit_70.setFocus)
        self.ui.lineEdit_4.returnPressed.connect(self.ui.lineEdit_5.setFocus)
        self.ui.lineEdit_5.returnPressed.connect(self.ui.lineEdit_3.setFocus)
        self.ui.lineEdit_3.returnPressed.connect(self.ui.lineEdit_6.setFocus)
        self.ui.lineEdit_6.returnPressed.connect(self.ui.lineEdit_10.setFocus)
        self.ui.lineEdit_81.returnPressed.connect(self.ui.lineEdit_82.setFocus)
        self.ui.lineEdit_82.returnPressed.connect(self.ui.lineEdit_83.setFocus)
        self.ui.lineEdit_77.returnPressed.connect(self.ui.lineEdit_78.setFocus)
        self.ui.lineEdit_78.returnPressed.connect(self.ui.lineEdit_80.setFocus)

    # 处方模板页面
    def pre_form_page(self):
        form = QDialog()
        form.resize(300, 500)
        verticalLayout = QtWidgets.QVBoxLayout(form)
        verticalLayout.setObjectName("verticalLayout")
        tableWidget = QtWidgets.QTableWidget(form)
        tableWidget.setObjectName("tableWidget")
        tableWidget.setColumnCount(2)
        tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        tableWidget.setHorizontalHeaderItem(1, item)
        verticalLayout.addWidget(tableWidget)
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("Form", "处方模板"))
        item = tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "名称"))
        item = tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "处方类别"))
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        cur, conn = self.connect_mysql()
        sql = 'select 名称,处方类别 from 处方模板信息表'
        df = pd.read_sql(sql, conn)
        form_name = np.array(df)
        self.show(tableWidget, form_name, 2)
        SI.History_ill = tableWidget
        tableWidget.cellPressed.connect(self.get_form)
        form.exec_()

    # 点击处方模板
    def get_form(self, row, col):
        name = SI.History_ill.item(row, 0).text()  # 点击处方名获得文本
        self.reply = QMessageBox(QMessageBox.Information, '提示', '请选择:')
        yes = self.reply.addButton('合并', QMessageBox.YesRole)
        no = self.reply.addButton('覆盖', QMessageBox.NoRole)
        self.reply.show()
        self.reply.exec_()
        if self.reply.clickedButton() == no:
            self.ui.tableWidget_2.clear()
            self.ui.tableWidget_10.clear()
        cur, conn = self.connect_mysql()
        sql = 'select 处方类别,医嘱,处方 from 处方模板信息表 where 名称 = "%s"' % name
        df = pd.read_sql(sql, conn)
        text = np.array(df)
        doctor_word = text[0][1]
        pre_form = text[0][0]
        self.ui.lineEdit_38.setText(doctor_word)
        str1 = re.sub("[\!\%\[\]\,\。]", "", text[0][2])
        str2 = str1.replace("'", "")  # 去除单引号
        text1 = re.split(r'[\s:]+', str2.strip())
        if pre_form == "西药处方":
            self.west_pre()
            count = len(text1) / 6
            x = 0
            for i in range(int(count)):
                row = self.ui.tableWidget_10.rowCount()
                self.ui.tableWidget_10.insertRow(row)
                for j in range(6):
                    item = QTableWidgetItem(text1[x])
                    x += 1
                    self.ui.tableWidget_10.setItem(row, j, item)
                    item.setTextAlignment(Qt.AlignCenter)
        else:
            self.east_pre()
            count = len(text1) / 5
            x = 0
            for i in range(int(count)):
                row = self.ui.tableWidget_2.rowCount()
                self.ui.tableWidget_2.insertRow(row)
                for j in range(5):
                    item = QTableWidgetItem(text1[x])
                    x += 1
                    self.ui.tableWidget_2.setItem(row, j, item)
                    item.setTextAlignment(Qt.AlignCenter)

    # 显示处方模板
    def show_pre_form(self):
        cur,conn = self.connect_mysql()
        sql = 'select 名称,处方类别,医嘱,创建日期,标签 from 处方模板信息表'
        df1 = pd.read_sql(sql,conn)
        form_text = np.array(df1)
        self.show(self.ui.tableWidget_18,form_text,5)
        cur.close()
        conn.close()

    # 删除处方模板
    def delete_form(self):
        try:
            self.reply = QMessageBox(QMessageBox.Information, '提示', '是否删除')
            yes = self.reply.addButton('删除', QMessageBox.YesRole)
            no = self.reply.addButton('取消', QMessageBox.NoRole)
            self.reply.show()
            self.reply.exec_()
            if self.reply.clickedButton() == yes:
                row = self.ui.tableWidget_18.currentRow()  # 获取当前选中的行
                form_name = self.ui.tableWidget_18.item(row,0).text()
                cur,conn = self.connect_mysql()
                sql = 'delete from 处方模板信息表 where 名称 = "%s" '% form_name
                cur.execute(sql)
                conn.commit()
                cur.close()
                conn.close()
                self.show_pre_form()
        except:
            asg = QMessageBox(QMessageBox.Information,"提示","请选择要删除的模板")
            asg.exec_()

    # 模板搜索
    def seek_pre_form(self):
        cur,conn = self.connect_mysql()
        key_word = self.ui.lineEdit_41.text()
        sql = 'select 名称,处方类别,医嘱,创建日期 from 处方模板信息表 where 名称 like "%%%s%%"' %key_word
        df1 = pd.read_sql(sql, conn)
        form_text = np.array(df1)
        if len(form_text) != 0:
            self.show(self.ui.tableWidget_18, form_text, 4)
        else:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '没有查询到改模板！')
            msg_box.exec_()
        cur.close()
        conn.close()

    # 选择中药或西药处方模板
    def change_form(self):
        data = self.ui.comboBox_2.currentText()
        cur, conn = self.connect_mysql()
        if data == "中药处方" or data == "西药处方":
            sql = 'select 名称,处方类别,医嘱,创建日期,标签 from 处方模板信息表 where 处方类别 = "%s"'%data
        else:
            sql = 'select 名称,处方类别,医嘱,创建日期,标签 from 处方模板信息表'
        df1 = pd.read_sql(sql, conn)
        form_text = np.array(df1)
        self.show(self.ui.tableWidget_18, form_text, 5)
        cur.close()
        conn.close()

    # 添加模板
    def add_form(self):
        self.reply = QMessageBox(QMessageBox.Information, '提示', '请选择要添加的模板')
        yes = self.reply.addButton('中药模板', QMessageBox.YesRole)
        no = self.reply.addButton('西药模板', QMessageBox.NoRole)
        self.reply.show()
        self.reply.exec_()
        if self.reply.clickedButton() == yes:
            self.ui.stackedWidget.setCurrentIndex(16)
            if self.ui.tableWidget_19.item(0, 0) == None:
                self.ui.tableWidget_19.setRowCount(0)
                self.ui.tableWidget_19.setColumnCount(5)
                self.ui.tableWidget_19.setHorizontalHeaderLabels(['处方名', '方剂数', '频次/天', '单价/元', '总价/元'])
                pre_name = self.connect_mysql_prescription()  # 连接到处方库并将处方名转换为列表
                ls = ['']
                for i in pre_name:
                    ls.append(i[0])
                self.ui.comboBox_9.clear()
                self.ui.comboBox_9.addItems(ls)
        elif self.reply.clickedButton() == no:
            self.ui.stackedWidget.setCurrentIndex(17)
            if self.ui.tableWidget_20.item(0, 0) == None:
                self.ui.tableWidget_20.setRowCount(0)
                self.ui.tableWidget_20.setColumnCount(6)
                self.ui.tableWidget_20.setHorizontalHeaderLabels(['药品名', '数量', '规格', '频次/天', '单价/元', '总价/元'])
                cur, conn = self.connect_mysql()
                sql = 'select 药品名称,规格 from 西药品信息表'
                df = pd.read_sql(sql, conn)
                med_name = np.array(df)
                ls = ['']
                for i in med_name:
                    ls.append(i[0])
                self.ui.comboBox_10.clear()
                self.ui.comboBox_10.addItems(ls)

    # 添加中药模板
    def add_east_form(self):
        form_name = self.ui.lineEdit_77.text()
        form_label = self.ui.lineEdit_80.text()
        form_text = self.ui.lineEdit_78.text()
        form_kind = "中药处方"
        column = self.ui.tableWidget_19.columnCount()  # 获取当前表格共有多少列
        row = self.ui.tableWidget_19.rowCount()  # 获取当前表格共有多少行
        pre_text = []
        for i in range(row):
            for j in range(column):
                pre_text.append(self.ui.tableWidget_19.item(i, j).text())
        fd = time.gmtime()
        act_time = time.strftime("%Y/%m/%d %H:%M:%S", fd)
        cur,conn = self.connect_mysql()
        sql = 'insert into 处方模板信息表(名称,处方类别,医嘱,创建日期,处方,标签) values ("%s","%s","%s","%s","%s","%s")'%(form_name,form_kind ,form_text,act_time  ,pre_text,form_label )
        rows = cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        asg = QMessageBox(QMessageBox.Information,"提示","保存成功！")
        asg.exec_()
        self.show_pre_form()

    # 添加西药模板
    def add_west_form(self):
        form_name = self.ui.lineEdit_81.text()
        form_label = self.ui.lineEdit_83.text()
        form_text = self.ui.lineEdit_82.text()
        form_kind = "西药处方"
        column1 = self.ui.tableWidget_20.columnCount()  # 获取当前表格共有多少列
        row1 = self.ui.tableWidget_20.rowCount()  # 获取当前表格共有多少行
        med_text = []
        for i in range(row1):
            for j in range(column1):
                med_text.append(self.ui.tableWidget_20.item(i, j).text())
        fd = time.gmtime()
        act_time = time.strftime("%Y/%m/%d %H:%M:%S", fd)
        cur, conn = self.connect_mysql()
        sql = 'insert into 处方模板信息表(名称,处方类别,医嘱,创建日期,处方,标签) values ("%s","%s","%s","%s","%s","%s")' % (
        form_name, form_kind, form_text, act_time, med_text, form_label)
        rows = cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        asg = QMessageBox(QMessageBox.Information, "提示", "保存成功！")
        asg.exec_()
        self.show_pre_form()

    # 添加中药
    def form_add_east_pre(self):
        try:
            pre_text = self.ui.comboBox_9.currentText()
            cur, conn = self.connect_mysql()
            sql = 'select 价格 from 已有处方信息表 where 处方名称 = "%s" ' % pre_text
            df = pd.read_sql(sql, conn)
            pre = np.array(df)
            num = self.ui.lineEdit_79.text()
            all_cost = int(num) * int(pre[0][0])
            row = self.ui.tableWidget_19.rowCount()
            self.ui.tableWidget_19.insertRow(row)
            item = QTableWidgetItem(str(pre_text))
            item1 = QTableWidgetItem(str(pre[0][0]))
            item2 = QTableWidgetItem(str(all_cost))
            item3 = QTableWidgetItem(str(num))
            self.ui.tableWidget_19.setItem(row,0,item)
            self.ui.tableWidget_19.setItem(row,1,item3)
            self.ui.tableWidget_19.setItem(row,3,item1)
            self.ui.tableWidget_19.setItem(row,4,item2)
            cur.close()
            conn.close()
        except:
            msg_box = QMessageBox(QMessageBox.Information, "提示", "请输入有效信息")
            msg_box.exec_()

    # 添加西药
    def form_add_west_pre(self):
        try:
            med_text = self.ui.comboBox_10.currentText()
            med_num = self.ui.lineEdit_84.text()
            cur, conn = self.connect_mysql()
            sql = 'select 规格,价格 from 西药品信息表 where 药品名称 = "%s" '%med_text
            df = pd.read_sql(sql, conn)
            med = np.array(df)
            all_cost = int(med_num) * int(med[0][1])
            row = self.ui.tableWidget_20.rowCount()
            self.ui.tableWidget_20.insertRow(row)
            item = QTableWidgetItem(str(med_text))
            item2 = QTableWidgetItem(str(med_num))
            item4 = QTableWidgetItem(str(all_cost))
            item1 = QTableWidgetItem(str(med[0][0]))
            item3 = QTableWidgetItem(str(med[0][1]))
            self.ui.tableWidget_20.setItem(row, 0, item)
            self.ui.tableWidget_20.setItem(row, 1, item2)
            self.ui.tableWidget_20.setItem(row, 2, item1)
            self.ui.tableWidget_20.setItem(row, 4, item3)
            self.ui.tableWidget_20.setItem(row, 5, item4)
            cur.close()
            conn.close()
        except:
            msg_box = QMessageBox(QMessageBox.Information, "提示", "请输入有效信息")
            msg_box.exec_()

    # 添加新的过敏史、既往史、遗传史
    def ill_add(self):
        cur, conn = self.connect_mysql()
        sql = 'select * from 过敏史信息表'
        sql1 = 'select * from 既往史信息表'
        sql2 = 'select * from 遗传史信息表'
        df = pd.read_sql(sql,conn)
        df1 = pd.read_sql(sql1,conn)
        df2 = pd.read_sql(sql2,conn)
        ls = np.array(df)
        ls1 = np.array(df1)
        ls2= np.array(df2)
        AllItems = []
        AllItems1 = []
        AllItems2 = []
        for i in ls :
            AllItems.append(i[0])
        for i in ls1:
            AllItems1.append(i[0])
        for i in ls2:
            AllItems2.append(i[0])
        text = self.ui.comboBox.lineEdit().text()
        text1 = self.ui.comboBox_7.lineEdit().text()
        text2 = self.ui.comboBox_8.lineEdit().text()
        sql = ' insert into 过敏史信息表 values ("%s")' % text
        sql1 = ' insert into 既往史信息表 values ("%s")' % text1
        sql2 = ' insert into 遗传史信息表 values ("%s")' % text2
        if self.ui.comboBox.lineEdit().text() not in AllItems and self.ui.comboBox.lineEdit().text() != '':
            rows = cur.execute(sql)
            conn.commit()
        if self.ui.comboBox_7.lineEdit().text() not in AllItems1 and self.ui.comboBox_7.lineEdit().text() != '':
            rows = cur.execute(sql1)
            conn.commit()
        if self.ui.comboBox_8.lineEdit().text() not in AllItems2 and self.ui.comboBox_8.lineEdit().text() != '':
            rows = cur.execute(sql2)
            conn.commit()
        conn.commit()
        cur.close()
        conn.close()

    # 显示过敏史、既往史、遗传史
    def show_ill_history(self):
        cur,conn = self.connect_mysql()
        sql = 'select * from 过敏史信息表'
        sql1 = 'select * from 既往史信息表'
        sql2 = 'select * from 遗传史信息表'
        df = pd.read_sql(sql,conn)
        df1 = pd.read_sql(sql1,conn)
        df2 = pd.read_sql(sql2,conn)
        name_text = np.array(df)
        name_text1 = np.array(df1)
        name_text2 = np.array(df2)
        name_1 = []
        name_2 = []
        name_3 = []
        for i in name_text :
            name_1.append(i[0])
        for i in name_text1:
            name_2.append(i[0])
        for i in name_text2:
            name_3.append(i[0])
        self.ui.comboBox.clear()
        self.ui.comboBox_7.clear()
        self.ui.comboBox_8.clear()
        self.ui.comboBox.addItems(name_1)
        self.ui.comboBox_7.addItems(name_2)
        self.ui.comboBox_8.addItems(name_3)
        self.ui.comboBox.setCurrentIndex(-1)
        self.ui.comboBox_7.setCurrentIndex(-1)
        self.ui.comboBox_8.setCurrentIndex(-1)

    # 在设置中展示过敏史、既往史、遗传史
    def show_ill_setting(self):
        cur, conn = self.connect_mysql()
        sql = 'select * from 过敏史信息表'
        sql1 = 'select * from 既往史信息表'
        sql2 = 'select * from 遗传史信息表'
        df = pd.read_sql(sql, conn)
        df1 = pd.read_sql(sql1, conn)
        df2 = pd.read_sql(sql2, conn)
        name_text = np.array(df)
        name_text1 = np.array(df1)
        name_text2 = np.array(df2)
        name_1 = []
        name_2 = []
        name_3 = []
        for i in name_text:
            name_1.append(i[0])
        for i in name_text1:
            name_2.append(i[0])
        for i in name_text2:
            name_3.append(i[0])
        self.ui.listWidget.addItems(name_1)
        self.ui.listWidget_2.addItems(name_2)
        self.ui.listWidget_3.addItems(name_3)

    # 添加过敏史
    def add_allergy_ill(self):
        key_word = self.ui.lineEdit_85.text()
        cur, conn = self.connect_mysql()
        sql = 'select * from 过敏史信息表'
        df = pd.read_sql(sql, conn)
        name_text = np.array(df)
        name_1 = []
        for i in name_text:
            name_1.append(i[0])
        if key_word not in name_1 :
            sql1 = 'insert into 过敏史信息表 values ("%s")' % key_word
            cur.execute(sql1)
            conn.commit()
            cur.close()
            conn.close()
            self.ui.listWidget.clear()
            self.ui.listWidget_2.clear()
            self.ui.listWidget_3.clear()
            self.show_ill_setting()
            asg = QMessageBox(QMessageBox.Information, "提示", "添加成功")
            asg.exec_()
        else:
            asg = QMessageBox(QMessageBox.Information, "提示", "添加重复")
            asg.exec_()

    # 添加既往史
    def add_past_ill(self):
        key_word = self.ui.lineEdit_86.text()
        cur, conn = self.connect_mysql()
        sql = 'select * from 既往史信息表'
        df = pd.read_sql(sql, conn)
        name_text = np.array(df)
        name_1 = []
        for i in name_text:
            name_1.append(i[0])
        if key_word not in name_1:
            sql1 = 'insert into 既往史信息表 values ("%s")' % key_word
            cur.execute(sql1)
            conn.commit()
            cur.close()
            conn.close()
            self.ui.listWidget.clear()
            self.ui.listWidget_2.clear()
            self.ui.listWidget_3.clear()
            self.show_ill_setting()
            asg = QMessageBox(QMessageBox.Information, "提示", "添加成功")
            asg.exec_()

        else:
            asg = QMessageBox(QMessageBox.Information, "提示", "添加重复")
            asg.exec_()

    # 添加遗传史
    def add_heredity_ill(self):
        key_word = self.ui.lineEdit_87.text()
        cur, conn = self.connect_mysql()
        sql = 'select * from 遗传史信息表'
        df = pd.read_sql(sql, conn)
        name_text = np.array(df)
        name_1 = []
        for i in name_text:
            name_1.append(i[0])
        if key_word not in name_1:
            sql1 = 'insert into 遗传史信息表 values ("%s")' % key_word
            cur.execute(sql1)
            conn.commit()
            cur.close()
            conn.close()
            self.ui.listWidget.clear()
            self.ui.listWidget_2.clear()
            self.ui.listWidget_3.clear()
            self.show_ill_setting()
            asg = QMessageBox(QMessageBox.Information, "提示", "添加成功")
            asg.exec_()
        else:
            asg = QMessageBox(QMessageBox.Information, "提示", "添加重复")
            asg.exec_()

    # 历史病历页面
    def history_ill_page(self):
        form = QDialog()
        form.resize(400, 630)
        verticalLayout = QtWidgets.QVBoxLayout(form)
        verticalLayout.setObjectName("verticalLayout")
        tableWidget = QtWidgets.QTableWidget(form)
        tableWidget.setObjectName("tableWidget")
        tableWidget.setColumnCount(2)
        tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        tableWidget.setHorizontalHeaderItem(1, item)
        verticalLayout.addWidget(tableWidget)
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("Form", "历史病历"))
        item = tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "姓名"))
        item = tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "日期"))
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        key_word = self.ui.lineEdit.text()
        cur, conn = self.connect_mysql()
        sql = ' select 姓名,接诊时间 from 病人信息表 where 姓名 = "%s"' % key_word
        df = pd.read_sql(sql, conn)
        text = np.array(df)
        self.show(tableWidget, text, 2)
        SI.History_ill  = tableWidget
        tableWidget.cellPressed.connect(self.get_name)
        form.exec_()

    # 点击历史病历
    def get_name(self, row, col):  # 获得处方名
        name = SI.History_ill.item(row, 0).text()  # 点击处方名获得文本
        time = SI.History_ill.item(row, 1).text()  # 点击处方名获得文本
        self.sick_ill_text_show(name,time)

    # 展示病人病历详情
    def  sick_ill_text_show(self,name,time):
        try:
            cur, conn = self.connect_mysql()
            sql = 'select 门诊编号,姓名,性别,年龄,手机号,地址,过敏史,既往病史,遗传病史,诊断,医生 from 病人信息表 where 姓名 = "%s" and 接诊时间 = "%s"'%(name,time)
            df = pd.read_sql(sql,conn)
            text = np.array(df)
            SI.mainWin.ui.show()
            self.ui.stackedWidget.setCurrentIndex(11)
            self.ui.lineEdit_57.setText(text[0][1])
            self.ui.lineEdit_58.setText(text[0][2])
            self.ui.lineEdit_59.setText(text[0][3])
            self.ui.lineEdit_60.setText(text[0][4])
            self.ui.lineEdit_64.setText(text[0][5])
            self.ui.lineEdit_61.setText(text[0][6])
            self.ui.lineEdit_62.setText(text[0][7])
            self.ui.lineEdit_63.setText(text[0][8])
            self.ui.lineEdit_65.setText(text[0][9])
            self.ui.lineEdit_68.setText(text[0][10])
            sql1 = 'select 所需药品 from 已发药病人信息表 where 门诊编号 = "%s"' % text[0][0]
            sql2 = 'select 处方名称 from 已有处方信息表 '
            sql3 = 'select 药品名称 from 西药品信息表 '
            df1 = pd.read_sql(sql1, conn)
            df2 = pd.read_sql(sql2, conn)
            df3 = pd.read_sql(sql3, conn)
            med_need = np.array(df1)
            pre_name = np.array(df2)
            med_name = np.array(df3)
            pre = []
            for i in pre_name:
                pre.append(i[0])
            med = []
            for i in med_name:
                med.append(i[0])
            sick_need = med_need[0][0]
            str1 = re.sub("[\!\%\[\]\,\。]", "", sick_need)
            str2 = str1.replace("'", "")  # 去除单引号
            text1 = re.split(r'[\s:]+', str2.strip())
            need = []
            a = 0
            for i in range(len(text1)):
                for j in pre:
                    if text1[i] == j:
                        need.append(text1[i])
                        need.append("中药")
                        need.append(text1[i + 1])
                        break
                    else:
                        a = 1
                if a == 1:
                    for n in med:
                        if text1[i] == n:
                            need.append(text1[i])
                            need.append("西药")
                            need.append(text1[i + 1])
            self.ui.tableWidget_16.setRowCount(0)  # 格式化行
            self.ui.tableWidget_16.setColumnCount(3)  # 格式化列
            x = 0
            for i in range(int(len(need) / 3)):
                row = self.ui.tableWidget_16.rowCount()
                self.ui.tableWidget_16.insertRow(row)
                for j in range(3):
                    item = QTableWidgetItem(str(need[x]))
                    self.ui.tableWidget_16.setItem(row, j, item)
                    item.setTextAlignment(Qt.AlignCenter)
                    x += 1
            cur.close()
            conn.close()
        except:
            asg = QMessageBox(QMessageBox.Information ,"提示","未知错误！")
            asg.exec_()

    # 返回模板设置页面
    def back_set_page(self):
        self.ui.stackedWidget.setCurrentIndex(15)

    # 帮助页面切换
    def help_page(self,item):
        if item.text() == '挂号':
            self.ui.stackedWidget_3.setCurrentIndex(0)
        elif item.text() == '接诊':
            self.ui.stackedWidget_3.setCurrentIndex(1)
        elif item.text() == '收费与发药':
            self.ui.stackedWidget_3.setCurrentIndex(2)
        elif item.text() == '患者信息':
            self.ui.stackedWidget_3.setCurrentIndex(3)
        elif item.text() == '供货单位管理':
            self.ui.stackedWidget_3.setCurrentIndex(4)
        elif item.text() == '药品管理':
            self.ui.stackedWidget_3.setCurrentIndex(5)
        elif item.text() == '处方模板设置':
            self.ui.stackedWidget_3.setCurrentIndex(6)
        elif item.text() == '处方生成':
            self.ui.stackedWidget_3.setCurrentIndex(7)



if __name__ == '__main__':
    app = QApplication([])
    SI.loginWin = Win_Login()
    SI.loginWin.ui.show()
    app.exec_()
