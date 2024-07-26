from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtWidgets import QLineEdit
import urllib.parse

class URLBar(QLineEdit):
    url_changed = pyqtSignal(QUrl)

    def __init__(self):
        super().__init__()
        self.returnPressed.connect(self.navigate_to_url)
        self.setFocusPolicy(Qt.ClickFocus)
        self.mousePressEvent = self.highlight_url_bar

    def navigate_to_url(self):
        url = self.text()
        if ' ' in url or '.' not in url:
            # Treat as a search query
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(url)}"
            self.url_changed.emit(QUrl(search_url))
        else:
            # Treat as a URL
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            self.url_changed.emit(QUrl(url))

    def highlight_url_bar(self, event):
        self.selectAll()
        QLineEdit.mousePressEvent(self, event)

    def update_url(self, q):
        self.setText(q.toString())