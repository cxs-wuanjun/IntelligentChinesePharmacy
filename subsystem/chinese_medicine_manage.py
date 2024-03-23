import qrcode
import time
from PyQt5.QtPrintSupport import QPageSetupDialog
from utils import mysql_tools
from utils import pyqt_tools
from utils.public_variable import SI
from PyQt5.QtWidgets import QMessageBox, QHeaderView, QAbstractItemView
from pystrich.ean13 import EAN13Encoder
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtPrintSupport import QPrinter


# 展示药材
def show_med():
    sql = 'select * from med_data'
    med_data = mysql_tools.get_mysql_data(sql)
    SI.ui.tableWidget_4.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    SI.ui.tableWidget_4.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 药材表格禁止编辑
    pyqt_tools.show_widget(SI.ui.tableWidget_4, med_data, 8, label=2)


# 添加药材
def add_chinese_med():
    reply = QMessageBox(QMessageBox.Question, '添加', '确定添加？')
    yes = reply.addButton('确定', QMessageBox.YesRole)
    no = reply.addButton('取消', QMessageBox.NoRole)
    reply.show()
    reply.exec_()
    if reply.clickedButton() == yes:
        ls = [SI.ui.lineEdit_16.text(), SI.ui.lineEdit_17.text(), SI.ui.lineEdit_15.text(),
              SI.ui.lineEdit_14.text(), SI.ui.lineEdit_37.text()]
        cur, conn = mysql_tools.connect_mysql()
        sql = "insert into med_data(med_name, med_type, current_inventory, notes, med_price) values ('%s', '%s', " \
              "'%s', '%s', '%s')" % (
                  ls[0], ls[1], ls[2], ls[3], ls[4])
        try:
            rows = cur.execute(sql)
        except Exception as e:
            print(str(e))
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请按要求输入！')
            msg_box.exec_()
        conn.commit()
        cur.close()
        conn.close()
        ls.clear()
        show_med()


# 点击获得药材名称
def get_med_name(row, col):
    try:
        content = SI.ui.tableWidget_4.item(row, 0).text()
        SI.med_name_text = content
    except Exception as e:
        # 访问异常的错误编号和详细信息
        print(e.args)
        print(str(e))
        print(repr(e))
        msg_box = QMessageBox(QMessageBox.Information, '提示', '选中内容为空！')
        msg_box.exec_()


# 查找药材
def select_chinese_med():  # 查找药材
    text = SI.ui.lineEdit_32.text()
    sql = "select * from med_data where med_name like '%%%s%%' or med_type like '%%%s%%'" % (text, text)
    med_text = mysql_tools.get_mysql_data(sql)
    if med_text:
        pyqt_tools.show_widget(SI.ui.tableWidget_4, med_text, 8, label=2)
    else:
        msg_box = QMessageBox(QMessageBox.Information, '提示', '无该药材！')
        msg_box.exec_()


# 药材信息清空
def empty_med_text():
    SI.ui.lineEdit_14.clear()
    SI.ui.lineEdit_15.clear()
    SI.ui.lineEdit_16.clear()
    SI.ui.lineEdit_17.clear()
    SI.ui.lineEdit_37.clear()


# 二维码生成
def qr_code():
    t = time.gmtime()
    current_time = time.strftime("%Y一%m-%d %H : %M : %S", t)
    med_data = {"药材名称": SI.ui.lineEdit_16.text(),
                "药材类型": SI.ui.lineEdit_17.text(),
                "数量": SI.ui.lineEdit_15.text(),
                "备注": SI.ui.lineEdit_14.text(),
                "价格": SI.ui.lineEdit_37.text(),
                "入库时间": current_time}
    med_name = med_data["药材名称"]
    if med_name:
        sql = "select med_name from med_data"
        data = mysql_tools.get_mysql_data(sql)
        med_name_data = []
        for i in data:
            med_name_data.append(i[0])
        if med_name in med_name_data:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '已有该药材二维码！')
            msg_box.exec_()
        else:
            img = qrcode.make(med_data)
            file_load = 'img/qr_code/%s.png' % SI.ui.lineEdit_16.text()
            img.save(file_load)
            new_img = img_suit(file_load, SI.ui.label_3)
            pixmap = QPixmap(new_img)  # 按指定路径找到图片
            SI.ui.label_3.setPixmap(pixmap)  # 在label上显示图片
            SI.ui.label_3.setScaledContents(True)  # 让图片自适应label大小
    else:
        msg_box = QMessageBox(QMessageBox.Information, '提示', '请输入相关信息！')
        msg_box.exec_()


# 条形码生成
def bar_code():
    t = time.gmtime()
    current_time = time.strftime("%Y%m%d", t)
    num_12 = '693' + current_time
    ver_num = ean_num(int(num_12))
    num = num_12 + str(ver_num)
    med_name = SI.ui.lineEdit_16.text()
    if med_name:
        sql = "select med_name from med_data"
        data = mysql_tools.get_mysql_data(sql)
        med_name_data = []
        for i in data:
            med_name_data.append(i[0])
        if med_name in med_name_data:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '已有该药材条形码！')
            msg_box.exec_()
        else:
            encoder = EAN13Encoder(num)
            file_load = 'img/bar_code/%s.png' % med_name
            encoder.save(file_load)
            new_img = img_suit(file_load, SI.ui.label_2)
            pixmap = QPixmap(new_img)  # 按指定路径找到图片
            SI.ui.label_2.setPixmap(pixmap)  # 在label上显示图片
            SI.ui.label_2.setScaledContents(True)  # 让图片自适应label大小
    else:
        msg_box = QMessageBox(QMessageBox.Information, '提示', '请输入相关信息！')
        msg_box.exec_()


def ean_num(num):  # 条形码最后一位校验位
    odd_num = 0  # 从右开始，奇数个
    even_num = 0  # 从右开始， 偶数个
    for i in range(12):
        if i % 2 == 0:
            odd_num = odd_num + num % 10
            num = int(num / 10)
        else:
            even_num = even_num + num % 10
            num = int(num / 10)
    ver_num = 10 - (odd_num * 3 + even_num) % 10
    return ver_num


# 图片大小适应label
def img_suit(img, label):
    image = QPixmap()
    image.load(img)
    width = image.width()  # 获取图片宽度
    height = image.height()  # 获取图片高度
    if width / label.width() >= height / label.height():  # 比较图片宽度与label宽度之比和图片高度与label高度之比
        ratio = width / label.width()
    else:
        ratio = height / label.height()
    new_width = width / ratio  # 定义新图片的宽和高
    new_height = height / ratio
    new_img = image.scaled(new_width, new_height)  # 调整图片尺寸
    return new_img


# 打印函数
def print_fun():
    try:
        reply = QMessageBox(QMessageBox.Information, '提示', '打印选择')
        qr_btn = reply.addButton('二维码打印', QMessageBox.AcceptRole)
        bar_btn = reply.addButton('条形码打印', QMessageBox.AcceptRole)
        cancel_btn = reply.addButton('取消', QMessageBox.AcceptRole)
        reply.show()
        reply.exec_()
        if reply.clickedButton() == qr_btn:
            reply = QMessageBox(QMessageBox.Information, '提示', '打印二维码')
            print_setting = reply.addButton('打印设置', QMessageBox.YesRole)
            printer_btn = reply.addButton('打印', QMessageBox.NoRole)
            reply.show()
            reply.exec_()
            if reply.clickedButton() == print_setting:
                show_print_setting()
            elif reply.clickedButton() == printer_btn:
                show_print(SI.ui.label_3)
        elif reply.clickedButton() == bar_btn:
            reply = QMessageBox(QMessageBox.Information, '提示', '打印条形码')
            print_setting = reply.addButton('打印设置', QMessageBox.YesRole)
            printer_btn = reply.addButton('打印', QMessageBox.NoRole)
            reply.show()
            reply.exec_()
            if reply.clickedButton() == print_setting:
                show_print_setting()
            elif reply.clickedButton() == printer_btn:
                show_print(SI.ui.label_2)
        else:
            pass
    except Exception as e:
        print(1)
        print(repr(e))


# 显示打印设置
def show_print_setting():
    try:
        printDialog = QPageSetupDialog(SI.printer)
        printDialog.exec()
    except Exception as e:
        print(e.args)
        print(str(e))
        print(repr(e))


# 显示打印对话框
def show_print(label):
    try:
        # 创建打印机对象
        printer = QPrinter()
        # 设置打印机参数
        printer.setPageSize(QPrinter.A4)
        printer.setOrientation(QPrinter.Portrait)
        printer.setPageMargins(10, 10, 10, 10, QPrinter.Millimeter)
        # 创建画家对象
        painter = QPainter()
        painter.begin(printer)
        # 绘制图像
        pixmap = label.pixmap()
        painter.drawPixmap(0, 0, pixmap)
        # 结束绘制
        painter.end()
    except Exception as e:
        print(e.args)
        print(str(e))
        print(repr(e))


if __name__ == '__main__':
    bar_code()
