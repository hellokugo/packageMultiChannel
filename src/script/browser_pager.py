import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import env
import os
import log_utils

class MyBrowser(QWidget):

    def __init__(self, parent = None):
        super(MyBrowser, self).__init__(parent)
        self.createLayout()

    def search(self):
        log_utils.getLogger().debug("EXTRA_DIR:" + env.EXTRA_DIR)
        address = "file:///" + os.path.join(env.EXTRA_DIR, "readme", env.README_TOOLS)
        log_utils.getLogger().debug("address:" + address)
        if address:
            if address.find('://') == -1:
                address = 'http://' + address
            url = QUrl(address)
            self.webView.load(url)

    def createLayout(self):
        self.setWindowTitle("About")

        self.webView = QWebView()
        layout = QVBoxLayout()
        layout.addWidget(self.webView)
        self.setLayout(layout)

        self.search()