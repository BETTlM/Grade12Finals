########################################################################
#                                                                      #
#                   COMPUTER SCIENCE PROJECT  2023 -24                 #
#                                                                      #
#                                                                      #
#                          DYNAMIC TICKET EXPERT                       #
#                                                                      #
#                                                                      #
########################################################################




##Main python program running in background to detect people

#from picamera.array import PiRGBArray

#from picamera import PiCamera


##Both the modules above are used to run the program using live video input

##For demo purposes, the program uses a pre-recorded video



import numpy as np
import cv2 as cv

##Both the above two modules are AI modules used to detect people which is pre-trained

import Person

##Person is a custom module made specifically for this program
##This module is used to enumerate and uniquely identify people in the frame


import time

try:
    log = open('log.txt',"w")
except:
    print( "Cannot open log file")

##Local text file is used to store the logs of the backend program which
##can be accessed to debug the program during implications



##Counter objects for counting number of people entering and leaving the specified area


cnt_up   = 0
cnt_down = 0

##Source of video



cap = cv.VideoCapture(r'D:\Comp Sci\CS Project\f847bf18-b824-4037-bdff-3e00e5a4d14c.mp4')


##Use the code below in order to switch to live tracking


#camera = PiCamera()
##camera.resolution = (160,120)
##camera.framerate = 5
##rawCapture = PiRGBArray(camera, size=(160,120))
##time.sleep(0.1)

#Properties of video window
##cap.set(3,160) #Width
##cap.set(4,120) #Height

#Printing properties of frame to console

for i in range(19):
    print( i, cap.get(i))

h = 480
w = 640
frameArea = h*w
areaTH = frameArea/250
print( 'Area Threshold', areaTH)

##Input Output lines



line_up = int(2*(h/5))
line_down   = int(3*(h/5))


up_limit =   int(1*(h/5))
down_limit = int(4*(h/5))


print( "Red line y:",str(line_down))
print( "Blue line y:", str(line_up))


line_down_color = (255,0,0)
line_up_color = (0,0,255)


pt1 =  [0, line_down];
pt2 =  [w, line_down];


pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-1,1,2))


pt3 =  [0, line_up];
pt4 =  [w, line_up];


pts_L2 = np.array([pt3,pt4], np.int32)
pts_L2 = pts_L2.reshape((-1,1,2))


pt5 =  [0, up_limit];
pt6 =  [w, up_limit];


pts_L3 = np.array([pt5,pt6], np.int32)
pts_L3 = pts_L3.reshape((-1,1,2))


pt7 =  [0, down_limit];
pt8 =  [w, down_limit];


pts_L4 = np.array([pt7,pt8], np.int32)
pts_L4 = pts_L4.reshape((-1,1,2))



##Background Subtractor

fgbg = cv.createBackgroundSubtractorMOG2(detectShadows = True)


##Structuring elements for morphological filters

kernelOp = np.ones((3,3),np.uint8)
kernelOp2 = np.ones((5,5),np.uint8)
kernelCl = np.ones((11,11),np.uint8)


#Variables
font = cv.FONT_HERSHEY_SIMPLEX
persons = []
max_p_age = 5
pid = 1












while(cap.isOpened()):
##for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #Read an image from the video source
    
    ret, frame = cap.read()
##    frame = image.array

    for i in persons:
        i.age_one() #age every person one frame
    #########################
    #   PRE-PROCESSING      #
    #########################
    
    #Appliying background subtraction

    
    fgmask = fgbg.apply(frame)
    fgmask2 = fgbg.apply(frame)

    #Binaracion to eliminate shadows (gray color)
    try:
        
        ret,imBin= cv.threshold(fgmask,200,255,cv.THRESH_BINARY)
        ret,imBin2 = cv.threshold(fgmask2,200,255,cv.THRESH_BINARY)
        
        
        #Opening (erode->dilate) to remove noise
        mask = cv.morphologyEx(imBin, cv.MORPH_OPEN, kernelOp)
        mask2 = cv.morphologyEx(imBin2, cv.MORPH_OPEN, kernelOp)
        
        
        #Closing (dilate -> erode) to join white regions
        mask =  cv.morphologyEx(mask , cv.MORPH_CLOSE, kernelCl)
        mask2 = cv.morphologyEx(mask2, cv.MORPH_CLOSE, kernelCl)
    
    
    except:
        print('EndOfProgram')
        print( 'UP:',cnt_up)
        print ('DOWN:',cnt_down)
        break
    #################
    #   CONTOURS    #
    #################
    
    # RETR_EXTERNAL returns only extreme outer flags. All child contours are left behind.
    
    contours0, hierarchy = cv.findContours(mask2,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours0:
        area = cv.contourArea(cnt)
        
        
        if area > areaTH:
           
           
            #################
            #   TRACKING    #
            #################
            
            






##Need to add conditions for multi-person, screen exits and entrances.
            
  
  
            M = cv.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv.boundingRect(cnt)

            new = True
            if cy in range(up_limit,down_limit):
                for i in persons:
                    if abs(x-i.getX()) <= w and abs(y-i.getY()) <= h:
                        
                        #The object is close to one that was detected before
                        
                        new = False
                        i.updateCoords(cx,cy)   
                        
                        if i.going_UP(line_down,line_up) == True:
                            cnt_up += 1;
                        
                            print( "ID:",i.getId(),'crossed going up at',time.strftime("%c"))
                        
                            log.write("ID: "+str(i.getId())+' crossed going up at ' + time.strftime("%c") + '\n')
                        
                        elif i.going_DOWN(line_down,line_up) == True:
                        
                            cnt_down += 1;
                        
                            print( "ID:",i.getId(),'crossed going down at',time.strftime("%c"))
                            log.write("ID: " + str(i.getId()) + ' crossed going down at ' + time.strftime("%c") + '\n')
                        

                        #Linking this backend to another python instance using instantaneous writing
                        
                        temp_file = open('temp.txt','a+')
                        output_string = str(cnt_up)+' '+str(cnt_down)+'\n'
                        temp_file.write(output_string)
                        temp_file.close()



                        break
                    
                    if i.getState() == '1':
                    
                        if i.getDir() == 'down' and i.getY() > down_limit:
                    
                            i.setDone()
                    
                        elif i.getDir() == 'up' and i.getY() < up_limit:
                    
                            i.setDone()
                    
                    if i.timedOut():
                       
                        #remove i from the persons list
                        index = persons.index(i)
                        persons.pop(index)
                        del i     #free i memory
                
                
                
                
                ##If the object detected is NEW



                if new == True:
                    p = Person.MyPerson(pid,cx,cy, max_p_age)
                    persons.append(p)
                    pid += 1     
            #################
            #   DRAWINGS    #
            #################
            
            
            cv.circle(frame,(cx,cy), 5, (0,0,255), -1)
            
            img = cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            


    #END for cnt in contours0
            
    
    
    #########################
    #     DRAWING PATHS     #
    #########################
    
    
    
    for i in persons:
##        if len(i.getTracks()) >= 2:
##            pts = np.array(i.getTracks(), np.int32)
##            pts = pts.reshape((-1,1,2))
##            frame = cv.polylines(frame,[pts],False,i.getRGB())
##        if i.getId() == 9:
##            print str(i.getX()), ',', str(i.getY())
        cv.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv.LINE_AA)
        
    
    
    
    #################
    #     IMAGES    #
    #################



    str_up = 'UP: '+ str(cnt_up)
    str_down = 'DOWN: '+ str(cnt_down)
   
    frame = cv.polylines(frame,[pts_L1],False,line_down_color,thickness=2)
   
    frame = cv.polylines(frame,[pts_L2],False,line_up_color,thickness=2)
   
    frame = cv.polylines(frame,[pts_L3],False,(255,255,255),thickness=1)
   
    frame = cv.polylines(frame,[pts_L4],False,(255,255,255),thickness=1)
   
    cv.putText(frame, str_up ,(10,40),font,0.5,(255,255,255),2,cv.LINE_AA)
   
    cv.putText(frame, str_up ,(10,40),font,0.5,(0,0,255),1,cv.LINE_AA)
   
    cv.putText(frame, str_down ,(10,90),font,0.5,(255,255,255),2,cv.LINE_AA)
   
    cv.putText(frame, str_down ,(10,90),font,0.5,(255,0,0),1,cv.LINE_AA)




    cv.imshow('MAIN VIDEO PROCESSING',frame)
    cv.imshow('MORPHED FRAMES TO DETECT PEOPLE',mask)    
    

##    rawCapture.truncate(0)
    
    
    
    
    
    
    
    #PRESS ESC TO EXIT


    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
#END while(cap.isOpened())
    
#################
# CLEANING UP   #
#################
log.flush()
log.close()


cap.release()
cv.destroyAllWindows()


temp_file = open('temp.txt','a+')
temp_file.write('end')
temp_file.truncate(0)
temp_file.write('0 0\n')
temp_file.close()