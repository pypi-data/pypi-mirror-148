# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'table_1.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(970, 759)
        self.formLayout = QFormLayout(Dialog)
        self.formLayout.setObjectName(u"formLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton_1 = QPushButton(Dialog)
        self.pushButton_1.setObjectName(u"pushButton_1")
        font = QFont()
        font.setFamily(u"Adobe Devanagari")
        font.setPointSize(9)
        self.pushButton_1.setFont(font)

        self.verticalLayout.addWidget(self.pushButton_1)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        font1 = QFont()
        font1.setFamily(u"Adobe Devanagari")
        font1.setBold(True)
        font1.setWeight(75)
        self.label_3.setFont(font1)

        self.verticalLayout.addWidget(self.label_3)

        self.comboBox = QComboBox(Dialog)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        font2 = QFont()
        font2.setFamily(u"Times New Roman")
        self.comboBox.setFont(font2)
        self.comboBox.setLayoutDirection(Qt.LeftToRight)
        self.comboBox.setAutoFillBackground(False)

        self.verticalLayout.addWidget(self.comboBox)

        self.label_7 = QLabel(Dialog)
        self.label_7.setObjectName(u"label_7")
        font3 = QFont()
        font3.setFamily(u"Adobe Devanagari")
        font3.setBold(False)
        font3.setWeight(50)
        self.label_7.setFont(font3)

        self.verticalLayout.addWidget(self.label_7)

        self.comboBox_3 = QComboBox(Dialog)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setFont(font2)

        self.verticalLayout.addWidget(self.comboBox_3)

        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font3)

        self.verticalLayout.addWidget(self.label_6)

        self.comboBox_2 = QComboBox(Dialog)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setFont(font2)

        self.verticalLayout.addWidget(self.comboBox_2)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        font4 = QFont()
        font4.setFamily(u"Adobe Devanagari")
        font4.setPointSize(9)
        font4.setBold(False)
        font4.setWeight(50)
        self.label.setFont(font4)

        self.verticalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout.addWidget(self.lineEdit)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font4)

        self.verticalLayout.addWidget(self.label_2)

        self.lineEdit_2 = QLineEdit(Dialog)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.verticalLayout.addWidget(self.lineEdit_2)

        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font3)

        self.verticalLayout.addWidget(self.label_5)

        self.lineEdit_3 = QLineEdit(Dialog)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        font5 = QFont()
        font5.setFamily(u"Adobe Devanagari")
        font5.setItalic(True)
        self.lineEdit_3.setFont(font5)

        self.verticalLayout.addWidget(self.lineEdit_3)


        self.formLayout.setLayout(0, QFormLayout.LabelRole, self.verticalLayout)

        self.tableWidget = QTableWidget(Dialog)
        self.tableWidget.setObjectName(u"tableWidget")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.tableWidget)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_15 = QLabel(Dialog)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font3)

        self.verticalLayout_2.addWidget(self.label_15)

        self.radioButton = QRadioButton(Dialog)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setFont(font2)

        self.verticalLayout_2.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(Dialog)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setFont(font2)

        self.verticalLayout_2.addWidget(self.radioButton_2)

        self.radioButton_3 = QRadioButton(Dialog)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setFont(font2)

        self.verticalLayout_2.addWidget(self.radioButton_3)

        self.pushButton_2 = QPushButton(Dialog)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMinimumSize(QSize(140, 40))
        self.pushButton_2.setFont(font)

        self.verticalLayout_2.addWidget(self.pushButton_2)


        self.formLayout.setLayout(1, QFormLayout.LabelRole, self.verticalLayout_2)

        self.textBrowser = QTextBrowser(Dialog)
        self.textBrowser.setObjectName(u"textBrowser")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textBrowser)

        self.label_8 = QLabel(Dialog)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font1)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.label_8)

        self.pushButton_3 = QPushButton(Dialog)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy1)
        self.pushButton_3.setMinimumSize(QSize(140, 20))
        self.pushButton_3.setFont(font)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.pushButton_3)

        self.tableWidget_2 = QTableWidget(Dialog)
        self.tableWidget_2.setObjectName(u"tableWidget_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tableWidget_2.sizePolicy().hasHeightForWidth())
        self.tableWidget_2.setSizePolicy(sizePolicy2)
        self.tableWidget_2.setMinimumSize(QSize(0, 150))

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.tableWidget_2)

        self.label_11 = QLabel(Dialog)
        self.label_11.setObjectName(u"label_11")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.label_11)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_9 = QLabel(Dialog)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_4.addWidget(self.label_9)

        self.label_10 = QLabel(Dialog)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_4.addWidget(self.label_10)

        self.label_12 = QLabel(Dialog)
        self.label_12.setObjectName(u"label_12")

        self.verticalLayout_4.addWidget(self.label_12)

        self.label_13 = QLabel(Dialog)
        self.label_13.setObjectName(u"label_13")

        self.verticalLayout_4.addWidget(self.label_13)

        self.label_14 = QLabel(Dialog)
        self.label_14.setObjectName(u"label_14")

        self.verticalLayout_4.addWidget(self.label_14)


        self.formLayout.setLayout(5, QFormLayout.FieldRole, self.verticalLayout_4)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font2)

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_4)

        self.label_16 = QLabel(Dialog)
        self.label_16.setObjectName(u"label_16")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.label_16)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Data envelopment analysis 效率计算器  v1.0.1", None))
        self.pushButton_1.setText(QCoreApplication.translate("Dialog", u"\u5bfc\u5165\u8868\u683c", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u8bf7\u9009\u62e9\u6a21\u578b\uff1a", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"CCR\u6a21\u578b", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"SBM\u6a21\u578b", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Dialog", u"DDF\u6a21\u578b", None))

        self.label_7.setText(QCoreApplication.translate("Dialog", u"\u8bf7\u9009\u62e9\u89c4\u6a21\u62a5\u916c\u6027\uff1a", None))
        self.comboBox_3.setItemText(0, QCoreApplication.translate("Dialog", u"\u89c4\u6a21\u62a5\u916c\u4e0d\u53d8CRS", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("Dialog", u"\u89c4\u6a21\u62a5\u916c\u53ef\u53d8VRS", None))

        self.label_6.setText(QCoreApplication.translate("Dialog", u"\u8bf7\u9009\u62e9\u65b9\u5411(DDF\u6a21\u578b)\uff1a", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("Dialog", u"\u65e0\u65b9\u5411(\u9664DDF\u6a21\u578b\u5916)", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("Dialog", u"(-x,y,-b)\u5f31\u53ef\u5904\u7f6e\u6027=", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("Dialog", u"(-x,y,-b)\u5f3a\u53ef\u5904\u7f6e\u6027>=", None))
        self.comboBox_2.setItemText(3, QCoreApplication.translate("Dialog", u"(-x,y,b)\u5f3a\u53ef\u5904\u7f6e\u6027<=", None))

        self.label.setText(QCoreApplication.translate("Dialog", u"\u6295\u5165\u53d8\u91cf\u7684\u4e2a\u6570\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u4ea7\u51fa\u53d8\u91cf\u7684\u4e2a\u6570\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"\u975e\u671f\u671b\u4ea7\u51fa\u53d8\u91cf\u7684\u4e2a\u6570:", None))
        self.lineEdit_3.setText(QCoreApplication.translate("Dialog", u"\u82e5\u65e0\u53ef\u4e0d\u586b\u5199", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"\u6c42\u89e3\u5668\u9009\u53d6\uff1a", None))
        self.radioButton.setText(QCoreApplication.translate("Dialog", u"Gurobi", None))
        self.radioButton_2.setText(QCoreApplication.translate("Dialog", u"Cplex", None))
        self.radioButton_3.setText(QCoreApplication.translate("Dialog", u"Glpk", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"\u5f00\u59cb\u8ba1\u7b97", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"\u7ed3\u679c\u8f93\u51fa\u8868\u683c\u5c55\u793a\uff1a", None))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog", u"\u7ed3\u679c\u4fdd\u5b58", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"* DDF\u6a21\u578b\u9700\u8981\u9009\u62e9\u65b9\u5411\u5411\u91cf\uff0c\u5176\u4ed6\u6a21\u578b\u65e0\u9700\u9009\u62e9\uff0c\u9ed8\u8ba4\u5373\u53ef", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"\u6ce8\uff1a", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"1. \u5bfc\u5165\u6570\u636e\u65f6\uff0c\u8bf7\u6ce8\u610f\u6570\u636e\u683c\u5f0f\u9700\u6309\u7167DMU\u540d\u3001\u6295\u5165\u3001\u4ea7\u51fa\u7684\u987a\u5e8f\u3002", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"2. CCR\u6a21\u578b\u9ed8\u8ba4\u4f1a\u8f93\u51faCRS\u4e0eVRS\u7684\u7ed3\u679c\uff0c\u5e76\u7ed9\u51fa\u89c4\u6a21\u53d8\u5316\u60c5\u51b5\uff1bSBM\u6a21\u578b\u4f1a\u8f93\u51fa\u677e\u5f1b\u53d8\u91cf\u6539\u8fdb\u503c\u3002", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"3. \u9700\u8981\u9009\u62e9\u53d8\u91cf\u4e2a\u6570\uff0c\u53ea\u9700\u586b\u5199\u963f\u62c9\u4f2f\u6570\u5b57\uff0c\u5982\u6295\u51652\u4e2a\uff0c\u53ea\u9700\u8981\u5728\u7a7a\u683c\u5185\u586b\u51992\u3002", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"4. \u82e5\u6709\u975e\u671f\u671b\u4ea7\u51fa\uff0c\u9700\u5220\u9664\u201c\u82e5\u65e0\u53ef\u4e0d\u586b\u5199\u201d\u540e\u518d\u586b\u5199\u6570\u91cf\u3002", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Design by WANGY", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><a href=\"https://deatien.github.io/\"><span style=\" text-decoration: underline; color:#0000ff;\">请点击获取说明文档</span></a></p></body></html>", None))
        self.label_16.setOpenExternalLinks(True)
    # retranslateUi

