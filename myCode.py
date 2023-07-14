import cv2
import math

p1,p2=530,300
xpos=[]
ypos=[]
video=cv2.VideoCapture("footvolleyball.mp4")

tracker=cv2.TrackerCSRT_create()
success,img=video.read()

bbox=cv2.selectROI('obj',img,False)
tracker.init(img,bbox)
print(bbox)

def drawBox(frame,bbox):
    x,y,w,h=int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3,1)
    cv2.putText(frame,"Tracking",(75,90),cv2.FONT_HERSHEY_SCRIPT_COMPLEX,2,(0,0,255),5)

def goalTrack(frame,bbox):
    x,y,w,h=int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
    c1=x+int(w/2)
    c2=y+int(h/2)
    cv2.circle(frame,(c1,c2),2,(0,0,0),5)
    cv2.circle(frame,(p1,p2),2,(0,0,0),5)
    dist=math.sqrt(((c1-p1)**2)+((c2-p2)**2))
    if (dist<15):
        cv2.putText(frame,"GOAL",(300,90),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
    xpos.append(c1)
    ypos.append(c2)
    for i in range(len(xpos)-1):
        cv2.circle(frame,(xpos[i],ypos[i]),2,(0,0,0),5)


while True:
    ret,frame=video.read()

    success,bbox=tracker.update(frame)

    if success:
        drawBox(frame,bbox)
    else:
        cv2.putText(frame,"LOST",(75,90),cv2.FONT_HERSHEY_SCRIPT_COMPLEX,1,(0,0,255),2)

    goalTrack(frame,bbox)

    cv2.imshow("video",frame)
    if cv2.waitKey(1)==32:
        break


video.release()
cv2.destroyAllWindows()