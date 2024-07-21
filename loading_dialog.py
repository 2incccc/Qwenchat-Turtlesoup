from PyQt6.QtWidgets import QDialog, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMovie

def show_loading_dialog(parent):
    dialog = QDialog(parent)
    dialog.setWindowTitle('加载中')
    dialog.setModal(True)
    dialog.setFixedSize(200, 200)
    dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # 去掉边框

    # 设置加载动画
    label = QLabel(dialog)
    label.setFixedSize(200, 200)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    movie = QMovie('demo/img/loading.gif')  # 替换为你的加载动画图片路径
    label.setMovie(movie)
    movie.start()

    # 设置背景颜色和透明度
    dialog.setStyleSheet("""
        QDialog {
            background-color: rgba(255, 255, 255, 200);
            border-radius: 10px;
        }
    """)

    return dialog
