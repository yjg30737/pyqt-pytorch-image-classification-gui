import numpy as np

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView


class ImageView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.__aspectRatioMode = Qt.KeepAspectRatio
        self.__gradient_enabled = False
        self.__initVal()

    def __initVal(self):
        self._scene = QGraphicsScene()
        self._p = QPixmap()
        self._item = ''

    def displayPillowImage(self, image):
        img_array = np.array(image)

        # Convert NumPy array to QImage
        if img_array.ndim == 3:
            h, w, ch = img_array.shape
            bytesPerLine = ch * w
            qim = QImage(img_array.data, w, h, bytesPerLine, QImage.Format_RGB888)
        else:
            raise ValueError("Unsupported image dimension: {}".format(img_array.ndim))

        pixmap = QPixmap.fromImage(qim)

        self._scene.clear()

        self._scene.addPixmap(pixmap)

        self._scene.setSceneRect(QRectF(0, 0, pixmap.width(), pixmap.height()))
        self.setScene(self._scene)
        self.fitInView(self.sceneRect(), self.__aspectRatioMode)

    def setAspectRatioMode(self, mode):
        self.__aspectRatioMode = mode

    def resizeEvent(self, e):
        self.fitInView(self.sceneRect(), self.__aspectRatioMode)
        return super().resizeEvent(e)