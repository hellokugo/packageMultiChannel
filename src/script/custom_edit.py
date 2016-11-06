# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtGui, QtCore

class AutoEdit(QtGui.QLineEdit):
    def __init__(self,parent):
        super(AutoEdit,self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(AutoEdit, self).dragEnterEvent(event)


    def dragMoveEvent(self, event):
        super(AutoEdit, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            #遍历输出拖动进来的所有文件路径
            for url in event.mimeData().urls():
                self.setText(str(url.toLocalFile()))
            event.acceptProposedAction()
        else:
            super(AutoEdit,self).dropEvent(event)