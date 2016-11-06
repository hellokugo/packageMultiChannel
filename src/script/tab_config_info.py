import os.path
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import logging

import log_utils
import channel_util
import custom_edit

class checkConfigInfo:

    def __init__(self,parent,tabWidget,Windows,settings):
        self.parent = parent
        configPathLabelT = QLabel("Path:       ")
        rememberPath = None
        try:
            rememberPath = bool(int(settings.value("rememberpath",
                1 if Windows else 0)))
        except ValueError:
            rememberPath = True if rememberPath == "true" else False
        log_utils.getLogger().debug("ConfigureInfo path rememberPath:" + str(rememberPath))
        if rememberPath:
            log_utils.getLogger().debug("ConfigureInfo path:" + str(settings.value("path")))
            apkPath = settings.value("path") or os.getcwd()
        else:
            apkPath = (sys.argv[1] if len(sys.argv) > 1 and
                    QFile.exists(sys.argv[1]) else os.getcwd())
        self.ConfigPathEdit = custom_edit.AutoEdit(parent)
        self.ConfigPathEdit.setFocusPolicy(Qt.NoFocus)
        self.ConfigPathEdit.setStyleSheet("color:gray")
        self.ConfigPathEdit.setPlaceholderText('支持直接拖拽文件到文本框')
        ConfigPathButton = QPushButton("&Path")

        self.ConfigLogBrowser = QTextBrowser()
        self.ConfigLogBrowser.setLineWrapMode(QTextEdit.NoWrap)

        ConfigTopLayout = QHBoxLayout()
        ConfigTopLayout.addWidget(configPathLabelT)
        ConfigTopLayout.addWidget(self.ConfigPathEdit, 1)
        ConfigTopLayout.addWidget(ConfigPathButton)

        ConfigCheckChannelIdButton = QPushButton("&查看")

        ConfigCheckLayout = QHBoxLayout()
        ConfigCheckLayout.addStretch()
        # ConfigCheckLayout.addWidget(ConfigCheckInfoButton)
        ConfigCheckLayout.addWidget(ConfigCheckChannelIdButton)
        ConfigCheckLayout.addStretch()

        layout = QVBoxLayout()
        layout.addLayout(ConfigTopLayout)
        layout.addLayout(ConfigCheckLayout)
        layout.addWidget(self.ConfigLogBrowser)

        ConfigInfoWidget = QFrame()
        ConfigInfoWidget.setLayout(layout)

        tabWidget.addTab(ConfigInfoWidget,'查看渠道')

        parent.connect(ConfigPathButton, SIGNAL("clicked()"), self.configSetPath)
        parent.connect(ConfigCheckChannelIdButton, SIGNAL("clicked()"), self.configChannelIdCheck)
        parent.connect(log_utils.aSigalOutLog,SIGNAL("displayLog(QString)"), parent.displayLog)

    def configSetPath(self):
        path = QFileDialog.getOpenFileName(self.parent,
                "请选择要查看信息的apk", self.ConfigPathEdit.text(), "*.apk")
        if path:
            self.ConfigPathEdit.setText(QDir.toNativeSeparators(path))

    def configChannelIdCheck(self):
        self.parent.logControl = self.ConfigLogBrowser
        self.ConfigLogBrowser.clear()

        titleMsg = '查看apk渠道信息'

        path = self.ConfigPathEdit.text()
        log_utils.getLogger().debug(path)
        if self.checkFormat(titleMsg,path):
            result = channel_util.checkApkComment(path)
            if result:
                self.parent.showMsgBox(titleMsg,result)

    def checkFormat(self,title,path):
        titleMsg = title
        if not path:
            self.parent.showMsgBox(titleMsg,"你输入的包名为空，请检查!")
            return False
        elif not (os.path.exists(path)):
            self.parent.showMsgBox(titleMsg,"你输入的apk路径格式不存在，请检查!")
            return False
        elif not (path.endswith('apk') or path.endswith('zip')):
            self.parent.showMsgBox(titleMsg,"你输入的apk路径格式不正确，请检查!")
            return False
        return True
