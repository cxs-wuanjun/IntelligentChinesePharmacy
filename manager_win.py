from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui, QtCore
from utils import mysql_tools, pyqt_tools
from utils.public_variable import SI


class ManagerWin(QWidget):
    def __init__(self):
        super(ManagerWin, self).__init__()
        self.ui = uic.loadUi("ui_file/user_manage.ui")
        self.show_user()  # 展示账号信息
        self.ui.btn_seek_user.clicked.connect(self.seek)  # 查找
        self.ui.lineEdit_48.returnPressed.connect(self.seek)  # 回车查找
        self.ui.btn_add_user.clicked.connect(self.add_user)  # 添加账号
        self.jump_lineEdit()  # lineEdit 跳转
        self.ui.btn_clear_user.clicked.connect(self.clear_all)  # 清空
        self.img_insert()
        self.ui.btn_exit.clicked.connect(self.exit_win)  # 退出
        self.ui.pushButton_2.clicked.connect(self.view_password)  # 查看管理员密码
        self.ui.pushButton.clicked.connect(self.change_password)  # 修改管理员密码

    # 背景设置
    def img_insert(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./res_img/群蜂账号管理.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.setWindowIcon(icon)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("./res_img/退出.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.btn_exit.setIcon(icon7)

        self.ui.label.setPixmap(QtGui.QPixmap("./res_img/背景01.jpeg"))
        # self.ui.movie = QMovie("./res_img/水墨.gif")
        #
        # # 将动画设置为自动播放并循环播放
        # self.ui.movie.setCacheMode(QMovie.CacheAll)
        # self.ui.movie.setSpeed(100)
        # self.ui.movie.setScaledSize(self.ui.label.size())
        # self.ui.movie.start()
        #
        # # 将QMovie对象设置为QLabel的背景
        # self.ui.label.setMovie(self.ui.movie)

    # 退出
    def exit_win(self):
        self.ui.close()
        SI.loginWin.ui.show()

    # 管理员密码查看
    def view_password(self):
        sql = "select password from administrators_password where administrator='tcm'"
        data = mysql_tools.get_mysql_data(sql)
        self.ui.lineEdit_2.setText(data[0][0])

    # 管理员密码修改
    def change_password(self):
        data = self.ui.lineEdit.text()
        sql = "update tcm.administrators_password set password='%s' where administrator='tcm'" % data
        print(sql)
        cur, conn = mysql_tools.connect_mysql()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        msg_box = QMessageBox(QMessageBox.Information, '提示', '修改成功！')
        msg_box.exec_()

    # 展示已有账号信息
    def show_user(self):
        sql = 'select * from user_info'
        user_data = mysql_tools.get_mysql_data(sql)

        self.ui.tableWidget_15.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget_15.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 账号信息表格禁止编辑
        self.ui.lineEdit_2.setReadOnly(True)  # 密码查看只读

        pyqt_tools.show_widget(self.ui.tableWidget_15, user_data, 6, label=3)

    # 查找
    def seek(self):
        key_text = self.ui.lineEdit_48.text()
        sql = "select * from user_info where user_name like '%%%s%%' or user_id like '%%%s%%' or user_phone like" \
              "'%%%s%%'" % (key_text, key_text, key_text)
        user_data = mysql_tools.get_mysql_data(sql)
        pyqt_tools.show_widget(self.ui.tableWidget_15, user_data, 6, label=3)

    # 添加账号
    def add_user(self):
        reply = QMessageBox(QMessageBox.Question, '提交', '确定添加？')
        yes = reply.addButton('确定', QMessageBox.YesRole)
        no = reply.addButton('取消', QMessageBox.NoRole)
        reply.show()
        reply.exec_()
        if reply.clickedButton() == yes:
            user_name = self.ui.lineEdit_49.text()
            user_phone = self.ui.lineEdit_52.text()
            notes = self.ui.lineEdit_54.text()
            user_id = self.ui.lineEdit_55.text()
            user_password = self.ui.lineEdit_56.text()
            if self.ui.radioButton.isChecked():
                user_sex = "男"
            else:
                user_sex = "女"

            cur, conn = mysql_tools.connect_mysql()
            sql = "insert into user_info(user_id, user_name, user_sex, user_phone, notes) values ('%s', '%s', '%s', " \
                  "'%s', '%s')" % (user_id, user_name, user_sex, user_phone, notes)
            rows = cur.execute(sql)
            sql1 = "insert into user_data(user_id, user_password, user_phone, notes) values ('%s', '%s', '%s', " \
                   "'%s')" % (user_id, user_password, user_phone, notes)
            rows = cur.execute(sql1)
            conn.commit()
            cur.close()
            conn.close()

            self.show_user()
            msg_box = QMessageBox(QMessageBox.Information, '提示', '添加成功！')
            msg_box.exec_()

    # linEdit跳转
    def jump_lineEdit(self):
        self.ui.lineEdit_49.returnPressed.connect(self.ui.lineEdit_52.setFocus)
        self.ui.lineEdit_52.returnPressed.connect(self.ui.lineEdit_54.setFocus)
        self.ui.lineEdit_54.returnPressed.connect(self.ui.lineEdit_55.setFocus)
        self.ui.lineEdit_55.returnPressed.connect(self.ui.lineEdit_56.setFocus)

    # 清空
    def clear_all(self):
        self.ui.lineEdit_49.clear()
        self.ui.lineEdit_52.clear()
        self.ui.lineEdit_54.clear()
        self.ui.lineEdit_55.clear()
        self.ui.lineEdit_56.clear()
