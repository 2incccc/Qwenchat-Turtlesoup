import sys
from PyQt6.QtWidgets import QApplication
from ui_components import ChatQwen

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChatQwen()
    ex.show()
    sys.exit(app.exec())
