# Standard imports
import cv2, time
import numpy as np
from ws4py.client.threadedclient import WebSocketClient

class DummyClient(WebSocketClient):
    def opened(self):
        mac = raw_input("Enter cameras address (enter nothing for cc0000000001): ")
        if mac == "":
            mac = "cc000000000001"
        
        self.send("camera-" + mac)
        x, y = 0, 0

        params = cv2.SimpleBlobDetector_Params()
        params.blobColor = 255
        params.minArea = 5
        detector = cv2.SimpleBlobDetector_create(params)

        cap = cv2.VideoCapture(2)
        cap.set(3, 640)
        cap.set(4, 480)
        cap.set(5, 60)

        while True:
            ret, im = cap.read()
            keypoints = detector.detect(im)
            im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            
            cv2.imshow("Keypoints", im_with_keypoints)

            if len(keypoints) == 1:
                point = keypoints[0]
                x, y = point.pt[0], point.pt[1]
                self.send(mac + "x"+str(int(x))+"y"+str(int(y))+"h5w5a0")

                print(int(x),int(y))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


    def closed(self, code, reason=None):
        cap.release()
        cv2.destroyAllWindows()
        print "Closed down", code, reason

    def received_message(self, m):
        print(m)
 

if __name__ == '__main__':
    try:
        print("camera client")
        ws = DummyClient('ws://192.168.1.2:8001/', protocols=['http-only', 'chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()

