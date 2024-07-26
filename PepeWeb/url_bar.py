from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QMouseEvent
import urllib.parse

class URLBar(QLineEdit):
    url_changed = pyqtSignal(QUrl)

    def __init__(self):
        super().__init__()
        self.returnPressed.connect(self.navigate_to_url)
        self.setFocusPolicy(Qt.ClickFocus)

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

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        self.selectAll()

    def update_url(self, q):
        self.setText(q.toString())