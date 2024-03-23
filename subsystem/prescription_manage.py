import re
from PyQt5.QtCore import Qt
from utils import mysql_tools
from utils import pyqt_tools
from utils.public_variable import SI
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QSpinBox, QHeaderView, QAbstractItemView


# 显示药材名
def show_medicine():  # 显示药材名
    sql = 'select med_name from med_data'
    med_data = mysql_tools.get_mysql_data(sql)
    pyqt_tools.show_widget(SI.ui.tableWidget_8, med_data, 1, label=1)


# 获得药材名
def get_medicine_name(row, col):  # 获得药材名
    try:
        content = SI.ui.tableWidget_8.item(row, col).text()  # 点击药材名获得文本
        SI.medicine_name_text = content  # 将药材名放入变量medicine_name_text
        data = []  # 表格中已有的药材
        count = []  # 记录表格前面空格情况

        for row_1 in range(0, SI.ui.tableWidget.rowCount()):
            item_1 = SI.ui.tableWidget.item(row_1, 0)
            if item_1 is None:
                count.append(row_1)
            else:
                item_2 = SI.ui.tableWidget.item(row_1, 0)
                if item_2 is not None:
                    if len(item_2.text()) != 0:
                        data.append(item_2.text())
                    else:
                        count.append(row_1)

        if count:
            insert_med_to_tableWight(content, data, count[0], 0)
        else:
            if data:
                SI.med_clicked_num = len(data)
                insert_med_to_tableWight(content, data, SI.med_clicked_num, 0, label=1)
            else:
                insert_med_to_tableWight(content, data, 0, 0, label=1)

    except Exception as e:
        # 访问异常的错误编号和详细信息
        print(e.args)
        print(str(e))
        print(repr(e))


# 点击药材添加到表格
def insert_med_to_tableWight(med_name, data, row, col=0, label=0):
    if med_name not in data:
        if label == 1:
            if row == 0:
                SI.ui.tableWidget.insertRow(row)
                pyqt_tools.add_btn(row, 2, SI.ui.tableWidget)
            if row == SI.med_clicked_num and SI.med_clicked_num != 0:
                SI.ui.tableWidget.insertRow(row)
                pyqt_tools.add_btn(row, 2, SI.ui.tableWidget)
                SI.med_clicked_num += 1

        item = QTableWidgetItem(med_name)
        SI.ui.tableWidget.setItem(row, col, item)
        item.setTextAlignment(Qt.AlignCenter)
        spin_box = QSpinBox()
        spin_box.setValue(1)
        SI.ui.tableWidget.setCellWidget(row, 1, spin_box)

    else:
        info = '已有药材：%s！' % med_name
        msg_box = QMessageBox(QMessageBox.Information, '提示', info)
        msg_box.exec_()


# 查找药材
def select_medicine():  # 查找药材
    text = SI.ui.lineEdit_29.text()
    sql = "select med_name from med_data where med_name like '%%%s%%'" % text
    med_name = mysql_tools.get_mysql_data(sql)
    pyqt_tools.show_widget(SI.ui.tableWidget_8, med_name, 1)


# 显示处方名
def show_prescription():
    sql = 'select prescription_name from prescription_data'
    pre_name = mysql_tools.get_mysql_data(sql)

    SI.ui.tableWidget_6.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    SI.ui.tableWidget_7.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    SI.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    SI.ui.tableWidget_6.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 处方表格禁止编辑
    SI.ui.tableWidget_8.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 处方药材选择表格禁止编辑
    SI.ui.tableWidget_7.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 处方详情表格禁止编辑

    pyqt_tools.show_widget(SI.ui.tableWidget_6, pre_name, 1)
    show_prescription_info(pre_name[0][0])


# 点击添加一行tableWight行列
def add_row():
    row = SI.ui.tableWidget.rowCount()
    SI.ui.tableWidget.insertRow(row)
    pyqt_tools.add_btn(row, 2, SI.ui.tableWidget)


# 获得处方名
def get_prescription_name(row, col):  # 获得处方名
    try:
        content = SI.ui.tableWidget_6.item(row, col).text()  # 点击处方名获得文本
        SI.pre_name_text = content  # 将处方名放入变量pre_name_text
        show_prescription_info(content)
    except Exception as e:
        # 访问异常的错误编号和详细信息
        print(e.args)
        print(str(e))
        print(repr(e))
        msg_box = QMessageBox(QMessageBox.Information, '提示', '未选中内容！')
        msg_box.exec_()


# 显示处方详情
def show_prescription_info(pre_name):
    SI.ui.lineEdit_27.setText(pre_name)
    cur, conn = mysql_tools.connect_mysql()
    sql = "select prescription_info, indication, notes from prescription_data where prescription_name = '%s'" % pre_name
    pre_data = mysql_tools.get_mysql_data(sql)
    pre_need = pre_data[0][0]

    SI.ui.textEdit_5.setText(pre_data[0][1])
    SI.ui.textEdit.setText(pre_data[0][2])
    str1 = re.sub("[\[\],]", "", pre_need)
    str2 = str1.replace("'", "")  # 去除单引号
    text = re.split(r'[\s:]+', str2.strip())
    SI.ui.tableWidget_7.setRowCount(0)
    SI.ui.tableWidget_7.setColumnCount(2)
    i = 0

    while i < len(text):
        row = SI.ui.tableWidget_7.rowCount()
        SI.ui.tableWidget_7.insertRow(row)
        item = QTableWidgetItem(str(text[i]))
        item1 = QTableWidgetItem(str(text[i + 1]))
        item.setTextAlignment(Qt.AlignCenter)
        item1.setTextAlignment(Qt.AlignCenter)
        SI.ui.tableWidget_7.setItem(row, 0, item)
        SI.ui.tableWidget_7.setItem(row, 1, item1)
        i += 2
    conn.commit()
    cur.close()
    conn.close()


# 删除处方
def delete_pre():  # 删除处方
    if SI.pre_name_text:
        reply = QMessageBox(QMessageBox.Question, '删除', '确定删除？')
        yes = reply.addButton('确定', QMessageBox.YesRole)
        no = reply.addButton('取消', QMessageBox.NoRole)
        reply.show()
        reply.exec_()

        if reply.clickedButton() == yes:
            try:
                cur, conn = mysql_tools.connect_mysql()
                sql = "delete from prescription_data where prescription_name = %s "  # 删除处方的sql语句
                rows = cur.execute(sql, SI.pre_name_text)
                conn.commit()
                cur.close()
                conn.close()
                show_prescription()
            except Exception as e:
                # 访问异常的错误编号和详细信息
                print(e.args)
                print(str(e))
                print(repr(e))
    else:
        reply = QMessageBox(QMessageBox.Information, '提示', '请选择处方！')
        reply.show()
        reply.exec_()


# 查找处方
def select_pre():  # 查找处方
    text = SI.ui.lineEdit_26.text()
    sql = "select prescription_name from prescription_data where prescription_name like '%%%s%%'" % text
    pre_data = mysql_tools.get_mysql_data(sql)
    show_prescription_info(pre_data[0][0])
    pyqt_tools.show_widget(SI.ui.tableWidget_6, pre_data, 1)  # 将处方名显示到表格1


# 获取处方表格数据
def get_wight_data():
    pre_info = []
    for row in range(SI.ui.tableWidget.rowCount()):
        row_data = []
        for col in range(2):
            cell_widget = SI.ui.tableWidget.cellWidget(row, col)
            if isinstance(cell_widget, QSpinBox):
                row_data.append(cell_widget.value())
            else:
                if SI.ui.tableWidget.item(row, col):
                    row_data.append(SI.ui.tableWidget.item(row, col).text())
                else:
                    break
        pre_info.append(row_data)
    pre_info = [x for x in pre_info if x != [] and x[0] != '']
    return pre_info


# 生成处方
def creat_prescription():  # 生成处方
    try:
        pre_info = get_wight_data()
        pre_name = SI.ui.lineEdit_28.text()
        indication_txt = SI.ui.lineEdit.text()
        notes_txt = SI.ui.lineEdit_2.text()
        pre_price = 0
        for info in pre_info:
            sql = "select med_price from med_data where med_name = '%s'" % info[0]
            med_price = mysql_tools.get_mysql_data(sql)
            pre_price += int(info[1]) * int(med_price[0][0])
        if pre_info:
            if not pre_name:
                reply = QMessageBox(QMessageBox.Information, '提示', '请输入处方名！')
                reply.show()
                reply.exec_()
            elif not indication_txt:
                reply = QMessageBox(QMessageBox.Information, '提示', '请输入适应症！')
                reply.show()
                reply.exec_()
            elif not notes_txt:
                reply = QMessageBox(QMessageBox.Information, '提示', '请输入注意事项及禁忌！')
                reply.show()
                reply.exec_()
            else:
                label = pre_taboo(pre_info)
                if label == 0:
                    cur, conn = mysql_tools.connect_mysql()
                    pre_info = str(pre_info)
                    pre_info = pre_info.replace("'", "")  # 去除单引号
                    sql = "insert into prescription_data(prescription_name, prescription_info, indication, notes, " \
                          "prescription_price) values('%s', '%s', '%s', '%s', '%s')" % (pre_name, pre_info,
                                                                                        indication_txt, notes_txt,
                                                                                        pre_price)
                    rows = cur.execute(sql)
                    conn.commit()
                    cur.close()
                    conn.close()
                    SI.med_clicked_num = 0  # 药材添加的数字在处方生成后归零
                    msg_box = QMessageBox(QMessageBox.Information, '提示', '处方生成成功！')
                    msg_box.exec_()
    except Exception as e:
        # 访问异常的错误编号和详细信息
        print(e.args)
        print(str(e))
        print(repr(e))
        title = '警告'
        obj = '请输入处方信息'
        pyqt_tools.warning_box(title, obj)


# 清空文本
def clear_textEdit():  # 清空文本
    SI.ui.tableWidget.setRowCount(0)
    SI.ui.lineEdit_28.clear()
    SI.ui.lineEdit.clear()
    SI.ui.lineEdit_2.clear()
    SI.med_clicked_num = 0


# 处方详情点击
def pre_text():
    pre_name = SI.ui.lineEdit_28.text()
    SI.ui.lineEdit_27.setText(pre_name)
    pre_indication = SI.ui.lineEdit.text()
    SI.ui.textEdit_5.setText(pre_indication)
    pre_notes = SI.ui.lineEdit_2.text()
    SI.ui.textEdit.setText(pre_notes)
    pre_info = get_wight_data()
    pyqt_tools.show_widget(SI.ui.tableWidget_7, pre_info, 2)
    SI.ui.stackedWidget.setCurrentIndex(2)
    show_prescription()


# 处方禁忌
def pre_taboo(pre_info):
    if not pre_info:
        pre_info = get_wight_data()
    label = 0
    if not eighteen_against(pre_info):  # 十八反
        label += 1
    if not nineteen_fear(pre_info):  # 十九畏
        label += 1
    if label == 0:
        msg_box = QMessageBox(QMessageBox.Information, '提示', '该处方没有违反中药方的禁忌')
        msg_box.exec_()
    return label


# 十八反
def eighteen_against(pre_info):  # 十八反\
    pre_data = []
    for info in pre_info:
        pre_data.append(info[0])
    if '乌头' in pre_data:
        name = ['半夏', '瓜蒌', '贝母', '白蔹', '白芨']
        for i in name:
            if i in pre_data:
                title = '警告'
                warn = '该处方违反了十八反：乌头（贝母、瓜蒌、半夏、白蔹、白芨）'
                warn_text(title, warn)
                return False
    elif '甘草' in pre_data:
        name = ['海藻', '京大戟', '甘遂', '芫花']
        for i in name:
            if i in pre_data:
                title = '警告'
                warn = '该处方违反了十八反：甘草(甘遂、京大戟、海藻、芫花)'
                warn_text(title, warn)
                return False
    elif '藜芦' in pre_data:
        name = ['人参', '沙参', '丹参', '玄参', '细辛', '芍药']
        for i in name:
            if i in pre_data:
                title = '警告'
                warn = '该处方违反了十八反：藜芦（人参、沙参、丹参、玄参、细辛、芍药）'
                warn_text(title, warn)
                return False
    else:
        return True


# 十九畏
def nineteen_fear(pre_info):  # 十九畏
    pre_data = []
    for info in pre_info:
        pre_data.append(info[0])
    ls = [['硫磺', '朴硝'], ['水银', '砒霜'], ['狼毒', '密陀僧'], ['巴豆', '牵牛'], ['郁金', '丁香'], ['川乌', '犀角'], ['草乌', '犀角'],
          ['牙硝', '三棱'], ['官桂', '石脂'], ['人参', '五灵脂']]
    num = 0
    for i in ls:
        count = 0
        for j in pre_data:
            if j in i:
                count += 1
        if count >= 2:
            title = '警告'
            warn = '该处方违反了十九畏：%s-%s' % (i[0], i[1])
            warn_text(title, warn)
            num += 1
    if num == 0:
        return True
    else:
        return False


# 警告提示框
def warn_text(obj, obj1):
    msg_box = QMessageBox(QMessageBox.Warning, obj, obj1)
    msg_box.exec_()
