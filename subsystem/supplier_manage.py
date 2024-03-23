from utils import mysql_tools
from utils import pyqt_tools
from utils.public_variable import SI
from PyQt5.QtWidgets import QMessageBox, QHeaderView, QAbstractItemView


# 展示供货单位
def show_supplier():
    sql = 'select * from supplier_data'
    supplier_data = mysql_tools.get_mysql_data(sql)
    SI.ui.tableWidget_5.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    SI.ui.tableWidget_5.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 供货单位表格禁止编辑
    pyqt_tools.show_widget(SI.ui.tableWidget_5, supplier_data, 9, label=1)


# 添加供货单位
def add_supplier():
    reply = QMessageBox(QMessageBox.Question, '提交', '确定提交？')
    yes = reply.addButton('确定', QMessageBox.YesRole)
    no = reply.addButton('取消', QMessageBox.NoRole)
    reply.show()
    reply.exec_()
    if reply.clickedButton() == yes:
        ls = [SI.ui.lineEdit_24.text(), SI.ui.lineEdit_19.text(), SI.ui.lineEdit_20.text(),
              SI.ui.lineEdit_22.text(), SI.ui.lineEdit_23.text(), SI.ui.lineEdit_18.text(),
              SI.ui.lineEdit_21.text(), SI.ui.textEdit_2.toPlainText()]
        cur, conn = mysql_tools.connect_mysql()
        sql = "insert into supplier_data(supplier_name, supplier_type, supplier_address, supplier_phone, license_key, " \
              "business_license, gmp, notes) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                  ls[0], ls[1], ls[2], ls[3], ls[4], ls[5], ls[6], ls[7])
        rows = cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        ls.clear()
        show_supplier()


# 删除供货单位
def delete_supplier():
    reply = QMessageBox(QMessageBox.Question, '删除', '确定删除？')
    yes = reply.addButton('确定', QMessageBox.YesRole)
    no = reply.addButton('取消', QMessageBox.NoRole)
    reply.show()
    reply.exec_()
    if reply.clickedButton() == yes:
        cur, conn = mysql_tools.connect_mysql()
        sql = "delete from supplier_data where supplier_name = '%s'" % SI.supplier_name_text
        rows = cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        show_supplier()


# 获得企业名称
def get_supplier_name(row, col):
    try:
        content = SI.ui.tableWidget_5.item(row, 0).text()
        SI.supplier_name_text = content
    except Exception as e:
        # 访问异常的错误编号和详细信息
        print(e.args)
        print(str(e))
        print(repr(e))
        msg_box = QMessageBox(QMessageBox.Information, '提示', '选中内容为空！')
        msg_box.exec_()


# 查找供货单位
def seek_supplier():
    text = SI.ui.lineEdit_25.text()
    sql = "select * from supplier_data where supplier_name like '%%%s%%'" % text
    supplier_text = mysql_tools.get_mysql_data(sql)
    if supplier_text:
        pyqt_tools.show_widget(SI.ui.tableWidget_5, supplier_text, 9, label=1)
    else:
        msg_box = QMessageBox(QMessageBox.Information, '提示', '无相关企业！')
        msg_box.exec_()


# 清空供货单位信息
def empty_supplier_text():
    SI.ui.textEdit_2.clear()
    SI.ui.lineEdit_18.clear()
    SI.ui.lineEdit_19.clear()
    SI.ui.lineEdit_20.clear()
    SI.ui.lineEdit_21.clear()
    SI.ui.lineEdit_22.clear()
    SI.ui.lineEdit_23.clear()
    SI.ui.lineEdit_24.clear()
