from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QPushButton, QVBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap, QPalette, QColor
from chat_logic import get_answer, init_session
from http import HTTPStatus
class ChatQwen(QWidget):
    
    def __init__(self):
        super().__init__()
        self.response = None  # 初始化response属性
        self.initUI()

    def initUI(self):
        self.resize(600, 400)
        self.setWindowTitle('基于Qwen大模型的海龟汤游戏')

        # 设置背景颜色
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))  # 浅灰色背景
        self.setPalette(palette)
        
        # 创建堆叠窗口
        self.stackedWidget = QStackedWidget()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stackedWidget)
        
        # 创建开始页
        self.startPage = QWidget()
        self.startPageLayout = QVBoxLayout()
        self.startPage.setLayout(self.startPageLayout)
        
        # 添加图片
        self.imageLabel = QLabel()
        pixmap = QPixmap('demo/img/Snipaste_2024-06-11_22-47-33.png')  # 替换为你的图片路径
        scaled_pixmap = pixmap.scaled(600, 500, Qt.AspectRatioMode.KeepAspectRatio)  # 调整图片大小
        self.imageLabel.setPixmap(scaled_pixmap)
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.startPageLayout.addWidget(self.imageLabel)
        
        # 添加开始按钮
        self.startButton = QPushButton('开始游戏')
        self.startButton.setFont(QFont('Arial', 14))
        self.startButton.setStyleSheet("""
            QPushButton { 
                background-color: #A25423; 
                color: white; 
                border-radius: 10px; 
                padding: 10px 20px;
                min-width: 150px; 
            }
            QPushButton:pressed { 
                background-color: #D09C00; 
            }
            QPushButton:hover {
                background-color: #B5651D;
            }
        """)
        self.startButton.clicked.connect(self.showChatPage)
        self.startPageLayout.addWidget(self.startButton, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 创建聊天页
        self.chatPage = QWidget()
        self.chatPageLayout = QGridLayout()
        self.chatPage.setLayout(self.chatPageLayout)
        
        self.label = QLabel('👨：')
        self.label.setFont(QFont('Arial', 12))
        self.lineEdit = QLineEdit()
        self.lineEdit.setFont(QFont('Arial', 12))
        self.lineEdit.setPlaceholderText('你的猜想是什么？')
        self.okButton = QPushButton('发送')
        self.okButton.setFont(QFont('Arial', 12))
        self.textEdit = QTextEdit()
        self.textEdit.setFont(QFont('Arial', 12))
        self.textEdit.setReadOnly(True)  # 设置文本编辑器为只读

        self.chatPageLayout.setSpacing(15)
        
        self.chatPageLayout.addWidget(self.label, 0, 0)
        self.chatPageLayout.addWidget(self.lineEdit, 0, 1)
        self.chatPageLayout.addWidget(self.okButton, 0, 2)
        self.chatPageLayout.addWidget(self.textEdit, 1, 0, 1, 3)
        
        self.okButton.pressed.connect(self.displayUserInput)
        
        # 添加页面到堆叠窗口
        self.stackedWidget.addWidget(self.startPage)
        self.stackedWidget.addWidget(self.chatPage)

        # 显示开始页
        self.stackedWidget.setCurrentWidget(self.startPage)

    def displayUserInput(self):
        question = self.lineEdit.text()
        if not question.strip():
            return  # 如果输入为空，不执行任何操作

        # 显示用户的问题，添加换行和居中
        current_text = self.textEdit.toHtml()
        user_text = f"""
<div style="display: flex; justify-content: flex-start;">
    <div style="max-width: 90%; padding: 10px; background-color: #FFD2A7; border-radius: 10px; font-size: 16px;">
        <span style="font-size: 24px;">👨</span> {question}
    </div>
</div>
"""
        self.textEdit.setHtml(current_text + user_text)
        self.lineEdit.clear()  # 清除输入框内容

        # 滚动到最后
        self.textEdit.verticalScrollBar().setValue(self.textEdit.verticalScrollBar().maximum())

        # 使用QTimer来延迟调用获取模型回答的方法
        QTimer.singleShot(100, lambda: self.getAnswer(question))

    def getAnswer(self, question):
        current_text = self.textEdit.toHtml()
        
        # 如果self.response为空，意味着是第一次调用，需要从showChatPage中获取session_id
        if self.response:
            session_id = self.response.output.session_id
        else:
            session_id = None

        response = get_answer(question, session_id)
        
        if response.status_code != HTTPStatus.OK:
            answer = f'Error: {response.message}'
        else:
            answer = response.output.text
            self.response = response  # 更新self.response以保持会话的连续性

        # 显示模型的回答，添加换行和居中
        bot_text = f"""
<div style="display: flex; justify-content: flex-end;">
    <div style="max-width: 70%; padding: 10px; background-color: #D5E8D4; border-radius: 10px; font-size: 16px;">
        <span style="font-size: 24px;">🤖</span> {answer} <span style="font-size: 24px;"></span>
    </div>
</div>
"""

        self.textEdit.setHtml(current_text + bot_text)
        self.textEdit.verticalScrollBar().setValue(self.textEdit.verticalScrollBar().maximum()) 

    def showChatPage(self):
        self.stackedWidget.setCurrentWidget(self.chatPage)
        
        # 设置初始对话内容
        self.textEdit.clear()

        self.response = init_session()
        
        if self.response.status_code != HTTPStatus.OK:
            answer = f'Error: {self.response.message}'
        else:
            answer = self.response.output.text
        
        end_text = '🤖: 海龟汤情景推理的游戏规则：作为裁判，我会给出一个简短的离奇故事，称为“汤面”。你可以轮流提问，只能问“是”或“否”问题。例如，“这个人是自杀的吗？”我会回答“是”或“否”，或指出与真相无关。通过提问和推理，逐步揭开故事的全貌。当你们能复述完整的故事时，游戏结束。\n'
        self.textEdit.setPlainText(f'🤖:{answer}\n\n' + end_text)
