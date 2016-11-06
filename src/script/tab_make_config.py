import os.path
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import log_utils
import channel_util
import custom_edit

class makeConfiguraton:

    def __init__(self,parent,tabWidget,Windows,settings):
        self.parent = parent
        makeConfigLabelTitle = QLabel("Path:        ")
        rememberPath = None
        try:
            rememberPath = bool(int(settings.value("rememberpath",
                1 if Windows else 0)))
        except ValueError:
            rememberPath = True if rememberPath == "true" else False

        if rememberPath:
            log_utils.getLogger().debug("path:" + str(settings.value("path")))
            apkPath = settings.value("path") or os.getcwd()
        else:
            apkPath = (sys.argv[1] if len(sys.argv) > 1 and
                    QFile.exists(sys.argv[1]) else os.getcwd())
        self.makeConPathEdit = custom_edit.AutoEdit(parent)
        self.makeConPathEdit.setFocusPolicy(Qt.NoFocus)
        self.makeConPathEdit.setPlaceholderText('支持直接拖拽文件到文本框')

        makeConPathButton = QPushButton("&Select Path")

        makePathLayout = QHBoxLayout()
        makePathLayout.addWidget(makeConfigLabelTitle)
        makePathLayout.addWidget(self.makeConPathEdit, 1)
        makePathLayout.addWidget(makeConPathButton)

        makeConChannelLabelTitle = QLabel("Channel:     ")
        self.makeConChannelEdit = QLineEdit()
        self.makeConChannelEdit.setPlaceholderText('渠道间请用\',\'作为分隔')

        makeChannelLayout = QHBoxLayout()
        makeChannelLayout.addWidget(makeConChannelLabelTitle)
        makeChannelLayout.addWidget(self.makeConChannelEdit)

        makeConExtraLabelTitle = QLabel("Extra:       ")
        self.makeConExtraLabelEdit = QLineEdit()
        self.makeConExtraLabelEdit.setPlaceholderText('可以为空')

        makeExtraLayout = QHBoxLayout()
        makeExtraLayout.addWidget(makeConExtraLabelTitle)
        makeExtraLayout.addWidget(self.makeConExtraLabelEdit)

        makeConOutputLabelTitle = QLabel("OutputPath:  ")
        rememberPath = None
        try:
            rememberPath = bool(int(settings.value("rememberpath",
                1 if Windows else 0)))
        except ValueError:
            rememberPath = True if rememberPath == "true" else False

        # log_utils.getLogger().debug("path rememberPath:" + str(rememberPath))

        if rememberPath:
            log_utils.getLogger().debug("path:" + str(settings.value("path")))
            apkPath = settings.value("path") or os.getcwd()
        else:
            apkPath = (sys.argv[1] if len(sys.argv) > 1 and
                    QFile.exists(sys.argv[1]) else os.getcwd())
        self.makeConOutputPathEdit = custom_edit.AutoEdit(parent)
        self.makeConOutputPathEdit.setFocusPolicy(Qt.NoFocus)
        self.makeConOutputPathEdit.setPlaceholderText('支持直接拖拽文件到文本框')
        makeConOutputPathButton = QPushButton("&Select Path")

        makeOutputLayout = QHBoxLayout()
        makeOutputLayout.addWidget(makeConOutputLabelTitle)
        makeOutputLayout.addWidget(self.makeConOutputPathEdit, 1)
        makeOutputLayout.addWidget(makeConOutputPathButton)

        makeConClickButton = QPushButton("&Start")
        makeClickLayout = QHBoxLayout()
        makeClickLayout.addStretch()
        makeClickLayout.addWidget(makeConClickButton)
        makeClickLayout.addStretch()

        makeTotallayout = QVBoxLayout()
        makeTotallayout.addLayout(makePathLayout)
        makeTotallayout.addLayout(makeChannelLayout)
        makeTotallayout.addLayout(makeExtraLayout)
        makeTotallayout.addLayout(makeOutputLayout)
        makeTotallayout.addLayout(makeClickLayout)

        # 实现layout下为空白
        makeTotallayout.addStretch()

        makeConfigWidget = QFrame()
        makeConfigWidget.setLayout(makeTotallayout)

        tabWidget.addTab(makeConfigWidget,'生成配置')

        parent.connect(makeConPathButton, SIGNAL("clicked()"), self.makeConApkPath)
        parent.connect(makeConOutputPathButton, SIGNAL("clicked()"), self.makeConOutputPath)
        parent.connect(makeConClickButton, SIGNAL("clicked()"), self.makeConStart)

    def makeConApkPath(self):
        path = QFileDialog.getOpenFileName(self.parent,
                "请选择你要打入渠道的apk包", self.makeConPathEdit.text(), "*.apk")
        if path:
            self.makeConPathEdit.setText(QDir.toNativeSeparators(path))

    def makeConOutputPath(self):
        dialog = QFileDialog()
        dialog.setWindowTitle("请选择你的输出路径")

        # 关键：这里指定只能选择文件夹
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dialog.exec()
        path = dialog.selectedFiles()[0]
        if path:
            self.makeConOutputPathEdit.setText(QDir.toNativeSeparators(path))

    def makeConStart(self):

        self.parent.logControl = None

        titleMsg = 'fail'

        originApk = self.makeConPathEdit.text()
        channelList = self.makeConChannelEdit.text()
        extraInfo = self.makeConExtraLabelEdit.text()
        outPath = self.makeConOutputPathEdit.text()
        log_utils.getLogger().debug(originApk)
        log_utils.getLogger().debug(extraInfo)
        log_utils.getLogger().debug(outPath)


        if self.checkFormat(titleMsg,originApk,outPath,channelList):
            result = channel_util.changeNativeChannel(originApk,channelList,extraInfo,outPath)
            if result == '':
                self.parent.showMsgBox("Success","请到 " + outPath + " 目录下查看！")
            else:
                originName = os.path.split(originApk)[1]
                tempFile = os.path.join(outPath,originName)
                if os.path.exists(tempFile):
                    os.remove(tempFile)
                self.parent.showMsgBox(titleMsg,result)

    def checkFormat(self,titleMsg,originApk,outPath,channelList):

        if not (originApk or outPath):
            self.parent.showMsgBox(titleMsg,"你输入的apk包名或输出路径为空，请检查!")
            return False
        elif not (os.path.exists(originApk) and os.path.exists(outPath)):
            self.parent.showMsgBox(titleMsg,"你输入的apk或输出目录不存在，请检查!")
            return False
        elif not (originApk.endswith('apk') or originApk.endswith('zip')):
            self.parent.showMsgBox(titleMsg,"你输入的apk路径格式不正确，请检查!")
            return False
        elif not (os.path.exists(outPath) or os.path.isdir(outPath)):
            self.parent.showMsgBox(titleMsg,"你输入的输出路径格式不是文件夹，请检查!")
            return False
        elif not channelList:
            self.parent.showMsgBox(titleMsg,"请输入渠道号!")
            return False
        elif '，' in channelList:
            self.parent.showMsgBox(titleMsg,"请检查输入渠道号，是否包含中文字符‘，’？")
            return False

        return True
