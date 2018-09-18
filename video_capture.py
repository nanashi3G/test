import cv2
import time
import requests
import base64

URL = 'http://localhost/uwsgi/post_video'
FILE_NAME = 'out.jpg'
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

def main():
    capture = cv2.VideoCapture(0) 
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    while(True):
        ret, frame = capture.read()
        cv2.imwrite(FILE_NAME, frame)

        time.sleep(0.5)

        fd = open(FILE_NAME, 'rb')
        files = {'file': (FILE_NAME, fd, 'image/jpeg')}
        res = requests.post(URL, data=base64.b64encode(fd.read()))
        fd.close()

        cv2.imshow('', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()
    fd.close()

if __name__ == '__main__':
    main()

