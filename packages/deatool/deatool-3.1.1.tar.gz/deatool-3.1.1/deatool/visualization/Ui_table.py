# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'table.ui'
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
        Dialog.resize(900, 600)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButton_1 = QPushButton(Dialog)
        self.pushButton_1.setObjectName(u"pushButton_1")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_1.sizePolicy().hasHeightForWidth())
        self.pushButton_1.setSizePolicy(sizePolicy)
        self.pushButton_1.setMinimumSize(QSize(170, 30))

        self.gridLayout_2.addWidget(self.pushButton_1, 0, 0, 1, 1)

        self.tableWidget = QTableWidget(Dialog)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.tableWidget, 0, 1, 1, 1)

        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy2)
        self.tabWidget.setMinimumSize(QSize(20, 20))
        font = QFont()
        font.setFamily(u"Times New Roman")
        self.tabWidget.setFont(font)
        self.tabWidget.setLayoutDirection(Qt.LeftToRight)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(self.tab)
        self.label_3.setObjectName(u"label_3")
        font1 = QFont()
        font1.setFamily(u"Adobe Devanagari")
        font1.setBold(True)
        font1.setWeight(75)
        self.label_3.setFont(font1)

        self.verticalLayout.addWidget(self.label_3)

        self.comboBox = QComboBox(self.tab)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy3)
        self.comboBox.setFont(font)
        self.comboBox.setLayoutDirection(Qt.LeftToRight)
        self.comboBox.setAutoFillBackground(False)

        self.verticalLayout.addWidget(self.comboBox)

        self.label_7 = QLabel(self.tab)
        self.label_7.setObjectName(u"label_7")
        font2 = QFont()
        font2.setFamily(u"Adobe Devanagari")
        font2.setBold(False)
        font2.setWeight(50)
        self.label_7.setFont(font2)

        self.verticalLayout.addWidget(self.label_7)

        self.comboBox_3 = QComboBox(self.tab)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        sizePolicy3.setHeightForWidth(self.comboBox_3.sizePolicy().hasHeightForWidth())
        self.comboBox_3.setSizePolicy(sizePolicy3)
        self.comboBox_3.setFont(font)

        self.verticalLayout.addWidget(self.comboBox_3)

        self.label_6 = QLabel(self.tab)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font2)

        self.verticalLayout.addWidget(self.label_6)

        self.comboBox_2 = QComboBox(self.tab)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        sizePolicy3.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy3)
        self.comboBox_2.setFont(font)

        self.verticalLayout.addWidget(self.comboBox_2)

        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        font3 = QFont()
        font3.setFamily(u"Adobe Devanagari")
        font3.setPointSize(9)
        font3.setBold(False)
        font3.setWeight(50)
        self.label.setFont(font3)

        self.verticalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(self.tab)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout.addWidget(self.lineEdit)

        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font3)

        self.verticalLayout.addWidget(self.label_2)

        self.lineEdit_2 = QLineEdit(self.tab)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.verticalLayout.addWidget(self.lineEdit_2)

        self.label_5 = QLabel(self.tab)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font2)

        self.verticalLayout.addWidget(self.label_5)

        self.lineEdit_3 = QLineEdit(self.tab)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy4)
        font4 = QFont()
        font4.setFamily(u"Adobe Devanagari")
        font4.setItalic(True)
        self.lineEdit_3.setFont(font4)

        self.verticalLayout.addWidget(self.lineEdit_3)

        self.pushButton_2 = QPushButton(self.tab)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setEnabled(True)
        sizePolicy5 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy5)
        self.pushButton_2.setMinimumSize(QSize(170, 30))
        font5 = QFont()
        font5.setFamily(u"Adobe Devanagari")
        font5.setPointSize(9)
        self.pushButton_2.setFont(font5)

        self.verticalLayout.addWidget(self.pushButton_2)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_2 = QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_15 = QLabel(self.tab_2)
        self.label_15.setObjectName(u"label_15")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy6)
        self.label_15.setFont(font1)

        self.verticalLayout_2.addWidget(self.label_15)

        self.comboBox_4 = QComboBox(self.tab_2)
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.setObjectName(u"comboBox_4")
        sizePolicy3.setHeightForWidth(self.comboBox_4.sizePolicy().hasHeightForWidth())
        self.comboBox_4.setSizePolicy(sizePolicy3)
        self.comboBox_4.setFont(font)
        self.comboBox_4.setLayoutDirection(Qt.LeftToRight)
        self.comboBox_4.setAutoFillBackground(False)

        self.verticalLayout_2.addWidget(self.comboBox_4)

        self.label_17 = QLabel(self.tab_2)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font2)

        self.verticalLayout_2.addWidget(self.label_17)

        self.comboBox_5 = QComboBox(self.tab_2)
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.setObjectName(u"comboBox_5")
        sizePolicy3.setHeightForWidth(self.comboBox_5.sizePolicy().hasHeightForWidth())
        self.comboBox_5.setSizePolicy(sizePolicy3)
        self.comboBox_5.setFont(font)

        self.verticalLayout_2.addWidget(self.comboBox_5)

        self.label_18 = QLabel(self.tab_2)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font2)

        self.verticalLayout_2.addWidget(self.label_18)

        self.comboBox_6 = QComboBox(self.tab_2)
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.setObjectName(u"comboBox_6")
        sizePolicy3.setHeightForWidth(self.comboBox_6.sizePolicy().hasHeightForWidth())
        self.comboBox_6.setSizePolicy(sizePolicy3)
        self.comboBox_6.setFont(font)

        self.verticalLayout_2.addWidget(self.comboBox_6)

        self.label_19 = QLabel(self.tab_2)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font3)

        self.verticalLayout_2.addWidget(self.label_19)

        self.lineEdit_4 = QLineEdit(self.tab_2)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.verticalLayout_2.addWidget(self.lineEdit_4)

        self.label_20 = QLabel(self.tab_2)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font3)

        self.verticalLayout_2.addWidget(self.label_20)

        self.lineEdit_5 = QLineEdit(self.tab_2)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.verticalLayout_2.addWidget(self.lineEdit_5)

        self.label_21 = QLabel(self.tab_2)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font2)

        self.verticalLayout_2.addWidget(self.label_21)

        self.lineEdit_6 = QLineEdit(self.tab_2)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        sizePolicy4.setHeightForWidth(self.lineEdit_6.sizePolicy().hasHeightForWidth())
        self.lineEdit_6.setSizePolicy(sizePolicy4)
        self.lineEdit_6.setFont(font4)

        self.verticalLayout_2.addWidget(self.lineEdit_6)

        self.pushButton_4 = QPushButton(self.tab_2)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setEnabled(True)
        sizePolicy5.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy5)
        self.pushButton_4.setMinimumSize(QSize(170, 30))
        self.pushButton_4.setFont(font5)

        self.verticalLayout_2.addWidget(self.pushButton_4)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_4 = QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_27 = QLabel(self.tab_3)
        self.label_27.setObjectName(u"label_27")
        sizePolicy6.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy6)
        self.label_27.setFont(font1)

        self.verticalLayout_4.addWidget(self.label_27)

        self.comboBox_9 = QComboBox(self.tab_3)
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.setObjectName(u"comboBox_9")
        sizePolicy3.setHeightForWidth(self.comboBox_9.sizePolicy().hasHeightForWidth())
        self.comboBox_9.setSizePolicy(sizePolicy3)
        self.comboBox_9.setFont(font)
        self.comboBox_9.setLayoutDirection(Qt.LeftToRight)
        self.comboBox_9.setAutoFillBackground(False)

        self.verticalLayout_4.addWidget(self.comboBox_9)

        self.label_23 = QLabel(self.tab_3)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font2)

        self.verticalLayout_4.addWidget(self.label_23)

        self.comboBox_8 = QComboBox(self.tab_3)
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.setObjectName(u"comboBox_8")
        sizePolicy3.setHeightForWidth(self.comboBox_8.sizePolicy().hasHeightForWidth())
        self.comboBox_8.setSizePolicy(sizePolicy3)
        self.comboBox_8.setFont(font)

        self.verticalLayout_4.addWidget(self.comboBox_8)

        self.label_24 = QLabel(self.tab_3)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font3)

        self.verticalLayout_4.addWidget(self.label_24)

        self.lineEdit_8 = QLineEdit(self.tab_3)
        self.lineEdit_8.setObjectName(u"lineEdit_8")

        self.verticalLayout_4.addWidget(self.lineEdit_8)

        self.label_26 = QLabel(self.tab_3)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font3)

        self.verticalLayout_4.addWidget(self.label_26)

        self.lineEdit_9 = QLineEdit(self.tab_3)
        self.lineEdit_9.setObjectName(u"lineEdit_9")

        self.verticalLayout_4.addWidget(self.lineEdit_9)

        self.label_25 = QLabel(self.tab_3)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font2)

        self.verticalLayout_4.addWidget(self.label_25)

        self.lineEdit_7 = QLineEdit(self.tab_3)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setFont(font4)

        self.verticalLayout_4.addWidget(self.lineEdit_7)

        self.pushButton_5 = QPushButton(self.tab_3)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setEnabled(True)
        sizePolicy5.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy5)
        self.pushButton_5.setMinimumSize(QSize(170, 30))
        self.pushButton_5.setFont(font5)

        self.verticalLayout_4.addWidget(self.pushButton_5)

        self.tabWidget.addTab(self.tab_3, "")

        self.gridLayout_2.addWidget(self.tabWidget, 1, 0, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_22 = QLabel(Dialog)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font1)
        self.label_22.setTextFormat(Qt.RichText)

        self.verticalLayout_3.addWidget(self.label_22)

        self.textBrowser = QTextBrowser(Dialog)
        self.textBrowser.setObjectName(u"textBrowser")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(6)
        sizePolicy7.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy7)

        self.verticalLayout_3.addWidget(self.textBrowser)

        self.label_8 = QLabel(Dialog)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font1)
        self.label_8.setTextFormat(Qt.RichText)

        self.verticalLayout_3.addWidget(self.label_8)

        self.tableWidget_2 = QTableWidget(Dialog)
        self.tableWidget_2.setObjectName(u"tableWidget_2")
        sizePolicy8 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.tableWidget_2.sizePolicy().hasHeightForWidth())
        self.tableWidget_2.setSizePolicy(sizePolicy8)
        self.tableWidget_2.setMinimumSize(QSize(0, 150))

        self.verticalLayout_3.addWidget(self.tableWidget_2)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 2)
        self.verticalLayout_3.setStretch(2, 1)
        self.verticalLayout_3.setStretch(3, 4)

        self.gridLayout_2.addLayout(self.verticalLayout_3, 1, 1, 1, 1)

        self.label_16 = QLabel(Dialog)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_2.addWidget(self.label_16, 2, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(300)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setContentsMargins(0, -1, 0, -1)
        self.pushButton_3 = QPushButton(Dialog)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy2.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy2)
        self.pushButton_3.setMinimumSize(QSize(170, 30))
        self.pushButton_3.setFont(font5)

        self.gridLayout.addWidget(self.pushButton_3, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_9 = QLabel(Dialog)
        self.label_9.setObjectName(u"label_9")
        font6 = QFont()
        font6.setFamily(u"Times New Roman")
        font6.setPointSize(9)
        font6.setBold(False)
        font6.setWeight(50)
        self.label_9.setFont(font6)

        self.horizontalLayout.addWidget(self.label_9)

        self.lineEdit_10 = QLineEdit(Dialog)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        self.lineEdit_10.setFont(font)

        self.horizontalLayout.addWidget(self.lineEdit_10)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 2, 1, 2, 1)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
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
        self.comboBox_2.setItemText(3, QCoreApplication.translate("Dialog", u"(-x,y,-b)\u5f3a\u53ef\u5904\u7f6e\u6027<=", None))

        self.label.setText(QCoreApplication.translate("Dialog", u"\u6295\u5165\u53d8\u91cf\u7684\u4e2a\u6570\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u4ea7\u51fa\u53d8\u91cf\u7684\u4e2a\u6570\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"\u975e\u671f\u671b\u4ea7\u51fa\u53d8\u91cf\u7684\u4e2a\u6570:", None))
        self.lineEdit_3.setText(QCoreApplication.translate("Dialog", u"\u82e5\u65e0\u53ef\u4e0d\u586b\u5199", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"\u5f00\u59cb\u8ba1\u7b97", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Dialog", u"\u5e38\u89c4\u6548\u7387\u6a21\u578b", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"\u8bf7\u9009\u62e9\u6a21\u578b\uff1a", None))
        self.comboBox_4.setItemText(0, QCoreApplication.translate("Dialog", u"CCR\u8d85\u6548\u7387\u6a21\u578b", None))
        self.comboBox_4.setItemText(1, QCoreApplication.translate("Dialog", u"SBM\u8d85\u6548\u7387\u6a21\u578b", None))
        self.comboBox_4.setItemText(2, QCoreApplication.translate("Dialog", u"DDF\u8d85\u6548\u7387\u6a21\u578b", None))

        self.label_17.setText(QCoreApplication.translate("Dialog", u"\u8bf7\u9009\u62e9\u89c4\u6a21\u62a5\u916c\u6027\uff1a", None))
        self.comboBox_5.setItemText(0, QCoreApplication.translate("Dialog", u"\u89c4\u6a21\u62a5\u916c\u4e0d\u53d8CRS", None))
        self.comboBox_5.setItemText(1, QCoreApplication.translate("Dialog", u"\u89c4\u6a21\u62a5\u916c\u53ef\u53d8VRS", None))

        self.label_18.setText(QCoreApplication.translate("Dialog", u"\u8bf7\u9009\u62e9\u65b9\u5411(DDF\u6a21\u578b)\uff1a", None))
        self.comboBox_6.setItemText(0, QCoreApplication.translate("Dialog", u"\u65e0\u65b9\u5411(\u9664DDF\u6a21\u578b\u5916)", None))
        self.comboBox_6.setItemText(1, QCoreApplication.translate("Dialog", u"(-x,y,-b)\u5f31\u53ef\u5904\u7f6e\u6027=", None))
        self.comboBox_6.setItemText(2, QCoreApplication.translate("Dialog", u"(-x,y,-b)\u5f3a\u53ef\u5904\u7f6e\u6027>=", None))
        self.comboBox_6.setItemText(3, QCoreApplication.translate("Dialog", u"(-x,y,-b)\u5f3a\u53ef\u5904\u7f6e\u6027<=", None))

        self.label_19.setText(QCoreApplication.translate("Dialog", u"\u6295\u5165\u53d8\u91cf\u7684\u4e2a\u6570\uff1a", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"\u4ea7\u51fa\u53d8\u91cf\u7684\u4e2a\u6570\uff1a", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"\u975e\u671f\u671b\u4ea7\u51fa\u53d8\u91cf\u7684\u4e2a\u6570:", None))
        self.lineEdit_6.setText(QCoreApplication.translate("Dialog", u"\u82e5\u65e0\u53ef\u4e0d\u586b\u5199", None))
        self.pushButton_4.setText(QCoreApplication.translate("Dialog", u"\u5f00\u59cb\u8ba1\u7b97", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"\u8d85\u6548\u7387\u6a21\u578b", None))
        self.label_27.setText(QCoreApplication.translate("Dialog", u"\u8bf7\u9009\u62e9\u6a21\u578b\uff1a", None))
        self.comboBox_9.setItemText(0, QCoreApplication.translate("Dialog", u"CCR Malmquist \u6307\u6570\u6a21\u578b", None))
        self.comboBox_9.setItemText(1, QCoreApplication.translate("Dialog", u"SBM Malmquist \u6307\u6570\u6a21\u578b", None))

        self.label_23.setText(QCoreApplication.translate("Dialog", u"\u8bf7\u9009\u62e9\u89c4\u6a21\u62a5\u916c\u6027\uff1a", None))
        self.comboBox_8.setItemText(0, QCoreApplication.translate("Dialog", u"\u89c4\u6a21\u62a5\u916c\u4e0d\u53d8CRS", None))
        self.comboBox_8.setItemText(1, QCoreApplication.translate("Dialog", u"\u89c4\u6a21\u62a5\u916c\u53ef\u53d8VRS", None))

        self.label_24.setText(QCoreApplication.translate("Dialog", u"\u6295\u5165\u53d8\u91cf\u7684\u4e2a\u6570\uff1a", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"\u4ea7\u51fa\u53d8\u91cf\u7684\u4e2a\u6570\uff1a", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"\u671f\u6570\uff1a", None))
        self.lineEdit_7.setText("")
        self.pushButton_5.setText(QCoreApplication.translate("Dialog", u"\u5f00\u59cb\u8ba1\u7b97", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Dialog", u"Malmquist\u6307\u6570", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"\u6c42\u89e3\u4fe1\u606f\u5c55\u793a\uff1a", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"\u7ed3\u679c\u8f93\u51fa\u8868\u683c\u5c55\u793a\uff1a", None))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog", u"\u7ed3\u679c\u4fdd\u5b58", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Key:", None))
        self.lineEdit_10.setText("")
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Design by WANGY", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><a href=\"https://deatien.github.io/\"><span style=\" text-decoration: underline; color:#0000ff;\">请点击获取说明文档</span></a></p></body></html>", None))
        self.label_16.setOpenExternalLinks(True)
    # retranslateUi

