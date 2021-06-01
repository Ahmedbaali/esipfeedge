#import time
import cv2 
import urllib.request
import numpy as np
from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #Using HaarCascade for face detection


"""def detect_face(img):
    
  
    face_img = img.copy()
  
    face_rects = face_cascade.detectMultiScale(face_img) 
    
    for (x,y,w,h) in face_rects: 
        cv2.rectangle(face_img, (x,y), (x+w,y+h), (255,255,255), 10) 
        
    return face_img
"""

def gen():
    url = "http://192.168.137.4/cam-hi.jpg"
    """Video streaming generator function."""
   # cap = cv2.VideoCapture("http://192.168.137.4/cam-hi.jpg") #With WebCam!! 
    #cap = cv2.VideoCapture('rtsp://admin:admin@192.168.1.201:554/') 
    #exemple for using IPcamera: cv2.VideoCapture('rtsp://username:password@192.xxx.xxx.xx:554/1')

    # Read until video is completed
    while True:
      # Capture frame-by-frame
        imgResp=urllib.request.urlopen(url)
        imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
        img=cv2.imdecode(imgNp,-1)            
        img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            #time.sleep(0.1)
        #else: 
         #   break
        

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host="0.0.0.0")