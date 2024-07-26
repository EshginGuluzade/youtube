import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar
from tabs import TabbedBrowser

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Simple Browser')
        self.setGeometry(100, 100, 1024, 768)

        self.tabbed_browser = TabbedBrowser(self)
        self.setCentralWidget(self.tabbed_browser)

        # Navigation bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Back button
        back_btn = navbar.addAction('Back')
        back_btn.triggered.connect(self.back)

        # Forward button
        forward_btn = navbar.addAction('Forward')
        forward_btn.triggered.connect(self.forward)

        # Reload button
        reload_btn = navbar.addAction('Reload')
        reload_btn.triggered.connect(self.reload)

        # Custom Home button
        home_btn = navbar.addAction('Home')
        home_btn.triggered.connect(self.navigate_home)

        # New Tab button
        new_tab_btn = navbar.addAction('New Tab')
        new_tab_btn.triggered.connect(self.tabbed_browser.add_tab)

    def back(self):
        self.tabbed_browser.current_browser().back()

    def forward(self):
        self.tabbed_browser.current_browser().forward()

    def reload(self):
        self.tabbed_browser.current_browser().reload()

    def navigate_home(self):
        self.tabbed_browser.current_browser().setUrl(QUrl('https://www.google.com'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = SimpleBrowser()
    browser.show()
    sys.exit(app.exec_())