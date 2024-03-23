import re
import traceback
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from utils.public_variable import SI
from win_main import WinMain
from manager_win import ManagerWin
from utils import mysql_tools


# 登录界面
class WinLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ui_file/welcome.ui")
        self.determine_user()  # 判断是否有记住的账号
        self.ui.btn_login.clicked.connect(self.onSignIn_pre)   # 登录主界面
        self.ui.btn_manager.clicked.connect(self.onSignIn_manager)  # 登录管理员页面
        self.ui.btn_login_2.clicked.connect(self.login_user)   # 注册
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.close())  # 关闭登录页面
        self.ui.pushButton.clicked.connect(self.show_password)  # 密码显示
        self.ui.checkBox.toggled.connect(self.remember_user)  # 记住账号
        self.lineEdit_change()
        self.img_insert()

    # 判断是否有被记住的账号
    def determine_user(self):
        sql = "select id, password from login_remember where user = 'user'"
        user_data = mysql_tools.get_mysql_data(sql)
        if user_data[0][0]:
            self.ui.lineEdit_3.setText(str(user_data[0][0]))
            self.ui.lineEdit_2.setText(str(user_data[0][1]))

    # 登陆主界面
    def onSignIn_pre(self):
        try:
            user_id = self.ui.lineEdit_3.text()
            user_password = self.ui.lineEdit_2.text()
            sql = 'select user_id, user_password from user_data'
            user_info = mysql_tools.get_mysql_data(sql)
            log_label = 0
            if not user_id or not user_password:
                msg_box = QMessageBox(QMessageBox.Information, '提示', '请输入账号或密码！')
                msg_box.exec_()
            else:
                for i in user_info:
                    if user_id == i[0]:
                        if user_id == i[0] and user_password == i[1]:
                            SI.user_id = user_id
                            SI.mainWin = WinMain()
                            SI.mainWin.ui.show()
                            self.ui.close()
                            log_label = 1
                        else:
                            log_label = 2
                            msg_box = QMessageBox(QMessageBox.Information, '提示', '账号或密码错误')
                            msg_box.exec_()
            if log_label == 0:
                msg_box = QMessageBox(QMessageBox.Information, '提示', '账号或密码错误')
                msg_box.exec_()

        except Exception as e:
            # 访问异常的错误编号和详细信息
            print(e.args)
            print(str(e))
            print(repr(e))
            print(traceback.format_exc())
            print('Failed to load icon, using fallback icon')
            msg_box = QMessageBox(QMessageBox.Information, '提示', '账号或密码错误')
            msg_box.exec_()

    def onSignIn_manager(self):
        try:
            SI.AdLogWin = Log()
            SI.AdLogWin.ui.show()

        except Exception as e:
            print(repr(e))

    def lineEdit_change(self):
        self.ui.lineEdit_3.returnPressed.connect(self.ui.lineEdit_2.setFocus)
        self.ui.lineEdit_2.returnPressed.connect(self.onSignIn_pre)
        self.ui.lineEdit_12.returnPressed.connect(self.ui.lineEdit_7.setFocus)
        self.ui.lineEdit_7.returnPressed.connect(self.ui.lineEdit_11.setFocus)
        self.ui.lineEdit_11.returnPressed.connect(self.ui.lineEdit_6.setFocus)
        self.ui.lineEdit_6.returnPressed.connect(self.ui.lineEdit_8.setFocus)

    # 记住账号功能
    def remember_user(self):
        if self.ui.checkBox.isChecked():
            user_id = self.ui.lineEdit_3.text()
            user_password = self.ui.lineEdit_2.text()
            sql = 'select user_id, user_password from user_data'
            user_info = mysql_tools.get_mysql_data(sql)
            counter = 0
            if not user_id or not user_password:
                msg_box = QMessageBox(QMessageBox.Information, '提示', '请输入账号或密码！')
                msg_box.exec_()
            else:
                for i in user_info:
                    if user_id == i[0]:
                        if user_id == i[0] and user_password == i[1]:
                            counter = 1
                        else:
                            msg_box = QMessageBox(QMessageBox.Information, '提示', '账号或密码错误')
                            msg_box.exec_()
            if counter == 1:
                cur, conn = mysql_tools.connect_mysql()
                sql1 = "update tcm.login_remember set id = '%s', password = '%s' where user = 'user'" % (user_id, user_password)
                cur.execute(sql1)
                conn.commit()
                cur.close()
                conn.close()
            else:
                msg_box = QMessageBox(QMessageBox.Information, '提示', '账号或密码错误')
                msg_box.exec_()

    # 背景设置
    def img_insert(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./res_img/中药.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.setWindowIcon(icon)  # 主界面标题
        self.ui.label_4.setPixmap(QtGui.QPixmap("./res_img/山水.jpeg"))
        self.ui.label_4.setScaledContents(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./res_img/退出.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pushButton_3.setIcon(icon1)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./res_img/不显示.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pushButton.setIcon(icon2)

    # 密码显示
    def show_password(self):
        if self.ui.lineEdit_2.echoMode() == QLineEdit.Password:
            icon3 = QtGui.QIcon()
            icon3.addPixmap(QtGui.QPixmap("./res_img/密码显示.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton.setIcon(icon3)
            self.ui.lineEdit_2.setEchoMode(QLineEdit.Normal)
        else:
            icon4 = QtGui.QIcon()
            icon4.addPixmap(QtGui.QPixmap("./res_img/不显示.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton.setIcon(icon4)
            self.ui.lineEdit_2.setEchoMode(QLineEdit.Password)

    # 注册
    def login_user(self):
        user_name = self.ui.lineEdit_12.text()
        user_phone = self.ui.lineEdit_7.text()
        user_notes = self.ui.lineEdit_11.text()
        user_id = self.ui.lineEdit_6.text()
        user_password = self.ui.lineEdit_8.text()
        if self.ui.radioButton_3.isChecked():
            user_sex = "男"
        else:
            user_sex = "女"
        if not user_notes:
            user_notes = '无'
        info = [user_id, user_password, user_name, user_sex, user_phone]
        info_1 = ['账号', '密码', '姓名', '性别', '手机号']
        text = "请填写"
        counter = 0
        for num, i in enumerate(info):
            if not i:
                text = text + info_1[num] + '、'
                counter += 1
        text = text[0:-1]
        text = text + '!'
        phone_regex = re.compile(r'^1[3-9]\d{9}$')
        sql = "select user_id, user_phone from user_data"
        user_info = mysql_tools.get_mysql_data(sql)
        if phone_regex.match(user_phone):  # 是否是手机号
            counter = 6
        for i in user_info:
            if user_id in i:  # id重复
                counter = 7
            if user_phone in i:  # 手机号已注册
                counter = 8
        if counter == 0:
            cur, conn = mysql_tools.connect_mysql()
            sql = "insert into user_info(user_id, user_name, user_sex, user_phone, notes) values ('%s', '%s', '%s', " \
                  "'%s', '%s')" % (user_id, user_name, user_sex, user_phone, user_notes)
            rows = cur.execute(sql)
            sql1 = "insert into user_data(user_id, user_password, user_phone, notes) values ('%s', '%s', '%s', " \
                   "'%s')" % (user_id, user_password, user_phone, user_notes)
            rows = cur.execute(sql1)
            conn.commit()
            cur.close()
            conn.close()
            msg_box = QMessageBox(QMessageBox.Information, '提示', '添加成功！')
            msg_box.exec_()
            self.ui.lineEdit_3.setText(user_id)
            self.ui.lineEdit_2.setText(user_password)
            self.ui.tabWidget.setCurrentWidget(self.ui.tab_2)
        elif counter == 6:
            msg_box = QMessageBox(QMessageBox.Information, '提示', "请输入正确的手机号")
            msg_box.exec_()
        elif counter == 7:
            msg_box = QMessageBox(QMessageBox.Information, '提示', "账号id重复，请更改")
            msg_box.exec_()
        elif counter == 8:
            msg_box = QMessageBox(QMessageBox.Information, '提示', "该手机号已注册")
            msg_box.exec_()
        else:
            msg_box = QMessageBox(QMessageBox.Information, '提示', text)
            msg_box.exec_()

    # close
    def close_logWin(self):
        self.ui.close()


class Log(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = self.ui = uic.loadUi("ui_file/log.ui")
        self.ui.pushButton.clicked.connect(self.ensure_password)  # 确认密码
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.close())   # 退出
        self.ui.pushButton_3.clicked.connect(self.show_password)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./res_img/群蜂账号管理.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.setWindowIcon(icon)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("./res_img/不显示.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pushButton_3.setIcon(icon3)

    # 密码显示
    def show_password(self):
        if self.ui.lineEdit_2.echoMode() == QLineEdit.Password:
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap("./res_img/密码显示.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_3.setIcon(icon1)
            self.ui.lineEdit_2.setEchoMode(QLineEdit.Normal)
        else:
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap("./res_img/不显示.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.pushButton_3.setIcon(icon2)
            self.ui.lineEdit_2.setEchoMode(QLineEdit.Password)

    # 密码判断
    def ensure_password(self):
        data = self.ui.lineEdit_2.text()
        sql = "select password from administrators_password where administrator='tcm'"
        password = mysql_tools.get_mysql_data(sql)
        if data:
            if int(data) == int(password[0][0]):
                SI.managerWin = ManagerWin()
                SI.managerWin.ui.show()
                SI.loginWin.ui.close()
                self.ui.close()
            else:
                msg_box = QMessageBox(QMessageBox.Information, '提示', "密码错误！")
                msg_box.exec_()
        else:
            msg_box = QMessageBox(QMessageBox.Information, '提示', "请输入密码！")
            msg_box.exec_()


if __name__ == '__main__':
    app = QApplication([])
    SI.loginWin = WinLogin()
    SI.loginWin.ui.show()
    app.exec_()
