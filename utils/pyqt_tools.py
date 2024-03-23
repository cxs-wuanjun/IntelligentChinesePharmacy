from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from utils import pyqt_tools, mysql_tools


def warning_box(text1, text2):
    msg_box = QMessageBox(QMessageBox.Warning, text1, text2)
    msg_box.exec_()


# 显示到表格
def show_widget(table_widget, text, count, label=0):
    table_widget.setRowCount(0)          # 格式化行
    table_widget.setColumnCount(count)   # 格式化列
    if label == 0:
        for i in range(len(text)):
            item = text[i]
            row = table_widget.rowCount()
            table_widget.insertRow(row)
            for j in range(len(item)):
                item = QTableWidgetItem(str(text[i][j]))
                table_widget.setItem(row, j, item)
                item.setTextAlignment(Qt.AlignCenter)
    else:
        for i in range(len(text)):
            item = text[i]
            row = table_widget.rowCount()
            table_widget.insertRow(row)
            for j in range(len(item) + 1):
                if j == len(text[i]):
                    pyqt_tools.add_btn(i, j, table_widget, label=label)   # 1是供货单位，2是药材
                else:
                    item = QTableWidgetItem(str(text[i][j]))
                    table_widget.setItem(row, j, item)
                    item.setTextAlignment(Qt.AlignCenter)


# 添加按钮
def add_btn(row, col, tableWidget, label=0):
    btn = QPushButton()
    btn.setStyleSheet("QPushButton {\n"
                      "            background-color: transparent;\n"
                      "            border: none;\n"
                      "            color: #555555;\n"
                      "            font-size: 16px;\n"
                      "            padding: 8px 16px;\n"
                      "            border-radius: 20px;\n"
                      "        }\n"
                      "       QPushButton:hover {\n"
                      "            background:rgba(0, 0, 0, 100);\n"
                      "            border: 4px solid #ffffff;\n"
                      "            border-radius: 40px;\n"
                      "        }")
    btn.setText("")
    icon5 = QtGui.QIcon()
    btn.setText("删除")
    icon5.addPixmap(QtGui.QPixmap("./res_img/减.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    btn.setIcon(icon5)
    tableWidget.setCellWidget(row, col, btn)
    btn.clicked.connect(lambda: delete_row(tableWidget, label=label))


# 删除行
def delete_row(tableWidget, label=0):
    if label == 0:
        row = tableWidget.currentRow()  # 获取当前选中的行
        tableWidget.removeRow(row)
    elif label == 1:
        reply = QMessageBox(QMessageBox.Question, '删除', '确定删除？')
        yes = reply.addButton('确定', QMessageBox.YesRole)
        no = reply.addButton('取消', QMessageBox.NoRole)
        reply.show()
        reply.exec_()
        if reply.clickedButton() == yes:
            row = tableWidget.currentRow()  # 获取当前选中的行
            cur, conn = mysql_tools.connect_mysql()
            sql = "delete from supplier_data where supplier_name = '%s'" % tableWidget.item(row, 0).text()
            rows = cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            tableWidget.removeRow(row)
    elif label == 2:
        row = tableWidget.currentRow()  # 获取当前选中的行
        cur, conn = mysql_tools.connect_mysql()
        sql = "delete from med_data where med_name = '%s'" % tableWidget.item(row, 0).text()
        rows = cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        tableWidget.removeRow(row)
    elif label == 3:
        reply = QMessageBox(QMessageBox.Question, '删除', '确定删除？')
        yes = reply.addButton('确定', QMessageBox.YesRole)
        no = reply.addButton('取消', QMessageBox.NoRole)
        reply.show()
        reply.exec_()
        if reply.clickedButton() == yes:
            row = tableWidget.currentRow()  # 获取当前选中的行
            cur, conn = mysql_tools.connect_mysql()
            sql = "delete from user_info where user_id = '%s'" % tableWidget.item(row, 0).text()
            rows = cur.execute(sql)
            sql1 = "delete from user_data where user_id = '%s'" % tableWidget.item(row, 0).text()
            rows = cur.execute(sql1)
            conn.commit()
            cur.close()
            conn.close()
            tableWidget.removeRow(row)



