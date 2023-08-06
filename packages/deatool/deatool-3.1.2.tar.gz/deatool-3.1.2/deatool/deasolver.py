import os
import sys
# deatool_root = r"C:\Users\wangy\Desktop\Project\deatools-mip\deatool"
# os.chdir(deatool_root)
# cwd = os.getcwd()
# sys.path.insert(0,cwd)
from PySide2 import QtCore
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import *
from deatool.MMODEL.CCR import MCCR
from deatool.MMODEL.DDF import MDDF
from deatool.MMODEL.SBM import MSBM
from deatool.MMODEL.super_CCR import MSCCR
from deatool.MMODEL.super_DDF import MSDDF
from deatool.MMODEL.super_SBM import MSSBM
from deatool.MMODEL.malmquist_ccr import MalmCCR
from deatool.MMODEL.malmquist_sbm import MalmSBM
from deatool.visualization.Ui_table import Ui_Dialog
import pandas as pd
from numpy import nan
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))
path = os.path.dirname(os.path.realpath(__file__))

class Tables(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.currentChanged.connect(self.add)
        self.pushButton_1.clicked.connect(self.dataprocess)
        self.pushButton_2.clicked.connect(self.result)
        self.pushButton_4.clicked.connect(self.result)
        self.pushButton_5.clicked.connect(self.result)
        self.pushButton_3.clicked.connect(self.save)
        self.setWindowTitle('Data envelopment analysis 效率计算器  v1.1.0')
        self.setWindowIcon(QIcon(path+'/deatool.png'))
        self.textBrowser.setStyleSheet("background-color:white;border:none;")
        self.tableWidget.setStyleSheet("background-color:white")
        self.tableWidget_2.setStyleSheet("background-color:white;border:none;")
        self.tabWidget.setStyleSheet('border-radius: 7px')
        _pushButton = ['self.pushButton_{}.setStyleSheet'.format(i) for i in range(1,6)]
        for _ in _pushButton:
            eval(_)('background-color:#fbfbfb;border-radius: 8px; border: 1px groove gray;border-style: outset;')
        # self.setWindowFlags(Qt.FramelessWindowHint)  
        # self.tabWidget.currentChanged.connect(self.tabchange)

            
    def putton(self):
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        pass

    def initialize(self,df):
        # 设置表格行数和列数
        columns = df.columns
        rows = df.index
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.setHorizontalHeaderLabels(columns)
        for j in range(len(columns)):
            self.tableWidget.setColumnWidth(j, 100)
            for i in range(len(rows)):
                data = QTableWidgetItem(str(df.iloc[i][j]))
                self.tableWidget.setItem(i, j, data)
        self.tableWidget.setAlternatingRowColors(True)
    
    def final(self,df):
        columns = df.columns
        rows = df.index
        self.tableWidget_2.setRowCount(len(rows))
        self.tableWidget_2.setColumnCount(len(columns))
        self.tableWidget_2.setHorizontalHeaderLabels(columns)
        for j in range(len(columns)):
            self.tableWidget_2.setColumnWidth(j, 100)
            for i in range(len(rows)):
                data = QTableWidgetItem(str(df.iloc[i][j]))
                self.tableWidget_2.setItem(i, j, data)
        self.tableWidget_2.setAlternatingRowColors(True)
    
    def dataprocess(self):
        try:
            openfile_name = QFileDialog.getOpenFileName(self,'选择文件','','Excel files(*.xlsx , *.xls)')
            global path_openfile_name
            path_openfile_name = openfile_name[0]
            self.df=pd.read_excel(path_openfile_name)
            self.initialize(self.df)
        except:
            self.printf('Error:数据读取有误，请检查数据。')
    def add(self, x):  
        if x != 0:
            if self.lineEdit_10.text() == 'a34d-ke12-tj46':
                if x == 1:
                    self.printf('已解锁超效率模型,您正在使用超效率模型功能')
                elif x == 2:
                    self.pushButton_5.setEnabled(False)
                    self.printf('Malmuqist指数功能受限制，预体验完整功能，请联系作者！')
            elif self.lineEdit_10.text() == 'a34d-ke12-tj92':
                if x == 1:
                    self.printf('已解锁全部模型,您正在使用超效率模型功能')
                elif x == 2:
                    self.printf('已解锁全部模型,您正在使用Malmquist指数计算功能')
                pass
            else:
                self.pushButton_4.setEnabled(False)
                self.pushButton_5.setEnabled(False)
                self.printf('该功能受限制，预体验完整功能，请联系作者！')    
    def result(self):
        data = self.df.copy()
        try:
            self.key = self.comboBox.currentText() 
            self.skey = self.comboBox_4.currentText() 
            self.mkey = self.comboBox_9.currentText() 
            vv = self.comboBox_3.currentText() 
            svv = self.comboBox_5.currentText() 
            dd = self.comboBox_2.currentText()
            sdd = self.comboBox_6.currentText()
            self.printf('正在计算结果，请稍后')
            
            if self.tabWidget.currentIndex() == 0:
                self.input_cols = list(self.df.columns.values[1:int(self.lineEdit.text())+1])
                self.output_cols = list(self.df.columns.values[int(self.lineEdit.text())+1:int(self.lineEdit.text())+int(self.lineEdit_2.text())+1])
                if self.lineEdit_3.text() == '若无可不填写':
                    self.un_output_cols = []
                else:
                    self.un_output_cols = list(self.df.columns.values[int(self.lineEdit.text())+int(self.lineEdit_2.text())+1:
                        int(self.lineEdit.text())+int(self.lineEdit_2.text())+int(self.lineEdit_3.text())+1])
                self.printf('-------------------------------------')
                self.printf('投入为{}'.format(self.input_cols))
                self.printf('产出为{}'.format(self.output_cols))
                self.printf('非期望产出为{}'.format(self.un_output_cols))
                if self.key == 'CCR模型':
                    if self.un_output_cols == []:
                        self.printf('您选择的模型是CCR模型,没有非期望产出')
                    else:
                        self.printf('您选择的模型是CCR模型,有非期望产出')
                    if dd != '无方向(除DDF模型外)':
                        self.printf('Warning:您选择的方向无效,默认还原为无方向')
                    model = MCCR(data=data, input_cols = self.input_cols, output_cols = self.output_cols,un_output_cols = self.un_output_cols, vv = vv )
                    self.res = model.res()
                elif self.key == 'DDF模型':
                    if self.un_output_cols == []:
                        self.printf('您选择的模型是DDF模型,没有非期望产出')
                    else:
                        self.printf('您选择的模型是DDF模型,有非期望产出')
                    if dd == '无方向(除DDF模型外)':
                        self.printf('Error:您没有选取方向,请选择合适的方向!')
                        raise Exception('您没有选取方向,请选择合适的方向')
                    model = MDDF(data=data, input_cols = self.input_cols, output_cols = self.output_cols,un_output_cols = self.un_output_cols, vv = vv, dd = dd)
                    self.res = model.res()
                elif self.key == 'SBM模型':
                    if self.un_output_cols == []:
                        self.printf('您选择的模型是SBM模型,没有非期望产出')
                    else:
                        self.printf('您选择的模型是SBM模型,有非期望产出')
                    if dd != '无方向(除DDF模型外)':
                        self.printf('Warning:您选择的方向无效,默认还原为无方向')
                    model = MSBM(data=data, input_cols = self.input_cols, output_cols = self.output_cols,un_output_cols = self.un_output_cols, vv = vv)
                    self.res = model.res()
            elif self.tabWidget.currentIndex() == 1:
                self.input_cols = list(self.df.columns.values[1:int(self.lineEdit_4.text())+1])
                self.output_cols = list(self.df.columns.values[int(self.lineEdit_4.text())+1:int(self.lineEdit_4.text())+int(self.lineEdit_5.text())+1])
                if self.lineEdit_3.text() == '若无可不填写':
                    self.un_output_cols = []
                else:
                    self.un_output_cols = list(self.df.columns.values[int(self.lineEdit_4.text())+int(self.lineEdit_5.text())+1:
                        int(self.lineEdit_4.text())+int(self.lineEdit_5.text())+int(self.lineEdit_6.text())+1])
                self.printf('-------------------------------------')
                self.printf('投入为{}'.format(self.input_cols))
                self.printf('产出为{}'.format(self.output_cols))
                self.printf('非期望产出为{}'.format(self.un_output_cols))
            # 超效率模型
                if self.skey == 'CCR超效率模型':
                    if self.un_output_cols == []:
                        self.printf('您选择的模型是CCR超效率模型,没有非期望产出')
                    else:
                        self.printf('您选择的模型是CCR超效率模型,有非期望产出')
                    if sdd != '无方向(除DDF模型外)':
                        self.printf('Warning:您选择的方向无效,默认还原为无方向')
                    model = MSCCR(data=data, input_cols = self.input_cols, output_cols = self.output_cols,un_output_cols = self.un_output_cols, vv=svv)
                    self.res = model.res()
                elif self.skey == 'DDF超效率模型':
                    if self.un_output_cols == []:
                        self.printf('您选择的模型是DDF超效率模型,没有非期望产出')
                    else:
                        self.printf('您选择的模型是DDF超效率模型,有非期望产出')
                    if sdd == '无方向(除DDF模型外)':
                        self.printf('Error:您没有选取方向,请选择合适的方向!')
                        raise Exception('您没有选取方向,请选择合适的方向!')
                    model = MSDDF(data=data, input_cols = self.input_cols, output_cols = self.output_cols,un_output_cols = self.un_output_cols, dd = dd, vv=svv)
                    self.res = model.res()
                elif self.skey == 'SBM超效率模型':
                    if self.un_output_cols == []:
                        self.printf('您选择的模型是SBM超效率模型,没有非期望产出')
                    else:
                        self.printf('您选择的模型是SBM超效率模型,有非期望产出')
                    if sdd != '无方向(除DDF模型外)':
                        self.printf('Warning:您选择的方向无效,默认还原为无方向')
                    model = MSSBM(data=data, input_cols = self.input_cols, output_cols = self.output_cols,un_output_cols = self.un_output_cols, vv=svv)
                    self.res = model.res()
            elif self.tabWidget.currentIndex() == 2:
                self.input_cols = list(self.df.columns.values[1:int(self.lineEdit_8.text())+1])
                self.output_cols = list(self.df.columns.values[int(self.lineEdit_8.text())+1:int(self.lineEdit_8.text())+int(self.lineEdit_9.text())+1])
                self.printf('-------------------------------------')
                self.printf('投入为{}'.format(self.input_cols))
                self.printf('产出为{}'.format(self.output_cols))
                num = int(len(data.index)/int(self.lineEdit_7.text()))
                period = int(self.lineEdit_7.text())
                if self.mkey == 'CCR Malmquist 指数模型':
                    self.printf('您选择的模型是CCR Malmquist 指数模型')
                    self.printf('DMU个数为{0},期数为{1}'.format(num,period))
                    model = MalmCCR(data=data, input_cols = self.input_cols, output_cols = self.output_cols,num = num, period = period, vv = self.comboBox_8.currentText())
                    self.res = model.value()
                elif self.mkey == 'SBM Malmquist 指数模型':
                    self.printf('您选择的模型是SBM Malmquist 指数模型')
                    self.printf('DMU个数为{0},期数为{1}'.format(num,period))
                    model = MalmSBM(data=data, input_cols = self.input_cols, output_cols = self.output_cols,num = num, period = period, vv = self.comboBox_8.currentText())
                    self.res = model.value()
            self.printf('计算已结束')
            self.printf('-------------------------------------')
            self.final(self.res)
        except:
            self.printf('出错，请检查步骤是否正确')
            self.printf('可能的原因有:')
            self.printf('1.数据格式设置有误,请参照正确设置方式;')
            self.printf('2.您的系统没有该求解器,请重新选取。')
            self.printf('3.您的模型参数设置有误,请重新参考以上Error提示。')
            self.printf('-------------------------------------')
    
    def save(self):
        path = os.path.split(path_openfile_name)[0]
        row = len(self.res.index)
        if self.tabWidget.currentIndex() == 0:
            self.res.loc[row] = nan
            self.res.iloc[row,0] = '该结果通过Deatool计算生成，模型为{}'.format(self.key)
            self.res.to_excel(path+r'\结果_{}.xlsx'.format(self.key), index=False)
        elif self.tabWidget.currentIndex() == 1:
            self.res.loc[row] = nan
            self.res.iloc[row,0] = '该结果通过Deatool计算生成，模型为{}'.format(self.skey)
            self.res.to_excel(path+r'\结果_{}.xlsx'.format(self.skey), index=False)
        elif self.tabWidget.currentIndex() == 2:
            self.res.loc[row] = nan
            self.res.iloc[row,0] = '该结果通过Deatool计算生成，模型为{}'.format(self.mkey)
            self.res.to_excel(path+r'\结果_{}.xlsx'.format(self.mkey), index=False)
# 运行界面
    def printf(self, mes):
        self.textBrowser.append(mes)  # 在指定的区域显示提示信息
        self.cursot = self.textBrowser.textCursor()
        self.textBrowser.moveCursor(self.cursot.End)