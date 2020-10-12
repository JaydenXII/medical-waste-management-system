import qrcode
from PIL import Image
import cv2 as cv
from hyperlpr import *

ALLOWED_EXTENSIONS = set(["png", "jpg", "heic"])
ALLOWED_TYPE = set(["A", "B", "C"])

def allowed_file(filename):
	return "." in filename and filename.split(".")[-1] in ALLOWED_EXTENSIONS

def QrGen(InputText, TargetPath):
	QrCode=qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_H,
		box_size=10,
		border=4,)
	QrCode.add_data(InputText)
	QrCodeImg=QrCode.make_image(fill_color="black", back_color="white").convert('RGB')
	QrCodeImg.save(TargetPath)
	#return QrCode

def QrDec(SourcePath):
	QrCodeImg=cv.imread(SourcePath)
	Detector = cv.QRCodeDetector()
	ReturnVal, _, _= Detector.detectAndDecode(QrCodeImg)
	return ReturnVal

def PlateDetection(SourcePath):
	PlateImage=cv.imread(SourcePath)
	PlateNumber=HyperLPR_plate_recognition(PlateImage)[0][0]
	print(PlateNumber)
	return PlateNumber

"""
if this function give you alot useless info, comment all the print in hyperlpr.py
they are useless and harmless, but i found them annoying
"""

"""
estimateAffinePartial2D返回一个元组然后第0位对应的原来estimateRigidTransform的返回值
line 231应该改成
mat_ = cv2.estimateAffinePartial2D(org_pts, target_pts, True)[0]
或者
pip install opencv-python==3.4.9.31
"""
