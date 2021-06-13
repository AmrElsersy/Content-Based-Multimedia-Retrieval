import os

from PyQt5 import QtWidgets, QtCore, QtGui
import sys

sys.path.insert(0, '../../Content-Based-Multimedia-Retrieval')
sys.path.insert(1, '../core')

import cv2
from datetime import datetime, timedelta
from PyQt5.QtCore import QDir, Qt, QUrl
from cbir import CBIR
from cbvr import CBVR

from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QMessageBox,QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from master import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):


    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Multimedia Library")
        self.ui.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.ui.play_btn.clicked.connect(self.play)
        self.ui.horizontalSlider.sliderMoved.connect(self.setPosition)
        self.ui.horizontalSlider_2.sliderMoved.connect(self.setPosition_upload)
        self.ui.horizontalSlider_3.sliderMoved.connect(self.setPosition_show)
        self.mediaPlayerSearch = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayerShow = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayerSearch.setVideoOutput(self.ui.video_widget)
        self.mediaPlayerSearch.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayerSearch.positionChanged.connect(self.positionChanged)
        self.mediaPlayerSearch.durationChanged.connect(self.durationChanged)
        self.mediaPlayerSearch.error.connect(self.handleError)
        self.ui.play_btn_2.clicked.connect(self.play_upload)
        self.mediaPlayerUpload = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayerUpload.setVideoOutput(self.ui.video_widget_2)
        self.mediaPlayerUpload.stateChanged.connect(self.mediaStateChanged_upload)
        self.mediaPlayerUpload.positionChanged.connect(self.positionChanged_upload)
        self.mediaPlayerUpload.durationChanged.connect(self.durationChanged_upload)
        self.mediaPlayerUpload.error.connect(self.handleError_upload)
        #show video
        self.ui.play_btn_3.clicked.connect(self.play_show)
        self.mediaPlayerShow = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayerShow.setVideoOutput(self.ui.video_widget_3)
        self.mediaPlayerShow.stateChanged.connect(self.mediaStateChanged_show)
        self.mediaPlayerShow.positionChanged.connect(self.positionChanged_show)
        self.mediaPlayerShow.durationChanged.connect(self.durationChanged_show)
        self.cbir = CBIR()
        self.cbvr = CBVR()
        self.main()


    def main(self):
        self.ui.pushButton.clicked.connect(self.img_browse)
        self.ui.pushButton_2.clicked.connect(self.video_browse)
        self.ui.pushButton_6.clicked.connect(self.video_browse_upload)
        self.ui.pushButton_9.clicked.connect(self.upload_video)
        self.ui.pushButton_10.clicked.connect(self.cancel_video)
        self.ui.pushButton_3.clicked.connect(self.img_upload)
        self.ui.pushButton_7.clicked.connect(self.upload_image)
        self.ui.pushButton_8.clicked.connect(self.cancel_image)
        self.ui.pushButton_videoSearchP.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(3))
        self.ui.pushButton_imageSearchP.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.pushButton_imageUploadP.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        self.ui.pushButton_videoUploadP.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(2))
        self.ui.pushButton_imageHistogramSearch.clicked.connect(self.image_histo_search)
        self.ui.pushButton_imageHistogramSearch_2.clicked.connect(self.video_histo_search)
        self.ui.pushButton_.clicked.connect(self.image_mean_search)
        self.ui.pushButton_4.clicked.connect(self.image_dominant_search)

    def img_browse(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Image", QDir.homePath())

        if file_name.endswith('.png') or file_name.endswith('.jpg') or file_name.endswith('.jpeg'):
            self.ui.lineEdit.setText(file_name)
        else:
            self.ui.lineEdit.clear()
            reply = QMessageBox.about(None, "Error", "Invalid Image File Format")
        pixaya = QtGui.QPixmap(self.ui.lineEdit.text())
        self.ui.label__showImage.setPixmap(pixaya)

    def img_upload(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Image", QDir.homePath())

        if file_name.endswith('.png') or file_name.endswith('.jpg'):
            self.ui.lineEdit_3.setText(file_name)
        else:
            self.ui.lineEdit_3.clear()
            reply = QMessageBox.about(None, "Error", "Invalid Image File Format")
        pixaya = QtGui.QPixmap(self.ui.lineEdit_3.text())
        self.ui.label__showImage_3.setPixmap(pixaya)

    def video_browse(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open video",
                QDir.homePath())
        if file_name != '':
            self.mediaPlayerSearch.setMedia(
                    QMediaContent(QUrl.fromLocalFile(file_name)))
            self.ui.lineEdit_2.setText(file_name)
            self.ui.play_btn.setEnabled(True)
            end_time = datetime.now() + timedelta(seconds=1)
            while datetime.now() < end_time:
                self.mediaPlayerSearch.play()
            self.mediaPlayerSearch.pause()


    def play(self):
        if self.mediaPlayerSearch.state() == QMediaPlayer.PlayingState:
            self.mediaPlayerSearch.pause()
        else:
            self.mediaPlayerSearch.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayerSearch.state() == QMediaPlayer.PlayingState:
            self.ui.play_btn.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.ui.play_btn.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.ui.horizontalSlider.setValue(position)

    def durationChanged(self, duration):
        self.ui.horizontalSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayerSearch.setPosition(position)

    def handleError(self):
        self.ui.play_btn.setEnabled(False)
        self.ui.errorLabel.setText("Error: " + self.mediaPlayer.errorString())
# upload page
    def video_browse_upload(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open video",
                QDir.homePath())
        if file_name != '':
            self.mediaPlayerUpload.setMedia(
                    QMediaContent(QUrl.fromLocalFile(file_name)))
            self.ui.lineEdit_4.setText(file_name)
            self.ui.play_btn_2.setEnabled(True)
            end_time = datetime.now() + timedelta(seconds=1)
            while datetime.now() < end_time:
                self.mediaPlayerUpload.play()
            self.mediaPlayerUpload.pause()


    def play_upload(self):
        if self.mediaPlayerUpload.state() == QMediaPlayer.PlayingState:
            self.mediaPlayerUpload.pause()
        else:
            self.mediaPlayerUpload.play()

    def mediaStateChanged_upload(self, state):
        if self.mediaPlayerUpload.state() == QMediaPlayer.PlayingState:
            self.ui.play_btn_2.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.ui.play_btn_2.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged_upload(self, position):
        self.ui.horizontalSlider_2.setValue(position)

    def durationChanged_upload(self, duration):
        self.ui.horizontalSlider_2.setRange(0, duration)

    def setPosition_upload(self, position):
        self.mediaPlayerUpload.setPosition(position)

    def handleError_upload(self):
        self.ui.play_btn_2.setEnabled(False)
        self.ui.errorLabel_2.setText("Error: " + self.mediaPlayer.errorString())

    def upload_video(self):
        video_url = self.ui.lineEdit_4.text()
        self.cbvr.insert(video_url)

    def cancel_video(self):
        self.ui.lineEdit_4.setText("")
        self.mediaPlayerUpload.setMedia(QMediaContent())

    def upload_image(self):
        image_url = self.ui.lineEdit_3.text()
        self.cbir.insert(image_url)
        print("done")

    def cancel_image(self):
        self.ui.lineEdit_3.setText("")
        self.ui.label__showImage_3.clear()

    def image_histo_search(self):
        image_path = self.ui.lineEdit.text()
        image = cv2.imread(image_path)
        print(image)
        images_dict = self.cbir.search( "histogram", image, "mean_abs_match")
        print('hnaa')
        self.ui.widget = QtWidgets.QWidget()
        self.ui.layout = QtWidgets.QVBoxLayout()
        for i in images_dict.keys():
            abs_path = "C:/Users/esmaa/Desktop/Multimedia/Content-Based-Multimedia-Retrieval/core/"
            path = abs_path + i
            print(path)
            pixaya = QtGui.QPixmap(path)
            self.ui.new_label = QtWidgets.QLabel()
            self.ui.new_label.setPixmap(pixaya)
            self.ui.new_label.setScaledContents(True)
            self.ui.new_label.setMaximumSize(400, 200)
            self.ui.verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.ui.layout.addSpacerItem(self.ui.verticalSpacer)
            self.ui.layout.addWidget(self.ui.new_label)
        self.ui.widget.setLayout(self.ui.layout)
        print("tmm")
        self.ui.scrollArea.setWidget(self.ui.widget)

    def image_mean_search(self):
        image_path = self.ui.lineEdit.text()
        image = cv2.imread(image_path)
        print(image)
        images_dict = self.cbir.search( "mean_color", image, "mean_abs_match")
        self.ui.widget = QtWidgets.QWidget()
        self.ui.layout = QtWidgets.QVBoxLayout()
        for i in images_dict.keys():
            abs_path = "C:/Users/esmaa/Desktop/Multimedia/Content-Based-Multimedia-Retrieval/core/"
            path = abs_path + i
            print(path)
            pixaya = QtGui.QPixmap(path)
            self.ui.new_label = QtWidgets.QLabel()
            self.ui.new_label.setPixmap(pixaya)
            self.ui.new_label.setScaledContents(True)
            self.ui.new_label.setMaximumSize(400, 200)
            self.ui.verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.ui.layout.addSpacerItem(self.ui.verticalSpacer)
            self.ui.layout.addWidget(self.ui.new_label)
        self.ui.widget.setLayout(self.ui.layout)
        self.ui.scrollArea.setWidget(self.ui.widget)

    def image_dominant_search(self):
        image_path = self.ui.lineEdit.text()
        image = cv2.imread(image_path)
        print(image)
        images_dict = self.cbir.search( "dominant_color", image, "mean_abs_match")
        print('hnaa')
        self.ui.widget = QtWidgets.QWidget()
        self.ui.layout = QtWidgets.QVBoxLayout()
        for i in images_dict.keys():
            abs_path = "C:/Users/esmaa/Desktop/Multimedia/Content-Based-Multimedia-Retrieval/core/"
            path = abs_path + i
            print(path)
            pixaya = QtGui.QPixmap(path)
            self.ui.new_label = QtWidgets.QLabel()
            self.ui.new_label.setPixmap(pixaya)
            self.ui.new_label.setScaledContents(True)
            self.ui.new_label.setMaximumSize(400, 200)
            self.ui.verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.ui.layout.addSpacerItem(self.ui.verticalSpacer)
            self.ui.layout.addWidget(self.ui.new_label)
        self.ui.widget.setLayout(self.ui.layout)
        print("tmm")
        self.ui.scrollArea.setWidget(self.ui.widget)

    def video_histo_search(self):
        video_path = self.ui.lineEdit_2.text()
        video = cv2.VideoCapture(video_path)
        self.videos_paths = self.cbvr.search(video, video_path)
        self.ui.wid = QtWidgets.QWidget()
        self.ui.layout = QtWidgets.QVBoxLayout()
        self.group = QtWidgets.QButtonGroup()
        print(self.videos_paths)
        for i in range(len(self.videos_paths)):
            self.ui.hlay = QtWidgets.QHBoxLayout()
            self.ui.Button = QPushButton()
            self.ui.vid_label = QLabel()
            self.ui.vid_label.setText("Video " + str(i+1) + " : ")
            self.ui.hlay.addWidget(self.ui.vid_label)
            self.ui.hlay.addWidget(self.ui.Button)
            self.ui.Button.setText("Show Video")
            self.group.addButton(self.ui.Button, i)
            self.ui.layout.addLayout(self.ui.hlay)
            self.ui.Button.setStyleSheet("QPushButton""{""background-color : #b0b0b0;""color : #ffffff;"
                                          "font-size : 30px;""}"
                                          "QPushButton::hover""{""background-color : green;"
                                          "border: 2px inset green""}")
            self.ui.vid_label.setStyleSheet("QLabel""{""color : black;"
                                          "font-size : 30px;""}"
                                          "border: 2px inset green""}")
        self.ui.wid.setLayout(self.ui.layout)
        self.ui.scrollArea_2.setWidget(self.ui.wid)
        self.group.buttonClicked.connect(self.vid_play)

    def vid_play(self, object):
        self.ui.stackedWidget_2.setCurrentIndex(4)
        print(self.group.id(object))
        self.mediaPlayerShow.setMedia(
                    QMediaContent(QUrl.fromLocalFile(self.videos_paths[self.group.id(object)])))
        self.ui.play_btn_3.setEnabled(True)
        end_time = datetime.now() + timedelta(seconds=1)
        while datetime.now() < end_time:
            self.mediaPlayerShow.play()
        self.mediaPlayerShow.pause()

    def play_show(self):
        if self.mediaPlayerShow.state() == QMediaPlayer.PlayingState:
            self.mediaPlayerShow.pause()
        else:
            self.mediaPlayerShow.play()

    def mediaStateChanged_show(self, state):
        if self.mediaPlayerShow.state() == QMediaPlayer.PlayingState:
            self.ui.play_btn_3.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.ui.play_btn_3.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged_show(self, position):
        self.ui.horizontalSlider_3.setValue(position)

    def durationChanged_show(self, duration):
        self.ui.horizontalSlider_3.setRange(0, duration)

    def setPosition_show(self, position):
        self.mediaPlayerUpload.setPosition(position)