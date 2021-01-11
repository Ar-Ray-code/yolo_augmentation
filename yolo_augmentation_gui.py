import yolo_augmentation as yoloa
import filters.filter as fil

import sys
import os
from tqdm import tqdm

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *


from ui import Ui_MainWindow

class gui(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super(gui,self).__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def select_folder(self):
        rootpath = os.path.abspath(os.path.dirname("__file__"))
        path = QFileDialog.getExistingDirectory(None, "rootpath", rootpath)
        self.lineEdit_2.setText(path)

    def start_button(self):
        path = self.lineEdit_2.text()
        img_format = self.lineEdit.text()
        #print(path)
        #print(img_format)

        bar = tqdm(total = len(yoloa.get_folder_list(path,img_format))*23)
        yoloa.flip_img(path, yoloa.get_folder_list(path,img_format),img_format,bar)
        yoloa.soltpaper_img(path, yoloa.get_folder_list(path,img_format),img_format,bar)
        yoloa.brightness_img(path, yoloa.get_folder_list(path,img_format),img_format,bar)
        
        self.label.setText("Finish!")
        
        

    def show_progress(self):
        self.setWindowTitle('Progress Bar')
        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 0, 300, 25)
        self.progress.setMaximum(100)

    def exit_qt(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qt_gui = gui()
    qt_gui.show()
    sys.exit(app.exec_())