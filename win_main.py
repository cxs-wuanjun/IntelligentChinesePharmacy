from PyQt5.QtGui import QFont, QPixmap, QIcon, QPalette, QBrush
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from PyQt5 import QtCore
from utils.public_variable import SI
from subsystem import supplier_manage as sm
from subsystem import chinese_medicine_manage as cmm
from subsystem import prescription_manage as pm
from utils import mysql_tools


# 主界面
class WinMain(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('ui_file/win_main.ui', self)  # 主界面
        # self.ui.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.printer = QPrinter()  # 打印
        SI.printer = self.printer
        SI.ui = self.ui
        self.counter = 1  # 记录菜单初始状态
        self.ui.menu_change.clicked.connect(self.menu_hide)
        self.ui.treeWidget.clicked.connect(self.change_page)  # 页面切换
        self.supplier_function()  # 供货单位部分函数
        self.med_function()  # 药材管理部分函数
        self.pre_create_function()  # 处方管理部分函数
        self.home_page()  # 首页
        self.user_info()  # 账号
        self.img_insert()  # 图片插入
        self.change_background()  # 选择背景
        self.ui.btn_exit.clicked.connect(self.exit_win)  # 退出
        self.background_setting()

    # 监听窗口大小变化
    def resizeEvent(self, event):
        sql = "select content from setting_label where label='bg_label'"
        file_label = mysql_tools.get_mysql_data(sql)
        if file_label[0][0] == '1':
            file_load = 'res_img/米白背景.png'
        elif file_label[0][0] == '2':
            file_load = 'res_img/背景.png'
        elif file_label[0][0] == '3':
            file_load = 'res_img/背景02.png'
        else:
            file_load = 'res_img/背景.png'
        self.setting_bg(file_load)

    # 首页
    def home_page(self):
        self.ui.pushButton.clicked.connect(self.buttonClicked)
        self.ui.pushButton_2.clicked.connect(self.buttonClicked)
        self.ui.pushButton_3.clicked.connect(self.buttonClicked)
        self.ui.pushButton_4.clicked.connect(self.buttonClicked)
        self.ui.pushButton_5.clicked.connect(self.buttonClicked)
        self.ui.pushButton_6.clicked.connect(self.buttonClicked)
        self.ui.pushButton_7.clicked.connect(self.buttonClicked)
        self.ui.pushButton_8.clicked.connect(self.buttonClicked)
        self.ui.pushButton_9.clicked.connect(self.buttonClicked)
        self.ui.pushButton_10.clicked.connect(self.buttonClicked)
        self.ui.pushButton_11.clicked.connect(self.buttonClicked)
        self.ui.pushButton_12.clicked.connect(self.buttonClicked)

    # 页面切换
    def buttonClicked(self):
        # 获取发出信号的按钮对象
        sender = self.sender()
        if isinstance(sender, QPushButton):
            button = sender
            if button is not None:
                # 确定哪个按钮被按下
                if button == self.ui.pushButton or button == self.ui.pushButton_6:
                    self.ui.stackedWidget.setCurrentIndex(2)
                elif button == self.ui.pushButton_2 or button == self.ui.pushButton_9:
                    self.ui.stackedWidget.setCurrentIndex(1)
                elif button == self.ui.pushButton_3 or button == self.ui.pushButton_7:
                    self.ui.stackedWidget.setCurrentIndex(3)
                elif button == self.ui.pushButton_4 or button == self.ui.pushButton_8:
                    self.ui.stackedWidget.setCurrentIndex(0)
                elif button == self.ui.pushButton_5 or button == self.ui.pushButton_10:
                    self.ui.stackedWidget.setCurrentIndex(5)
                elif button == self.ui.pushButton_11:
                    self.ui.stackedWidget.setCurrentIndex(6)
                elif button == self.ui.pushButton_12:
                    self.ui.stackedWidget.setCurrentIndex(4)

    # 页面切换
    def change_page(self):
        i = self.ui.treeWidget.currentItem()
        if i.text(0) == '药材管理':
            self.ui.stackedWidget.setCurrentIndex(0)
        elif i.text(0) == '供货单位管理':
            self.ui.stackedWidget.setCurrentIndex(1)
        elif i.text(0) == '处方生成':
            self.ui.stackedWidget.setCurrentIndex(3)
        elif i.text(0) == '已有处方' or i.text(0) == '处方管理':
            self.ui.stackedWidget.setCurrentIndex(2)
        elif i.text(0) == '首页':
            self.ui.stackedWidget.setCurrentIndex(4)
        elif i.text(0) == '帮助':
            self.ui.stackedWidget.setCurrentIndex(6)
        elif i.text(0) == '设置' or i.text(0) == '基础设置':
            self.ui.stackedWidget.setCurrentIndex(5)

    # 处方生成部分函数
    def pre_create_function(self):
        pm.show_prescription()  # 展示处方
        self.ui.tableWidget_6.cellPressed.connect(pm.get_prescription_name)  # 点击返回处方名称
        self.ui.tableWidget_8.cellPressed.connect(pm.get_medicine_name)  # 点击返回药材名称
        self.ui.btn_add_row.clicked.connect(pm.add_row)  # 点击添加一行表格
        self.ui.btn_delete_4.clicked.connect(pm.delete_pre)  # 删除处方
        self.ui.btn_seek_2.clicked.connect(pm.select_pre)  # 查找处方
        self.ui.lineEdit_26.returnPressed.connect(pm.select_pre)  # 回车查找
        self.ui.btn_update_1.clicked.connect(pm.show_prescription)  # 更新处方
        pm.show_medicine()  # 处方生成里药材展示
        self.ui.btn_seek_3.clicked.connect(pm.select_medicine)  # 查找药材
        self.ui.lineEdit_29.returnPressed.connect(pm.select_medicine)  # 回车查找
        self.ui.btn_update_2.clicked.connect(pm.show_medicine)  # 更新药材
        self.ui.btn_create_2.clicked.connect(pm.creat_prescription)  # 生成处方
        self.ui.lineEdit_28.returnPressed.connect(pm.creat_prescription)  # 回车生成
        self.ui.btn_taboo.clicked.connect(pm.pre_taboo)  # 禁忌
        self.ui.btn_clear_1.clicked.connect(pm.clear_textEdit)  # 清空处方文本
        self.ui.btn_create_3.clicked.connect(pm.pre_text)  # 点击详情
        self.ui.lineEdit_27.setFont(QFont("黑体", 16))
        self.ui.lineEdit_27.setAlignment(QtCore.Qt.AlignCenter)

    # 供货单位部分函数
    def supplier_function(self):
        sm.show_supplier()  # 展示供货单位
        self.ui.btn_updata_1.clicked.connect(sm.show_supplier)  # 更新供货单位
        self.ui.btn_create_1.clicked.connect(sm.add_supplier)  # 添加供货单位
        self.ui.tableWidget_5.cellPressed.connect(sm.get_supplier_name)  # 点击返回企业名称
        self.ui.btn_delete_2.clicked.connect(sm.delete_supplier)  # 删除企业
        self.ui.btn_seek_1.clicked.connect(sm.seek_supplier)  # 查找企业
        self.ui.lineEdit_25.returnPressed.connect(sm.seek_supplier)  # 回车查找
        self.ui.btn_delete_1.clicked.connect(sm.empty_supplier_text)  # 清空企业文本

    # 药材管理部分函数
    def med_function(self):
        cmm.show_med()  # 展示药材
        self.ui.btn_add_2.clicked.connect(cmm.add_chinese_med)  # 添加药材
        self.ui.btn_select_med_3.clicked.connect(cmm.select_chinese_med)  # 查找药材
        self.ui.lineEdit_32.returnPressed.connect(cmm.select_chinese_med)  # 回车查找
        self.ui.btn_delete_5.clicked.connect(cmm.empty_med_text)  # 清空药材文本
        self.ui.qr_code_btn.clicked.connect(cmm.qr_code)  # 生成二维码
        self.ui.bar_code_btn.clicked.connect(cmm.bar_code)  # 生成二维码
        self.ui.qr_bar_print_btn.clicked.connect(cmm.print_fun)  # 打印条码

    # 菜单隐藏
    def menu_hide(self):
        # 更换图片
        if self.counter == 0:
            self.ui.menu_change.setIcon(QIcon('res_img/左箭头.png'))
            self.counter = 1
            # 获取当前的QTreeWidget的可见性状态
            is_visible = self.ui.treeWidget.isVisible()
            # 设置QTreeWidget的可见性状态为相反的值
            self.ui.treeWidget.setVisible(not is_visible)
        else:
            self.ui.menu_change.setIcon(QIcon('res_img/右箭头.png'))
            self.counter = 0
            # 获取当前的QTreeWidget的可见性状态
            is_visible = self.ui.treeWidget.isVisible()
            # 设置QTreeWidget的可见性状态为相反的值
            self.ui.treeWidget.setVisible(not is_visible)

    # 帮助部分函数
    def help_function(self):
        self.ui.listWidget_4.itemClicked.connect(self.help_page)

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

    # lineEdit跳转
    def lineEdit_change(self):
        self.ui.lineEdit_16.returnPressed.connect(self.ui.lineEdit_17.setFocus)
        self.ui.lineEdit_17.returnPressed.connect(self.ui.lineEdit_15.setFocus)
        self.ui.lineEdit_15.returnPressed.connect(self.ui.lineEdit_14.setFocus)
        self.ui.lineEdit_14.returnPressed.connect(self.ui.lineEdit_37.setFocus)
        self.ui.lineEdit_24.returnPressed.connect(self.ui.lineEdit_19.setFocus)
        self.ui.lineEdit_19.returnPressed.connect(self.ui.lineEdit_20.setFocus)
        self.ui.lineEdit_20.returnPressed.connect(self.ui.lineEdit_22.setFocus)
        self.ui.lineEdit_22.returnPressed.connect(self.ui.lineEdit_23.setFocus)
        self.ui.lineEdit_23.returnPressed.connect(self.ui.lineEdit_18.setFocus)
        self.ui.lineEdit_18.returnPressed.connect(self.ui.lineEdit_21.setFocus)
        self.ui.lineEdit_21.returnPressed.connect(self.ui.textEdit_2.setFocus)

    # 图片插入
    def img_insert(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./res_img/中药.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.setWindowIcon(icon)  # 主界面标题

        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("./res_img/左箭头.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.menu_change.setIcon(icon5)  # 隐藏菜单

        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("./res_img/加.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.btn_add_row.setIcon(icon6)  # 处方生成添加表格行数

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./res_img/首页.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.treeWidget.topLevelItem(0).setIcon(0, icon1)  # 首页

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./res_img/中药 (2).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.treeWidget.topLevelItem(1).setIcon(0, icon2)  # 药材管理

        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("./res_img/fill_处方单.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.treeWidget.topLevelItem(2).setIcon(0, icon3)  # 处方管理

        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("./res_img/设置.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.treeWidget.topLevelItem(3).setIcon(0, icon4)  # 设置

        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("./res_img/退出.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.btn_exit.setIcon(icon7)

        self.ui.label_9.setPixmap(QPixmap('res_img/米白背景.png'))
        self.ui.label_9.setScaledContents(True)  # 拉伸图片填充标签
        self.ui.label_10.setPixmap(QPixmap('res_img/背景.png'))
        self.ui.label_10.setScaledContents(True)  # 拉伸图片填充标签
        self.ui.label_11.setPixmap(QPixmap('res_img/背景02.png'))
        self.ui.label_11.setScaledContents(True)  # 拉伸图片填充标签

        self.ui.label_13.setPixmap(QtGui.QPixmap("./res_img/help_dcoument.png"))  # 帮助文档

    def exit_win(self):
        self.ui.close()
        SI.loginWin.ui.show()
        SI.loginWin.ui.show()
        try:
            SI.userInfo.ui.close()
        except Exception as e:
            pass

    # 账号信息
    def user_info(self):
        self.ui.toolButton.setIcon(QIcon('res_img/群蜂账号管理.png'))
        ID = 'ID:' + SI.user_id
        self.ui.toolButton.setToolTip(ID)
        self.ui.toolButton.setPopupMode(QToolButton.InstantPopup)

        # 创建一个菜单，并将菜单项添加到其中
        menu = QMenu(self)
        account_info_action = QAction('账号信息', self)
        account_info_action.triggered.connect(self.user_info_all)
        settings_action = QAction('设置', self)
        settings_action.triggered.connect(self.setting_page)  # 设置
        quit_action = QAction('退出', self)
        quit_action.triggered.connect(self.exit_win)  # 退出
        # 创建样式表
        style = """
        QAction { 
            color: blue; 
            background-color: lightgray; 
            border-radius: 10px;
        } 
        """

        # 设置样式表
        menu.setStyleSheet(style)
        menu.addAction(account_info_action)
        menu.addAction(settings_action)
        menu.addAction(quit_action)

        # 设置菜单
        self.ui.toolButton.setMenu(menu)

    # 跳到设置页面
    def setting_page(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    # 账号详细信息
    def user_info_all(self):
        SI.userInfo = UserInfo()
        SI.userInfo.ui.show()

    # 背景切换
    def change_background(self):
        self.ui.buttonGroup = QButtonGroup()
        self.ui.buttonGroup.addButton(self.ui.radioButton)
        self.ui.buttonGroup.addButton(self.ui.radioButton_2)
        self.ui.buttonGroup.addButton(self.ui.radioButton_3)
        self.ui.buttonGroup.buttonClicked.connect(self.select_background)
        self.ui.buttonGroup_1 = QButtonGroup()
        self.ui.buttonGroup_1.addButton(self.ui.radioButton_4)
        self.ui.buttonGroup_1.addButton(self.ui.radioButton_5)
        self.ui.buttonGroup_1.buttonClicked.connect(self.menu_setting)

    def select_background(self, radioButton):
        if radioButton == self.ui.radioButton:
            cur, conn = mysql_tools.connect_mysql()
            sql = "update tcm.setting_label set content=1 where label='bg_label'"
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            file_load = 'res_img/米白背景.png'
            self.setting_bg(file_load)
        elif radioButton == self.ui.radioButton_2:
            cur, conn = mysql_tools.connect_mysql()
            sql = "update tcm.setting_label set content=2"
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            file_load = 'res_img/背景.png'
            self.setting_bg(file_load)
        elif radioButton == self.ui.radioButton_3:
            cur, conn = mysql_tools.connect_mysql()
            sql = "update tcm.setting_label set content=3 where label='bg_label'"
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            file_load = 'res_img/背景02.png'
            self.setting_bg(file_load)

    # 基础设置的按钮位置
    def background_setting(self):
        sql = "select content from setting_label where label='bg_label'"
        bg_label = mysql_tools.get_mysql_data(sql)
        sql1 = "select content from setting_label where label='menu_label'"
        menu_label = mysql_tools.get_mysql_data(sql1)
        if bg_label[0][0] == '1':
            self.ui.radioButton.setChecked(True)
        elif bg_label[0][0] == '2':
            self.ui.radioButton_2.setChecked(True)
        elif bg_label[0][0] == '3':
            self.ui.radioButton_3.setChecked(True)
        if menu_label[0][0] == '1':
            self.ui.radioButton_4.setChecked(True)
            self.ui.widget_2.setVisible(False)  # 隐藏上方
            self.ui.widget_3.setVisible(True)  # 显示左侧
        elif menu_label[0][0] == '2':
            self.ui.radioButton_5.setChecked(True)
            self.ui.widget_3.setVisible(False)  # 隐藏左侧
            self.ui.widget_2.setVisible(True)  # 显示上方

    # 菜单栏设置
    def menu_setting(self, radioButton):
        if radioButton == self.ui.radioButton_4:
            sql = "update tcm.setting_label set content = '1' where label='menu_label'"
            cur, conn = mysql_tools.connect_mysql()
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            self.ui.widget_2.setVisible(False)  # 隐藏上方
            self.ui.widget_3.setVisible(True)   # 显示左侧
        elif radioButton == self.ui.radioButton_5:
            sql = "update tcm.setting_label set content = '2' where label='menu_label'"
            cur, conn = mysql_tools.connect_mysql()
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            self.ui.widget_3.setVisible(False)  # 隐藏左侧
            self.ui.widget_2.setVisible(True)   # 显示上方

    # 设置背景函数
    def setting_bg(self, file_load):
        bg_image_scaled = QPixmap(file_load).scaled(self.ui.width(), self.ui.height())
        brush = QBrush(bg_image_scaled)
        # 设置背景色为背景图片
        palette = self.palette()
        palette.setBrush(QPalette.Background, brush)
        self.ui.setAutoFillBackground(True)
        self.ui.setPalette(palette)


class UserInfo(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui_file/user_info.ui")
        self.show_info()  # 展示信息
        self.ui.btn_update_password.clicked.connect(self.update_password)  # 更改密码
        self.bg_setting()  # 背景
        self.ui.pushButton.clicked.connect(lambda: self.show_password(self.ui.lineEdit_18, self.ui.pushButton))
        self.ui.pushButton_2.clicked.connect(lambda: self.show_password(self.ui.lineEdit_19, self.ui.pushButton_2))
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.close())

    # 信息显示
    def show_info(self):
        sql = "select user_name, user_phone from user_info where user_id='%s'" % SI.user_id
        user_info = mysql_tools.get_mysql_data(sql)
        self.ui.lineEdit_16.setText(user_info[0][0])
        self.ui.lineEdit_17.setText(user_info[0][1])
        self.ui.label_25.setText(SI.user_id)

    # 密码更改
    def update_password(self):
        old_password = self.ui.lineEdit_18.text()
        new_password = self.ui.lineEdit_19.text()
        sql = "select user_password from user_data where user_id='%s'" % SI.user_id
        user_password = mysql_tools.get_mysql_data(sql)
        if old_password == user_password[0][0]:
            sql1 = "update tcm.user_data set user_password='%s' where user_id='%s'" % (new_password, SI.user_id)
            cur, conn = mysql_tools.connect_mysql()
            cur.execute(sql1)
            conn.commit()
            cur.close()
            conn.close()
            msg_box = QMessageBox(QMessageBox.Information, '提示', "更改成功！")
            msg_box.exec_()
        else:
            msg_box = QMessageBox(QMessageBox.Information, '提示', "原密码错误！")
            msg_box.exec_()

    # 背景
    def bg_setting(self):
        self.ui.label.setPixmap(QtGui.QPixmap("./res_img/古风01.jpeg"))
        self.ui.label.setScaledContents(True)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./res_img/退出.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pushButton_3.setIcon(icon)

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./res_img/不显示.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pushButton.setIcon(icon1)

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./res_img/不显示.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pushButton_2.setIcon(icon2)

        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("./res_img/群蜂账号管理.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.setWindowIcon(icon5)

    # 密码显示
    def show_password(self, lineEdit, pushButton):
        if lineEdit.echoMode() == QLineEdit.Password:
            icon3 = QtGui.QIcon()
            icon3.addPixmap(QtGui.QPixmap("./res_img/密码显示.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            pushButton.setIcon(icon3)
            lineEdit.setEchoMode(QLineEdit.Normal)
        else:
            icon4 = QtGui.QIcon()
            icon4.addPixmap(QtGui.QPixmap("./res_img/不显示.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            pushButton.setIcon(icon4)
            lineEdit.setEchoMode(QLineEdit.Password)
