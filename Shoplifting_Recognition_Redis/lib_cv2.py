import cv2
import json
import base64
import numpy as np


def get_missing_points(x1, y1, x2, y2):
	return x2, y1, x1, y2

def area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) +
                x2 * (y3 - y1) +
                x3 * (y1 - y2)) / 2.0)

def is_contained_in_roi(x, y, roi: dict) -> bool:
    # points are clockwise starting at top right (x1, y1)
    x4, y4, x2, y2 = roi['x1'], roi['y1'], roi['x2'], roi['y2']
    x1, y1, x3, y3 = get_missing_points(x4, y4, x2, y2)

    R = (area(x1, y1, x2, y2, x3, y3) +
         area(x1, y1, x4, y4, x3, y3))

    T1 = area(x, y, x1, y1, x2, y2)
    T2 = area(x, y, x2, y2, x3, y3)
    T3 = area(x, y, x3, y3, x4, y4)
    T4 = area(x, y, x1, y1, x4, y4)

    return (R==T1+T2+T3+T4)

def get_absolute_roi_dict(roi: dict, imgx, imgy) -> dict:
	abs_roi = {}
	abs_roi['x1'], abs_roi['y1'] = get_absolute_coordinates(roi['x1'], roi['y1'], imgx, imgy)
	abs_roi['x2'], abs_roi['y2'] = get_absolute_coordinates(roi['x2'], roi['y2'], imgx, imgy)
	return abs_roi

def get_absolute_coordinates(x, y, imgx, imgy):
	return int(float(x)*float(imgx)), int(float(y)*float(imgy))




def convertBack(x, y, w, h):
	xmin=int(x)
	xmax=int(x+w)
	ymin=int(y)
	ymax=int(y+h)
	return xmin, ymin, xmax, ymax

	#xmin = int(round(x - (w / 2)))
	#xmax = int(round(x + (w / 2)))
	#ymin = int(round(y - (h / 2)))
	#ymax = int(round(y + (h / 2)))
	#eturn xmin, ymin, xmax, ymax

def converBackYolo(x,y,w,h):
	xmin = int(round(x - (w / 2)))
	xmax = int(round(x + (w / 2)))
	ymin = int(round(y - (h / 2)))
	ymax = int(round(y + (h / 2)))
	return xmin, ymin, xmax, ymax

def cvDrawBoxes(image,coords,notify):
	decode=base64.b64decode(image.encode())
	img=cv2.imdecode(np.fromstring(decode, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
	for name in notify:
		for coord in coords[name]:
			x, y, w, h = coord[0],coord[1],coord[2],coord[3]
			xmin, ymin, xmax, ymax = convertBack(float(x), float(y), float(w), float(h))
			pt1 = (xmin, ymin)
			pt2 = (xmax, ymax)
			cv2.rectangle(img, pt1, pt2, (0, 255, 0), 1)
			cv2.putText(img,name,
					(pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
					[0, 255, 0], 2)
	jpg=cv2.imencode('.jpg',img)[1].tobytes()
	img=base64.b64encode(jpg).decode()
	return img

def addtext(image,coords,text):
	decode=base64.b64decode(image.encode())
	img=cv2.imdecode(np.fromstring(decode, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
	pt1=(coords[0],coords[1])
	cv2.putText(img,text,
			(pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
			[0, 255, 0], 2)
	jpg=cv2.imencode('.jpg',img)[1].tobytes()
	img=base64.b64encode(jpg).decode()
	return img

def cvDrawBoxes(image,coords,notify):
	decode=base64.b64decode(image.encode())
	img=cv2.imdecode(np.fromstring(decode, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
	for name in notify:
		for coord in coords[name]:
			x, y, w, h = coord[0],coord[1],coord[2],coord[3]
			xmin, ymin, xmax, ymax = convertBack(float(x), float(y), float(w), float(h))
			pt1 = (xmin, ymin)
			pt2 = (xmax, ymax)
			cv2.rectangle(img, pt1, pt2, (0, 255, 0), 1)
			cv2.putText(img,name,
					(pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
					[0, 255, 0], 2)
	jpg=cv2.imencode('.jpg',img)[1].tobytes()
	img=base64.b64encode(jpg).decode()
	return img

def DrawBox2(img, boxes, colors):
	
	try:
		for box,  cl in zip(boxes, colors):
			c1, c2 = (box[0], box[1]), (box[2], box[3])
			if  cl =='red':
				img2 = cv2.rectangle(img,c1,c2,(0,0,255),3)
				img2= cv2.putText(img2, 'No Mask',(box[0],box[1]-7),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
			elif cl=='green':
				img2 = cv2.rectangle(img,c1,c2,(0,255,0),3)
				img2 =cv2.putText(img2, 'Masking',(box[0],box[1]-7),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
		#convert to json 64bit
		jpg=cv2.imencode('.jpg',img2)[1].tobytes()
		img2=base64.b64encode(jpg).decode()        
		return img2
	except:
		jpg=cv2.imencode('.jpg',img)[1].tobytes()
		img=base64.b64encode(jpg).decode()
		return img

def cvDrawBoxline(image,name,left,top,right,bottom,x1,y1,x2,y2):
	decode=base64.b64decode(image.encode())
	img=cv2.imdecode(np.fromstring(decode, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
	pt1 = (int(left), int(top))
	pt2 = (int(right), int(bottom))
	cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)
	cv2.putText(img,name,
					(pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
					[0, 255, 0], 2)
	pt1 = (int(x1),int(y1))
	pt2 = (int(x2), int(y2))
	cv2.line(img, pt1, pt2, (255, 0, 0), 3)
	jpg=cv2.imencode('.jpg',img)[1].tobytes()
	img=base64.b64encode(jpg).decode()
	return img



#######################################################
