import cv2 
from flask import Flask, render_template, Response, request
import flask

app = Flask(__name__)



@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/video', methods = ['GET','POST'])
def index():
    """Video streaming home page."""
    return render_template('index.html')

"""def cam():
    with app.test_request_context('/form', method = 'POST'):
        if request.method == 'GET':
            return f"The URL /data is accessed directly. Try going to '/form' to submit form"
        if request.method == 'POST':
            form_data = request.form
            a = int(form_data['Name'])
            return a"""

def gen(v):

    """global a
    with app.test_request_context('/form', method = 'POST'):
        if request.method == 'POST':
            form_data = request.form
            a = int(form_data['Name'])
            print(a)"""
        #print(type(form_data['Name']))
        
    #with app.test_request_context('/video', method = 'POST'):
       # v = request.form['Name']
        #print(v)

    """Video streaming generator function."""
    cap = cv2.VideoCapture(v) #With WebCam!! 
    #cap = cv2.VideoCapture('rtsp://admin:admin@192.168.1.201:554/') 
    #exemple for using IPcamera: cv2.VideoCapture('rtsp://username:password@192.xxx.xxx.xx:554/1')


    


    # Read until video is completed
    while(cap.isOpened()):
      # Capture frame-by-frame
        ret, img = cap.read()
        if ret == True:
        #    img = cv2.flip(img,1)
            #img = detect_face(img)            
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            #time.sleep(0.1)
        else: 
            break

@app.route('/video_feed')
def video_feed():
    v = request.form['Name']
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(v),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host="0.0.0.0")