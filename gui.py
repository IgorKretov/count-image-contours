# GitHub project: https://github.com/danielcmcg

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np
import cv2
import imutils

import countImage

image_main = np.empty
image_test = np.empty
contours = []
hierarchy = []

image_test = countImage._loadImageTest('test2.jpg')
image_path = 'test.jpg'
image_main = countImage._loadimage(image_path)


def runProcess(minArea, maxArea):
	global imCopy
	global image_main
	global image_path
	imCopy = np.empty
	image_main = countImage._loadimage(image_path)
	imCopy = countImage._greyImage(image_main)
	imCopy = countImage._erodeImage(imCopy)
	imCopy = countImage._binaryImage(imCopy)
	countImage._getContourHierarchy(imCopy)
	imCopy = countImage._findWorms(image_main,minArea, maxArea)	
	return imCopy
	
class App(QWidget):
	def __init__(self):
		super().__init__()
		self.title = 'PyQt5 button - pythonspot.com'
		self.left = 100
		self.top = 100
		self.width = 800
		self.height = 600
	      
		self.canMove = False
		self.object = []
		self.difX = 0
		self.difY = 0
	              
		self.initUI()
		self.setMouseTracking(True)
	              
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		layout = QGridLayout()
		layout.setSpacing(10)
		
		'''Load Image'''
		self.loadimagebutton = QPushButton('Find image', self)
		self.loadimagebutton.clicked.connect(self.setImagePath)
		
		'''Main image'''
		#initialize image from countimage
		imCopy = runProcess(1300, 9000)
		height, width, channel = imCopy.shape
		bytesPerLine = 3 * width
		qImg = QImage(imCopy.data, width, height, bytesPerLine, QImage.Format_RGB888)
		
		#load image to qt widget and show
		self.image = QLabel('image')
		self.pixmap = QPixmap(qImg)#'test2.jpg')
		self.image.setPixmap(self.pixmap)
		self.resize(400,600)
		self.image.installEventFilter(self)
		
		'''Slider min'''
		self.sliderMinLabel = QLabel('sliderMin: 1300')
		self.sliderMin = QSlider(Qt.Horizontal)
		self.sliderMin.setMinimum(0)
		self.sliderMin.setMaximum(20000)
		self.sliderMin.setValue(1300)
		self.sliderMin.setTickPosition(QSlider.TicksBelow)
		self.sliderMin.setTickInterval(1500)
		self.sliderMin.valueChanged.connect(self.valuechange)
		
		'''Slider max'''
		self.sliderMaxLabel = QLabel('sliderMax: 9000')
		self.sliderMax = QSlider(Qt.Horizontal)
		self.sliderMax.setMinimum(0)
		self.sliderMax.setMaximum(20000)
		self.sliderMax.setValue(9000)
		self.sliderMax.setTickPosition(QSlider.TicksBelow)
		self.sliderMax.setTickInterval(1500)
		self.sliderMax.valueChanged.connect(self.valuechange)
		
		'''Setting widgets on gird layout'''
		layout.addWidget(self.image,0,1,10,1)
		
		rightlayout = QGridLayout()
		rightlayout.setSpacing(10)
		layout.addLayout(rightlayout,0,0)
		
		rightlayout.addWidget(self.loadimagebutton,0,0,1,1)
		rightlayout.addWidget(self.sliderMinLabel,1,0,1,1)
		self.sliderMinLabel.setFixedHeight(20)
		rightlayout.addWidget(self.sliderMin,2,0,1,1)
		self.sliderMin.setFixedHeight(20)
		self.sliderMin.setFixedWidth(200)
		rightlayout.addWidget(self.sliderMaxLabel,3,0,1,1)
		self.sliderMaxLabel.setFixedHeight(20)
		rightlayout.addWidget(self.sliderMax,4,0,1,1)
		self.sliderMaxLabel.setFixedHeight(20)
		self.sliderMax.setFixedWidth(200)
		
		self.setLayout(layout) 
		self.show()
	              
	@pyqtSlot()
	
	def valuechange(self):
		global imCopy
		global image_main
		global image_path
		self.sliderMinLabel.setText('sliderMin: ' + str(self.sliderMin.value()))
		self.sliderMaxLabel.setText('sliderMax: ' + str(self.sliderMax.value()))
		_imCopy = np.empty
		_imCopy = runProcess(self.sliderMin.value(), self.sliderMax.value())
		height, width, channel = _imCopy.shape
		bytesPerLine = 3 * width
		qImg = QImage(_imCopy.data, width, height, bytesPerLine, QImage.Format_RGB888)
		self.pixmap = QPixmap(qImg)
		self.image.setPixmap(self.pixmap)
		self.image.installEventFilter(self)
		#print(self.sliderMin.value())
		
	def setImagePath(self):
		global imCopy
		global image_main
		global image_path
		imagePath, _ = QFileDialog.getOpenFileName()
		image_path = imagePath
		_imCopy = np.empty
		_imCopy = runProcess(self.sliderMin.value(), self.sliderMax.value())
		height, width, channel = _imCopy.shape
		bytesPerLine = 3 * width
		qImg = QImage(_imCopy.data, width, height, bytesPerLine, QImage.Format_RGB888)
		self.pixmap = QPixmap(qImg)
		self.image.setPixmap(self.pixmap)
		self.image.installEventFilter(self)
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_()) 