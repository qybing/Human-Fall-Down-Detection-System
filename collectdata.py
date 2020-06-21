import numpy as np
import cv2
import math
 
cap = cv2.VideoCapture('allfall.mp4')

fgbg = cv2.createBackgroundSubtractorMOG2(history=500)
kernele = np.ones((15,15),np.uint8)
kerneld = np.ones((21,21),np.uint8)
count = 0
frlist = []
eclist = []
ellist = []
relist = []
pelist = []
colist = []
orlist = []
while(1):
    Eccentricity = None
    Elongatedness = None
    Rectangularity = None
    perimeter = None
    Compactness = None
    angle = None


    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)
    
    fgmask = cv2.erode(fgmask,kernele,iterations = 1)
    fgmask = cv2.dilate(fgmask,kerneld,iterations = 1)


    ret, fgmask = cv2.threshold(fgmask, 240, 255, cv2.THRESH_BINARY)
    image, contours, hier = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) > 0:
        cnt = contours[0]
        for i in range(len(contours)):
            if len(contours[i])>len(cnt):
                cnt = contours[i]
        
        x,y,w,h = cv2.boundingRect(cnt)
        if(50<w<400 and 50<h<400):
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)

            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            area = cv2.contourArea(cnt)
            arearect = cv2.contourArea(box)
            if len(cnt) > 5:
                (x,y),(MA,ma),angle = cv2.fitEllipse(cnt)
                Eccentricity = math.sqrt((ma**2 - MA**2)/ma**2)
                perimeter = cv2.arcLength(cnt,True)
                Compactness = perimeter**2 / (4*math.pi*area)
                Elongatedness = float(h)/float(w)
                Rectangularity = float(area)/float(arearect)


                print ("========================")
                print ("Frame:          " + str(count))
                print ("Eccentricity:   " + str(Eccentricity))
                print ("Elongatedness:  " + str(Elongatedness))
                print ("Rectangularity: " + str(Rectangularity))
                print ("Perimeter:      " + str(perimeter))
                print ("Compactness:    " + str(Compactness))
                print ("Orientation:    " + str(abs(angle-90)))
                print ("========================")

                frlist.append(count)
                eclist.append(Eccentricity)
                ellist.append(Elongatedness)
                relist.append(Rectangularity)
                pelist.append(perimeter)
                colist.append(Compactness)
                orlist.append(abs(angle-90))



    if count == 100:
        record = fgmask
        break
    cv2.imshow('frame',frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break 
    count = count + 1

xlist = []
ylist = []
for i in range(len(eclist)):
    temp = []
    #temp.append(frlist[i])
    temp.append(eclist[i])
    temp.append(ellist[i])
    temp.append(relist[i])
    #temp.append(pelist[i])
    #temp.append(colist[i])
    temp.append(orlist[i])
    xlist.append(temp)
    if 50 < i < 145:
        ylist.append(1)
    else:
        ylist.append(0)

print xlist
print ylist
print frlist

cv2.imshow('record',record)
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()