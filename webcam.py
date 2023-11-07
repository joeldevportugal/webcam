import cv2
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage, QClipboard, QGuiApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class FrWebcam(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Menu Webcam dev Joel 2023 ")
        self.setGeometry(100, 100, 640, 480)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setFixedSize(640, 600)


         # Carregando uma imagem para ser usada como ícone
        icon = QIcon(r"C:\Users\HP\Desktop\Programas em python\Webcam\Icon.ico")  # Substitua pelo caminho da sua imagem
        
        # Definindo o ícone da janela
        self.setWindowIcon(icon)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.CMBCamaras = QComboBox()
        self.layout.addWidget(self.CMBCamaras)

        self.BtnIniciar = QPushButton("Iniciar")
        self.layout.addWidget(self.BtnIniciar)
        self.BtnIniciar.clicked.connect(self.start_capture)

        self.PicImagem = QLabel(self)
        self.layout.addWidget(self.PicImagem)

        self.BtnGuardar = QPushButton("Guardar")
        self.layout.addWidget(self.BtnGuardar)
        self.BtnGuardar.clicked.connect(self.save_image)

        self.BtnEncerrar = QPushButton("Encerrar")
        self.layout.addWidget(self.BtnEncerrar)
        self.BtnEncerrar.clicked.connect(self.stop_capture)

        self.BtnSair = QPushButton("Sair")
        self.layout.addWidget(self.BtnSair)
        self.BtnSair.clicked.connect(self.close)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.clipboard = QGuiApplication.clipboard()

        self.detect_cameras()  # Detecta e preenche as câmeras disponíveis

    def detect_cameras(self):
        cameras = cv2.VideoCapture(0).getBackendName()  # Detecta as câmeras disponíveis
        for index, camera in enumerate(cameras):
            self.CMBCamaras.addItem(f"Camera {index}: {camera}")

    def start_capture(self):
        if not self.timer.isActive():
            selected_camera_index = self.CMBCamaras.currentIndex()
            self.videoCapture = cv2.VideoCapture(selected_camera_index)
            self.timer.start(30)
        QMessageBox.information(self, "Webcam Iniciada", "A sua Webcam Esta Iniciada Com sucesso!")        

    def stop_capture(self):
        if self.timer.isActive():
            self.timer.stop()
            self.videoCapture.release()
            self.PicImagem.clear()
            QMessageBox.information(self, "Webcam Encerrada", "A sua Webcam Esta Encerrada!")         

    def update_frame(self):
        ret, frame = self.videoCapture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = QPixmap.fromImage(convertToQtFormat)
            self.PicImagem.setPixmap(p)

    def save_image(self):
        if self.PicImagem.pixmap():
            image = self.PicImagem.pixmap().toImage()
        if image.save("imagem.png", "PNG"):
            self.clipboard.setPixmap(self.PicImagem.pixmap())
        QMessageBox.information(self, "Sucesso", "Imagem guardada com sucesso.")                          


    def closeEvent(self, event):
        self.stop_capture()
        super().closeEvent(event)
        QMessageBox.information(self, "Aplicação encerrada", "A sua aplicação vai ser Encerrada")

def main():
    app = QApplication(sys.argv)
    window = FrWebcam()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
