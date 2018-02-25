#!/usr/bin/python3
"""
Icons from https://icons8.com/icon/set/image/all
"""
import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp, QApplication,
    QFileDialog, QHBoxLayout, QLabel, QScrollArea, QSizePolicy,
                             QMessageBox)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from myimage import MyImage

class SimpleImageViewer(QMainWindow):

    def __init__(self, *imgPath):
        super().__init__()
        self.tempPath = "./temp/"
        self.defaultPath = "/home/maria/Pictures/temp111/"
        if imgPath:
            self.imgPath = imgPath
        else:
            self.imgPath = ''
        self.__init_GUI()


    def __init_GUI(self):
        self.setWindowTitle('Simple Image Viewer')
        self.setWindowIcon(QIcon('./icons/main-window-color.png'))
        
        self.set_menus()
                       
        #image
        self.imageLabel = QLabel(self)
        self.__init_img()
        self.imageLabel.setPixmap(self.pixmap)
        self.imageLabel.setScaledContents(False)
        
        self.area = QScrollArea()
        self.area.setWidget(self.imageLabel)
        
        self.area.setWidgetResizable(True)
        self.area.adjustSize()
               
        self.setCentralWidget(self.area)
 
        self.resize(500, 400)
        self.show()

    def __init_img(self):
        if self.imgPath:
            self.__open_file(self.imgPath)
        else:
            self.pixmap = QPixmap('')
            self.imageLabel.setPixmap(self.pixmap)

    def set_menus(self):
        #FILE MENU
        openAct = QAction('&Open...', self)        
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open an image file')
        openAct.triggered.connect(lambda: self.__open_file())

        saveAct = QAction(QIcon('./icons/save-file.png'), '&Save', self)        
        saveAct.setShortcut('Ctrl+S')
        saveAct.setStatusTip('Save the open file')
        saveAct.triggered.connect(self.__save_file)

        saveAsAct = QAction('&Save as...', self)        
        saveAsAct.setShortcut('Ctrl+Shift+S')
        saveAsAct.setStatusTip('Save the open file as...')
        saveAsAct.triggered.connect(self.__save_as_file)

        delAct = QAction(QIcon('./icons/delete.png'), '&Delete image', self)        
        delAct.setShortcut('Del')
        delAct.setStatusTip('Permanently deletes the image file')
        delAct.triggered.connect(self.__del)
        
        exitAct = QAction('&Exit', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.closeEvent)

        #EDIT MENU
        rotLeftAct = QAction(QIcon('./icons/rotate-left.png'), 'Rotate left', self)        
        rotLeftAct.setShortcut('Ctrl+Shift++')
        rotLeftAct.setStatusTip('Rotates left for 90 degrees')
        rotLeftAct.triggered.connect(lambda: self.__rotate_img(-90))
        
        rotRightAct = QAction(QIcon('./icons/rotate-right.png'), 'Rotate right', self)        
        rotRightAct.setShortcut('Ctrl+Shift+-')
        rotRightAct.setStatusTip('Rotates right for 90 degrees')
        rotRightAct.triggered.connect(lambda: self.__rotate_img(90))
        
        zoomInAct = QAction(QIcon('./icons/zoom-in.png'), 'Zoom in', self)        
        zoomInAct.setShortcut('Ctrl++')
        zoomInAct.setStatusTip('Increase the image permanently with quality loss')
        zoomInAct.triggered.connect(lambda: self.__resize(0.1))

        zoomOutAct = QAction(QIcon('./icons/zoom-out.png'), 'Zoom out', self)        
        zoomOutAct.setShortcut('Ctrl+-')
        zoomOutAct.setStatusTip('Decrease the image permanently with quality loss')
        zoomOutAct.triggered.connect(lambda: self.__resize(-0.1))

        flipHorAct = QAction(QIcon('./icons/flip-hor.png'), 'Flip horizontally', self)        
        flipHorAct.setStatusTip('Flips the image horizontally')
        flipHorAct.triggered.connect(lambda: self.__flip_img('h'))

        flipVertAct = QAction(QIcon('./icons/flip-vert.png'), 'Flip vertically', self)        
        flipVertAct.setStatusTip('Flips the image vertically')
        flipVertAct.triggered.connect(lambda: self.__flip_img('v'))

        self.statusBar()
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        editMenu = menubar.addMenu('&Edit')
        
        fileMenu.addAction(openAct)
        fileMenu.addAction(saveAct)
        fileMenu.addAction(saveAsAct)
        fileMenu.addAction(delAct)
        fileMenu.addAction(exitAct)

        editMenu.addAction(rotLeftAct)
        editMenu.addAction(rotRightAct)
        editMenu.addAction(zoomInAct)
        editMenu.addAction(zoomOutAct)
        editMenu.addAction(flipHorAct)
        editMenu.addAction(flipVertAct)

        #adding toolbar
        toolbar = self.addToolBar('Edit image')
        toolbar.addAction(rotLeftAct)
        toolbar.addAction(rotRightAct)
        toolbar.addAction(flipHorAct)
        toolbar.addAction(flipVertAct)
        toolbar.addAction(zoomInAct)
        toolbar.addAction(zoomOutAct)
        toolbarFile = self.addToolBar('File')
        toolbarFile.addAction(saveAct)
        toolbarFile.addAction(delAct)
    

    def __open_file(self, *fileName):
        if not fileName:
            a = QFileDialog.getOpenFileName(self, 'Open file', self.defaultPath)
            if a:
                self.imgPath = a[0]
        else:
            self.imgPath = fileName[0]
        try:
            self.curImage = MyImage(self.imgPath, self.tempPath)
            self.pixmap = QPixmap(self.curImage.tempName)
            self.imageLabel.setPixmap(self.pixmap)
        except ValueError:
            QMessageBox.error(self, "Warning", "Cannot load %s." % a[0])
        
    def __save_file(self):
        if self.curImage:
            self.curImage.save(self.imgPath)

    def __save_as_file(self):
        if self.curImage:
            a = QFileDialog.getSaveFileName(self, 'Save file as', self.defaultPath)
            if a:
                self.imgPath = a[0]
                self.curImage.save(self.imgPath)
            

    def __rotate_img(self, degrees):
        self.curImage.rotate(degrees)
        self.update()

    def __flip_img(self, mode):
        self.curImage.flip(mode)
        self.update()
        

    def __resize(self, ratio):
        self.curImage.resize(ratio)
        self.update()

    def __del(self):
        a = QMessageBox.warning(self, "Warning", "Do you really want to delete this file?",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if a == QMessageBox.Yes:
            self.curImage.delete()
            self.pixmap = QPixmap('')
            self.imageLabel.setPixmap(self.pixmap)

    def update(self):
        self.pixmap = QPixmap(self.curImage.tempName)
        self.imageLabel.setPixmap(self.pixmap)


    def closeEvent(self, event):
        try:
            self.curImage.close()
            self.pixmap = QPixmap('')
            self.imageLabel.setPixmap(self.pixmap)
            event.accept()
        except AttributeError:
            event.accept()
    
def main():
    app = QApplication(sys.argv)
    if len(sys.argv) == 2:
        mainWindow = SimpleImageViewer(sys.argv[1])
    else:
        mainWindow = SimpleImageViewer()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
