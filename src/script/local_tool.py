# -*- coding: utf-8 -*-
'''
/*
 * Copyright (C) 2016 hellougo
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
'''
import os
import os.path
import platform
import stat
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import json
import logging

# from PyQt4 import QtGui, QtCore

import env
import re
import log_utils
import zipfile
import channel_util
import custom_edit
from tab_make_config import makeConfiguraton
from tab_config_info import checkConfigInfo
from browser_pager import MyBrowser

__version__ = "1.0.0"

Windows = sys.platform.lower().startswith(("win", "microsoft"))

QCoreApplication.setOrganizationName("demo");
QCoreApplication.setOrganizationDomain("hellokugo");
QCoreApplication.setApplicationName("modifyChannal");
settings = QSettings()

class Form(QMainWindow):

    def __init__(self):
        super(Form, self).__init__(None)

        # 窗口添加icon
        iconPath = os.path.join(env.EXTRA_DIR, "icon", env.ICON_TOOLS)
        self.setWindowIcon(QIcon(iconPath))
        self.setWindowTitle("打渠道工具")

        about = QAction(QIcon(''), 'Readme', self)
        self.connect(about, SIGNAL('triggered()'), self.goAbout)

        exit = QAction(QIcon(''), 'Exit', self)
        self.connect(exit, SIGNAL('triggered()'), SLOT('close()'))

        menubar = self.menuBar()

        file = menubar.addMenu('&tools')
        file.addAction(about)
        file.addAction(exit)

        self.setGeometry(400, 400, 600, 600)
        self.index = 1
        self.logControl = QTextBrowser()
        self.tabWidget = QTabWidget()

        # 不能直接调用类的方法，必须要赋于self.XXXX才可以
        self.checkConfig = checkConfigInfo(self,self.tabWidget,Windows,settings)
        self.makeConfig = makeConfiguraton(self,self.tabWidget,Windows,settings)

        self.setCentralWidget(self.tabWidget)

        print("log start")

    def goAbout(self):
        self.aboutBrowser = MyBrowser()
        self.aboutBrowser.show()

    def closeEvent(self, *args, **kwargs):
        self.remember()
        return QMainWindow.closeEvent(self, *args, **kwargs)

    def ProcessSend(self):
        #使用信号和槽来处理日志
        global aSigalOutLog
        print('测试标准输出')

    def showMsgBox(self,title,msg):
        QMessageBox.information(self, title,msg)

    def displayLog(self, log, level=logging.DEBUG):
        if not self.logControl:
            return

        if(log is not None and log.find("DEBUG")== -1):
            self.logControl.append("<font color=green>{}</font>".format(
                            log.replace("\n", "")))
        elif(level ==log_utils.getLogger().DEBUG ):
            self.logControl.append("<font color=blue>{}</font>".format(
            log.replace("\n", "")))
        elif (level ==log_utils.getLogger().INFO ):
            self.logControl.append("<font color=green>{}</font>".format(
                            log.replace("\n", "")))
        else:
            self.logControl.append("<font color=red>{}</font>".format(
                            log.replace("\n", "")))

if __name__ == "__main__":
    qtPluginsPath = env.PLUGINS_DIR
    QApplication.addLibraryPath(qtPluginsPath)
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qtPluginsPath
    print(os.environ)
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
