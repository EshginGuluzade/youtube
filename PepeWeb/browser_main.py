# main.py

import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar
from PyQt5.QtWebEngineWidgets import QWebEngineView
from url_bar import URLBar

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Simple Browser')
        self.setGeometry(100, 100, 1024, 1024)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://www.google.com'))
        self.setCentralWidget(self.browser)

        # Navigation bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Back button
        back_btn = navbar.addAction('Back')
        back_btn.triggered.connect(self.browser.back)

        # Forward button
        forward_btn = navbar.addAction('Forward')
        forward_btn.triggered.connect(self.browser.forward)

        # Reload button
        reload_btn = navbar.addAction('Reload')
        reload_btn.triggered.connect(self.browser.reload)

        # Custom Home button
        home_btn = navbar.addAction('Home')
        home_btn.triggered.connect(self.navigate_home)

        # Custom URL Bar
        self.url_bar = URLBar()
        self.url_bar.url_changed.connect(self.browser.setUrl)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.url_bar.update_url)

    def navigate_home(self):
        self.browser.setUrl(QUrl('https://www.google.com'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = SimpleBrowser()
    browser.show()
    sys.exit(app.exec_())