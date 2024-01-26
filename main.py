from PyQt5.QtWidgets import *
from child_table import *
from parent_table import *
from find_table import *
import sys
import psycopg2


class FindWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.cursor = connection.cursor()
        self.ui = Ui_FindWindow()
        self.ui.setupUi(self)
        self.find_data()


    def find_data(self):
        surname_sql = my_interface.ui.comboBox.currentText()
        first_name_sql = my_interface.ui.comboBox_2.currentText()
        patronymic_sql = my_interface.ui.comboBox_3.currentText()
        street_sql = my_interface.ui.comboBox_4.currentText()
        house_number_sql = my_interface.ui.lineEdit.text()
        house_corps_sql = my_interface.ui.lineEdit_2.text()
        flat_sql = my_interface.ui.lineEdit_3.text()
        phone_number_sql = my_interface.ui.lineEdit_4.text()
        if surname_sql != "":
            self.cursor.execute('''SELECT surname_text FROM surname WHERE surname_text = '%s';''' % surname_sql)
            surname_sql = str((self.cursor.fetchone())[0])
        if first_name_sql != "":
            self.cursor.execute(
                '''SELECT first_name_text FROM first_name WHERE first_name_text = '%s';''' % first_name_sql)
            first_name_sql = str((self.cursor.fetchone())[0])
        if patronymic_sql != "":
            self.cursor.execute(
                '''SELECT patronymic_text FROM patronymic WHERE patronymic_text ='%s';''' % patronymic_sql)
            patronymic_sql = str((self.cursor.fetchone())[0])
        if street_sql != "":
            self.cursor.execute('''SELECT street_text FROM street WHERE street_text ='%s';''' % street_sql)
            street_sql = str((self.cursor.fetchone())[0])

        flag = False
        if surname_sql != '':
            surname_sql = "WHERE surname_text = '" + surname_sql + "'"
            flag = True
        if first_name_sql != '':
            if flag:
                first_name_sql = "AND first_name_text = '" +first_name_sql+"'"
            else:
                first_name_sql = "WHERE first_name_text = '" + first_name_sql + "'"
                flag = True
        if patronymic_sql != '':
            if flag:
                patronymic_sql = "AND patronymic_text = '" + patronymic_sql+"'"
            else:
                patronymic_sql = "WHERE patronymic_text = '" + patronymic_sql + "'"
                flag = True
        if street_sql != '':
            if flag:
                street_sql = "AND street_text= '" + street_sql+"'"
            else:
                street_sql = "WHERE street_text= '" + street_sql+"'"
                flag = True
        if house_number_sql != '':
            if flag:
                house_number_sql = "AND house_number = " + house_number_sql
            else:
                house_number_sql = "WHERE house_number = " + house_number_sql
                flag = True
        if house_corps_sql != '':
            if flag:
                house_corps_sql = "AND house_corps = '" + house_corps_sql + "'"
            else:
                house_corps_sql = "WHERE house_corps = '" + house_corps_sql + "'"
                flag = True
        if flat_sql != '':
            if flag:
                flat_sql = "AND flat = " + flat_sql
            else:
                flat_sql = "WHERE flat = " + flat_sql
                flag = True
        if phone_number_sql != '':
            if flag:
                phone_number_sql = "AND phone_number ='"+phone_number_sql + "'"
            else:
                phone_number_sql = "WHERE phone_number ='"+phone_number_sql + "'"
                flag = True


        self.cursor.execute("""SELECT main_book_id,surname_text,first_name_text,patronymic_text,street_text,house_number,house_corps,flat,phone_number
                                FROM
                                    main_book 
                                    LEFT JOIN first_name ON main_book.first_name_id = first_name.first_name_id
                                    LEFT JOIN surname ON main_book.surname_id = surname.surname_id
                                    LEFT JOIN patronymic ON main_book.patronymic_id = patronymic.patronymic_id
                                    LEFT JOIN street ON main_book.street_id = street.street_id
                                %s %s %s %s %s %s %s %s
                                ORDER BY main_book_id asc;""" % (surname_sql,
                                                                  first_name_sql,
                                                                  patronymic_sql,
                                                                  street_sql,
                                                                  house_number_sql,
                                                                  house_corps_sql,
                                                                  flat_sql,
                                                                  phone_number_sql))
        self.table = self.cursor.fetchall()
        if self.table != []:
            self.ui.tableWidget.setColumnCount(len(self.table[0]))
            self.ui.tableWidget.setRowCount(len(self.table))
            row = 0
            for tup in self.table:
                col = 0
                for item in tup:
                    if item is None:
                        cellinfo = QTableWidgetItem(item)
                    else:
                        cellinfo = QTableWidgetItem(str(item))
                    self.ui.tableWidget.setItem(row, col, cellinfo)
                    cellinfo.setFlags(
                        QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # делаем ячейки нередактируемыми
                    col += 1
                row += 1
            self.ui.tableWidget.setHorizontalHeaderLabels(
                ('id', 'Фамилия', 'Имя', 'Отчество', 'Улица', 'Дом', 'Корпус', 'Квартира', 'Номер телефона'))
            self.ui.tableWidget.setVerticalHeaderLabels('' for i in range(len(self.table)))
        else:
            self.ui.tableWidget.setColumnCount(1)
            self.ui.tableWidget.setRowCount(1)
            self.ui.tableWidget.setItem(0, 0, QTableWidgetItem("Не найдено"))
            self.ui.tableWidget.setHorizontalHeaderLabels([''])
            self.ui.tableWidget.setVerticalHeaderLabels([''])

class NewWindow(QtWidgets.QMainWindow):
    def __init__(self, number_window, col_name, table_name):
        super().__init__()
        self.cursor = connection.cursor()
        self.number_window = number_window
        self.col_name = col_name
        self.table_name = table_name
        self.ui = Ui_AnotherWindow()
        self.ui.setupUi(self)
        self.ui.tableWidget.setColumnCount(len(my_interface.record_arr[self.number_window][0]))

        self.update_data()
        self.ui.pushButton_.clicked.connect(self.find_data)
        self.ui.pushButton_1.clicked.connect(self.delete_row)
        self.ui.pushButton_2.clicked.connect(self.add)



    def update_data(self):
        self.cursor.execute('''SELECT main_book_id,surname_text,first_name_text,patronymic_text,
                                        street_text,house_number,house_corps,flat,phone_number
                                    FROM
                	                    first_name RIGHT JOIN 
                	                    main_book ON main_book.first_name_id = first_name.first_name_id
                	                    LEFT JOIN surname ON main_book.surname_id = surname.surname_id
                	                    LEFT JOIN patronymic ON main_book.patronymic_id = patronymic.patronymic_id
                	                    LEFT JOIN street ON main_book.street_id = street.street_id
                	                ORDER BY main_book_id asc; ''')

        self.record = self.cursor.fetchall()
        self.record_arr = []
        self.cursor.execute('''SELECT surname_id,surname_text FROM surname''')
        surname_arr = self.cursor.fetchall()
        self.record_arr.append(surname_arr)
        self.cursor.execute('''SELECT first_name_id,first_name_text FROM first_name''')
        first_name_arr = self.cursor.fetchall()
        self.record_arr.append(first_name_arr)
        self.cursor.execute('''SELECT patronymic_id,patronymic_text FROM patronymic''')
        patronymic_arr = self.cursor.fetchall()
        self.record_arr.append(patronymic_arr)
        self.cursor.execute('''SELECT street_id,street_text FROM street''')
        street_arr = self.cursor.fetchall()
        self.record_arr.append(street_arr)
        self.ui.tableWidget.setRowCount(len(self.record_arr[self.number_window]))
        self.ui.tableWidget.setHorizontalHeaderLabels(('id', self.col_name))
        self.ui.tableWidget.setVerticalHeaderLabels(('' for i in range(len(self.record_arr[self.number_window]))))
        row = 0
        for tup in self.record_arr[self.number_window]:
            col = 0
            for item in tup:
                if item is None:
                    cellinfo = QTableWidgetItem(item)
                else:
                    cellinfo = QTableWidgetItem(str(item))
                self.ui.tableWidget.setItem(row, col, cellinfo)
                cellinfo.setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # делаем ячейки нередактируемыми
                col += 1
            row += 1
        self.ui.comboBox.clear()
        if self.table_name == "surname":
            for i in range(len(surname_arr)):
                self.ui.comboBox.addItem(str(surname_arr[i][0]))
        elif self.table_name == "first_name":
            for i in range(len(first_name_arr)):
                self.ui.comboBox.addItem(str(first_name_arr[i][0]))
        elif self.table_name == "patronymic":
            for i in range(len(patronymic_arr)):
                self.ui.comboBox.addItem(str(patronymic_arr[i][0]))
        elif self.table_name == "street":
            for i in range(len(street_arr)):
                self.ui.comboBox.addItem(str(street_arr[i][0]))

    def add(self):
        print(self.record_arr[self.number_window])
        col_text_sql = self.ui.lineEdit.text()
        #my_interface.cursor.execute()
        self.cursor.execute('''INSERT INTO %s(%s_text)  VALUES ('%s');''' %(self.table_name,self.table_name, col_text_sql))
        my_interface.clear_field()
        self.update_data()


    def delete_row(self):
        try:
            self.cursor.execute('''DELETE FROM %s
                                    WHERE %s_id = %s;''' % (self.table_name,self.table_name,self.ui.comboBox.currentText()))
        except(Exception):
            print(Exception)
        finally:
            my_interface.clear_field()
            self.update_data()

    def find_data(self):
        col_text_sql = self.ui.lineEdit.text()
        self.cursor.execute('''SELECT %s_id,%s_text FROM %s WHERE %s_text = '%s';''' % (self.table_name,
                                                                                      self.table_name,
                                                                                      self.table_name,
                                                                                      self.table_name,
                                                                                      col_text_sql))
        self.find_table = self.cursor.fetchall()

        if self.find_table!=[]:
            self.ui.tableWidget_2.setColumnCount(2)
            self.ui.tableWidget_2.setRowCount(len(self.find_table))
            row = 0
            for tup in self.find_table:
                col = 0
                for item in tup:
                    if item is None:
                        cellinfo = QTableWidgetItem(item)
                    else:
                        cellinfo = QTableWidgetItem(str(item))
                    self.ui.tableWidget_2.setItem(row, col, cellinfo)
                    cellinfo.setFlags(
                        QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # делаем ячейки нередактируемыми
                    col += 1
                row += 1
        else:
            self.ui.tableWidget_2.setColumnCount(2)
            self.ui.tableWidget_2.setRowCount(1)
            self.ui.tableWidget_2.setItem(0, 0, QTableWidgetItem("Не найдено"))
            self.ui.tableWidget_2.setItem(0, 1, QTableWidgetItem("Не найдено"))
        self.ui.tableWidget_2.setHorizontalHeaderLabels(
            ('id', self.col_name))
        self.ui.tableWidget_2.setVerticalHeaderLabels('' for i in range(len(self.find_table)))

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cursor = connection.cursor()
        self.clear_field()
        self.update_data()



        self.ui.tableWidget.setHorizontalHeaderLabels(
            ('id', 'Фамилия', 'Имя', 'Отчество', 'Улица', 'Дом', 'Корпус', 'Квартира', 'Номер телефона')
        )

        self.ui.pushButton_2.clicked.connect(self.add)
        self.ui.pushButton_3.clicked.connect(self.show_find_window)
        self.ui.pushButton_4.clicked.connect(self.update_row)
        self.ui.pushButton_5.clicked.connect(self.delete_row)
        self.ui.pushButton_6.clicked.connect(self.show_surname_window)
        self.ui.pushButton_7.clicked.connect(self.show_first_name_window)
        self.ui.pushButton_8.clicked.connect(self.show_patronymic_window)
        self.ui.pushButton_9.clicked.connect(self.show_street_window)

    def clear_field(self):
        self.ui.comboBox.clear()
        self.ui.comboBox_2.clear()
        self.ui.comboBox_3.clear()
        self.ui.comboBox_4.clear()
        self.ui.comboBox_5.clear()
        self.ui.comboBox_6.clear()
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.comboBox.addItem("")
        self.ui.comboBox_2.addItem("")
        self.ui.comboBox_3.addItem("")
        self.ui.comboBox_4.addItem("")
        self.cursor.execute('''SELECT main_book_id,surname_text,first_name_text,patronymic_text,
                                                street_text,house_number,house_corps,flat,phone_number
                                    FROM
                	                    first_name RIGHT JOIN 
                	                    main_book ON main_book.first_name_id = first_name.first_name_id
                	                    LEFT JOIN surname ON main_book.surname_id = surname.surname_id
                	                    LEFT JOIN patronymic ON main_book.patronymic_id = patronymic.patronymic_id
                	                    LEFT JOIN street ON main_book.street_id = street.street_id
                	                ORDER BY main_book_id asc; ''')

        self.record = self.cursor.fetchall()
        self.record_arr = []
        self.cursor.execute('''SELECT surname_id,surname_text FROM surname''')
        surname_arr = self.cursor.fetchall()
        self.record_arr.append(surname_arr)
        self.cursor.execute('''SELECT first_name_id,first_name_text FROM first_name''')
        first_name_arr = self.cursor.fetchall()
        self.record_arr.append(first_name_arr)
        self.cursor.execute('''SELECT patronymic_id,patronymic_text FROM patronymic''')
        patronymic_arr = self.cursor.fetchall()
        self.record_arr.append(patronymic_arr)
        self.cursor.execute('''SELECT street_id,street_text FROM street''')
        street_arr = self.cursor.fetchall()
        self.record_arr.append(street_arr)
        for i in range(len(surname_arr)):
            self.ui.comboBox.addItem(str(surname_arr[i][1]))
        for i in range(len(first_name_arr)):
            self.ui.comboBox_2.addItem(str(first_name_arr[i][1]))
        for i in range(len(patronymic_arr)):
            self.ui.comboBox_3.addItem(str(patronymic_arr[i][1]))
        for i in range(len(street_arr)):
            self.ui.comboBox_4.addItem(str(street_arr[i][1]))
        for tup in self.record:
            self.ui.comboBox_5.addItem(str(tup[0]))
            self.ui.comboBox_6.addItem(str(tup[0]))


    def update_data(self):
        self.cursor.execute('''SELECT main_book_id,surname_text,first_name_text,patronymic_text,
                                        street_text,house_number,house_corps,flat,phone_number
                            FROM
        	                    first_name RIGHT JOIN 
        	                    main_book ON main_book.first_name_id = first_name.first_name_id
        	                    LEFT JOIN surname ON main_book.surname_id = surname.surname_id
        	                    LEFT JOIN patronymic ON main_book.patronymic_id = patronymic.patronymic_id
        	                    LEFT JOIN street ON main_book.street_id = street.street_id
        	                ORDER BY main_book_id asc; ''')

        self.record = self.cursor.fetchall()
        if self.record!=[]:
            self.ui.tableWidget.setColumnCount(len(self.record[0]))
            self.ui.tableWidget.setRowCount(len(self.record))

        self.ui.tableWidget.setHorizontalHeaderLabels(
            ('id', 'Фамилия', 'Имя', 'Отчество', 'Улица', 'Дом', 'Корпус', 'Квартира', 'Номер телефона')
        )
        self.ui.tableWidget.setVerticalHeaderLabels('' for i in range(len(self.record)))

        """
        self.record_arr = []
        self.cursor.execute('''SELECT surname_id,surname_text FROM surname''')
        surname_arr = self.cursor.fetchall()
        self.record_arr.append(surname_arr)
        self.cursor.execute('''SELECT first_name_id,first_name_text FROM first_name''')
        first_name_arr = self.cursor.fetchall()
        self.record_arr.append(first_name_arr)
        self.cursor.execute('''SELECT patronymic_id,patronymic_text FROM patronymic''')
        patronymic_arr = self.cursor.fetchall()
        self.record_arr.append(patronymic_arr)
        self.cursor.execute('''SELECT street_id,street_text FROM street''')
        street_arr = self.cursor.fetchall()
        self.record_arr.append(street_arr)

        self.ui.comboBox.clear()
        self.ui.comboBox_2.clear()
        self.ui.comboBox_3.clear()
        self.ui.comboBox_4.clear()
        self.ui.comboBox_5.clear()
        self.ui.comboBox_6.clear()

        self.ui.comboBox.addItem("")
        self.ui.comboBox_2.addItem("")
        self.ui.comboBox_3.addItem("")
        self.ui.comboBox_4.addItem("")

        for i in range(len(surname_arr)):
            self.ui.comboBox.addItem(str(surname_arr[i][1]))
        for i in range(len(first_name_arr)):
            self.ui.comboBox_2.addItem(str(first_name_arr[i][1]))
        for i in range(len(patronymic_arr)):
            self.ui.comboBox_3.addItem(str(patronymic_arr[i][1]))
        for i in range(len(street_arr)):
            self.ui.comboBox_4.addItem(str(street_arr[i][1]))

        for tup in self.record:
            self.ui.comboBox_5.addItem(str(tup[0]))
            self.ui.comboBox_6.addItem(str(tup[0]))
        """
        row = 0
        for tup in self.record:
            col = 0
            for item in tup:
                if item is None:
                    cellinfo = QTableWidgetItem(item)
                else:
                    cellinfo = QTableWidgetItem(str(item))
                self.ui.tableWidget.setItem(row, col, cellinfo)
                cellinfo.setFlags(
                    QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # делаем ячейки нередактируемыми
                col += 1
            row += 1
        if self.record == []:
            for col in range(9):
                self.ui.tableWidget.setItem(0, col, QTableWidgetItem(""))




    def show_surname_window(self):
        self.surname_w = NewWindow(0,"Фамилия","surname")
        self.surname_w.show()
    def show_first_name_window(self):
        self.first_name_w = NewWindow(1,"Имя","first_name")
        self.first_name_w.show()
    def show_patronymic_window(self):
        self.patronymic_w = NewWindow(2,"Отчество","patronymic")
        self.patronymic_w.show()
    def show_street_window(self):
        self.street_w = NewWindow(3,"Улица","street")
        self.street_w.show()

    def show_find_window(self):
        self.find_w = FindWindow()
        self.find_w.show()

    def add(self):
        surname_sql = self.ui.comboBox.currentText()
        first_name_sql = self.ui.comboBox_2.currentText()
        patronymic_sql = self.ui.comboBox_3.currentText()
        street_sql = self.ui.comboBox_4.currentText()
        house_number_sql = self.ui.lineEdit.text()
        house_corps_sql = self.ui.lineEdit_2.text()
        flat_sql = self.ui.lineEdit_3.text()
        phone_number_sql = self.ui.lineEdit_4.text()
        if surname_sql != "":
            self.cursor.execute('''SELECT surname_id FROM surname WHERE surname_text = '%s';''' % surname_sql)
            surname_sql = str((self.cursor.fetchone())[0])
        if first_name_sql != "":
            self.cursor.execute('''SELECT first_name_id FROM first_name WHERE first_name_text = '%s';''' % first_name_sql)
            first_name_sql = str((self.cursor.fetchone())[0])
        if patronymic_sql != "":
            self.cursor.execute('''SELECT patronymic_id FROM patronymic WHERE patronymic_text ='%s';''' % patronymic_sql)
            patronymic_sql = str((self.cursor.fetchone())[0])
        if street_sql != "":
            self.cursor.execute('''SELECT street_id FROM street WHERE street_text ='%s';''' % street_sql)
            street_sql = str((self.cursor.fetchone())[0])

        if surname_sql =='':
            surname_sql = "NULL"
        if first_name_sql != '':
            first_name_sql =", "+first_name_sql
        else:
            first_name_sql = ",NULL"
        if patronymic_sql != '' :
            patronymic_sql =", "+patronymic_sql
        else:
            patronymic_sql = ", NULL"
        if street_sql != '':
            street_sql = ", "+street_sql
        else:
            street_sql = ", NULL"
        if house_number_sql != '':
            house_number_sql = ", "+house_number_sql
        else:
            house_number_sql = ", NULL"
        if house_corps_sql != '':
            house_corps_sql = ", "+"'"+house_corps_sql+"'"
        else:
            house_corps_sql = ", NULL"
        if flat_sql != '':
            flat_sql = ", "+flat_sql
        else:
            flat_sql = ", NULL"
        if phone_number_sql!='':
            phone_number_sql =", '"+phone_number_sql + "'"
        else:
            phone_number_sql = ", NULL"

        self.cursor.execute("""INSERT INTO main_book VALUES (DEFAULT,%s%s%s%s%s%s%s%s);""" % (surname_sql,
                                                                               first_name_sql,
                                                                               patronymic_sql,
                                                                               street_sql,
                                                                               house_number_sql,
                                                                               house_corps_sql,
                                                                               flat_sql,
                                                                               phone_number_sql))
        self.update_data()
        self.clear_field()

    def delete_row(self):
        self.cursor.execute('''DELETE FROM main_book
                        WHERE main_book_id = %s;''' %self.ui.comboBox_6.currentText())
        self.update_data()
        self.clear_field()

    def update_row(self):
        surname_sql = self.ui.comboBox.currentText()
        first_name_sql = self.ui.comboBox_2.currentText()
        patronymic_sql = self.ui.comboBox_3.currentText()
        street_sql = self.ui.comboBox_4.currentText()
        house_number_sql = self.ui.lineEdit.text()
        house_corps_sql = self.ui.lineEdit_2.text()
        flat_sql = self.ui.lineEdit_3.text()
        phone_number_sql = self.ui.lineEdit_4.text()
        if surname_sql != "":
            self.cursor.execute('''SELECT surname_id FROM surname WHERE surname_text = '%s';''' % surname_sql)
            surname_sql = str((self.cursor.fetchone())[0])
        if first_name_sql != "":
            self.cursor.execute(
                '''SELECT first_name_id FROM first_name WHERE first_name_text = '%s';''' % first_name_sql)
            first_name_sql = str((self.cursor.fetchone())[0])
        if patronymic_sql != "":
            self.cursor.execute(
                '''SELECT patronymic_id FROM patronymic WHERE patronymic_text ='%s';''' % patronymic_sql)
            patronymic_sql = str((self.cursor.fetchone())[0])
        if street_sql != "":
            self.cursor.execute('''SELECT street_id FROM street WHERE street_text ='%s';''' % street_sql)
            street_sql = str((self.cursor.fetchone())[0])

        if surname_sql == '':
            surname_sql = "NULL"
        if first_name_sql == '':
            first_name_sql = "NULL"
        if patronymic_sql == '':
            patronymic_sql = "NULL"
        if street_sql == '':
            street_sql = "NULL"
        if house_number_sql == '':
            house_number_sql = "NULL"
        if house_corps_sql == '':
            house_corps_sql = "NULL"
        else:
            house_corps_sql = "'"+house_corps_sql+"'"
        if flat_sql == '':
            flat_sql = "NULL"
        if phone_number_sql == '':
            phone_number_sql = "NULL"
        else:
            phone_number_sql = "'" + phone_number_sql + "'"
        self.cursor.execute('''UPDATE main_book
                SET surname_id = %s,
                    first_name_id = %s,
                    patronymic_id = %s,
                    street_id = %s,
                    house_number = %s,
                    house_corps = %s,
                    flat = %s,
                    phone_number = %s
                WHERE main_book_id = %s;
                ''' % (surname_sql,
                   first_name_sql,
                   patronymic_sql,
                   street_sql,
                   house_number_sql,
                   house_corps_sql,
                   flat_sql,
                   phone_number_sql,self.ui.comboBox_5.currentText()))
        self.update_data()

# Подключение к существующей базе данных
connection = psycopg2.connect(user="postgres",
                              password="1111",
                              host="localhost",
                              port="5432",
                              database="phone_book_db")
connection.autocommit = True

app = QtWidgets.QApplication([])
my_interface = MainWindow()
my_interface.show()
sys.exit(app.exec())
