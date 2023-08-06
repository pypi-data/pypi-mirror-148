import os
import sys

# deatool_root = r"C:\Users\wangy\Desktop\Project\deatools-mip"
# os.chdir(deatool_root)
# cwd = os.getcwd()
# sys.path.insert(0,cwd)

from deatool.deasolver import Tables
from PySide2.QtWidgets import *
from PySide2 import QtCore

def run():
    #QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)
    tables = Tables()
    tables.setWindowOpacity(0.975)
    tables.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()