# GitHub project: https://github.com/danielcmcg

import numpy as np
import cv2
import imutils

image_main = np.empty
image_test = np.empty
contours = []
hierarchy = []

def _loadImageTest(path):
	global image_test
	image_test = cv2.imread(path)
	return image_test
	
def _loadimage(path):
	global image_main
	image = cv2.imread(path)
	
	image = cv2.resize(image,(800,600))
	
	image = image.copy()
	
	row, col = image.shape[:2]
	bottom = image[row-2:row, 0:col]
	mean = cv2.mean(bottom)[0]
	bordersize = 10
	image=cv2.copyMakeBorder(image, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=[255,255,255] )
	
	image_main = image.copy()
	
	return image

def _greyImage(image):
	image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	return image
	
def _erodeImage(image):
	kernel = np.ones((2,2),np.uint8)
	image = cv2.erode(image,kernel,iterations = 1)
	return image
		
def _binaryImage(image):
	ret, image = cv2.threshold(image,127,255,200)
	image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,1.2)
	#ret,imgray = cv2.threshold(imgray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	return image

def _getContourHierarchy(image):
	global contours
	global hierarchy
	contours, hierarchy =  cv2.findContours(image,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

def _calcHist(image):
	hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
			[0, 256, 0, 256, 0, 256])
	hist = cv2.normalize(hist, hist).flatten()
	return hist

def _findWorms(image, minArea, maxArea):

	hist = _calcHist(image_test)
	
	i = 0
	j = 0
	
	global hierarchy
	global contours
	
	for c in contours:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.015 * peri, True)
		
		M = cv2.moments(c)
		if M['m00'] != 0:
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
		
		area = cv2.contourArea(c)
		
		if area > minArea and area < maxArea and hierarchy[0,i,3] != -1:
		
			x,y,w,h = cv2.boundingRect(c)
			roi = image_main[x:w, y:h]

			hist2 = _calcHist(roi)
			
			d = cv2.compareHist(hist, hist2, cv2.HISTCMP_CORREL)
			
			def _contourImage(j, contour, image):
				color = int(hierarchy[0,j,3])
				cv2.drawContours(image,[contour],-1,(255,color*10,0), 3)
				cv2.putText(image, str(j), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
				return image
				
			if d > 0.9:
				# draw the contour and center of the shape on the image
				image = _contourImage(j, c, image)
				j += 1
		
		i += 1
		
	line1 = 'min area: ' + str(minArea)
	line2 = 'max area: ' + str(maxArea)
	line3 = 'count: ' + str(j)

	cv2.putText(image, line1, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (25, 255, 255), 2)
	cv2.putText(image, line2, (15, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (25, 255, 255), 2)
	cv2.putText(image, line3, (15, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (25, 255, 255), 2)

	return image