from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon
from url_bar import URLBar

class TabbedBrowser(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create TabWidget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)

        self.layout.addWidget(self.tabs)

        # Create first tab
        self.add_tab()

    def add_tab(self):
        browser = QWebEngineView()
        url_bar = URLBar()
        url_bar.url_changed.connect(browser.setUrl)
        browser.urlChanged.connect(url_bar.update_url)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(url_bar)
        container_layout.addWidget(browser)

        index = self.tabs.addTab(container, "New Tab")
        self.tabs.setCurrentIndex(index)

        browser.loadFinished.connect(lambda _, i=index, browser=browser:
                                     self.update_tab_title(i, browser))
        
        # Connect iconChanged signal to update_tab_icon method
        browser.iconChanged.connect(lambda icon, i=index: self.update_tab_icon(i, icon))

        browser.setUrl(QUrl("https://www.google.com"))
        return browser, url_bar

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.add_tab()

    def update_tab_title(self, index, browser):
        if index == self.tabs.currentIndex():
            title = browser.page().title()
            self.tabs.setTabText(index, title[:15] + '...' if len(title) > 15 else title)

    def update_tab_icon(self, index, icon):
        self.tabs.setTabIcon(index, icon)

    def current_tab_changed(self, index):
        if index != -1:
            url = self.tabs.widget(index).findChild(QWebEngineView).url().toString()
            self.tabs.widget(index).findChild(URLBar).setText(url)

    def current_browser(self):
        return self.tabs.currentWidget().findChild(QWebEngineView)

    def current_url_bar(self):
        return self.tabs.currentWidget().findChild(URLBar)