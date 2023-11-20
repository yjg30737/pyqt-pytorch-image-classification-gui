import os, sys

from imageView import ImageView
from loadingLbl import LoadingLabel
from script import ImagePredictor

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLineEdit, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt, QCoreApplication, QThread, pyqtSignal
from PyQt5.QtGui import QFont

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont('Arial', 12))


class Thread(QThread):
    generateFinished = pyqtSignal(str)

    def __init__(self, image, pred: ImagePredictor):
        super(Thread, self).__init__()
        self.__image = image
        self.__pred = pred

    def run(self):
        try:
            self.generateFinished.emit(self.__pred.predict_image(self.__image))
        except Exception as e:
            raise Exception(e)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        model_path = 'result.pth'
        self.__pred = ImagePredictor(model_path)

    def __initUi(self):
        self.setWindowTitle('PyTorch Image Classification')

        self.__urlLineEdit = QLineEdit()
        self.__urlLineEdit.setPlaceholderText('Input the URL...')
        self.__urlLineEdit.textChanged.connect(self.__urlChanged)

        self.__view = ImageView()

        self.__runBtn = QPushButton('Run')
        self.__runBtn.setEnabled(False)
        self.__runBtn.clicked.connect(self.__run)

        self.__waitLbl = LoadingLabel()
        self.__waitLbl.setVisible(False)

        self.__resultLbl = QLabel()
        self.__resultLbl.setAlignment(Qt.AlignCenter)
        self.__resultLbl.setVisible(False)

        lay = QVBoxLayout()
        lay.addWidget(self.__urlLineEdit)
        lay.addWidget(self.__view)
        lay.addWidget(self.__runBtn)
        lay.addWidget(self.__waitLbl)
        lay.addWidget(self.__resultLbl)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)

    def __urlChanged(self, url):
        self.__runBtn.setEnabled(url.strip() != '')

    def __run(self):
        image_url = self.__urlLineEdit.text()
        image = self.__pred.get_image_from_url(image_url)
        self.__view.displayPillowImage(image)
        self.__t = Thread(image, self.__pred)
        self.__t.started.connect(self.__started)
        self.__t.generateFinished.connect(self.__generateFinished)
        self.__t.finished.connect(self.__finished)
        self.__t.start()

    def __started(self):
        self.__waitLbl.setVisible(True)
        self.__runBtn.setEnabled(False)

    def __generateFinished(self, result):
        self.__resultLbl.setText(result)

    def __finished(self):
        self.__waitLbl.setVisible(False)
        self.__resultLbl.setVisible(True)
        self.__runBtn.setEnabled(True)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())