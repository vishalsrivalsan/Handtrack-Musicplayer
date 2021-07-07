import cv2
import mediapipe as mp


class handTrack():
    def __init__(self, mode=False, maxHands = 2, detectConf=0.5, trackConf=0.5):
        self.mode=mode;
        self.maxHands=maxHands
        self.detectConf=detectConf
        self.trackConf=trackConf

        self.mp_hands=mp.solutions.hands
        self.hands = mp.solutions.hands.Hands(self.mode,self.maxHands,self.detectConf,self.trackConf)
        self.mp_draw =mp.solutions.drawing_utils


    def findHands(self,frame,draw=False):
        frame=frame
        rgbImg = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgbImg)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(frame, handLms, self.mp_hands.HAND_CONNECTIONS)
        return frame
    def findPosition(self, frame, handNo=0, draw=True):
        landmarkList=[]

        if self.results.multi_hand_landmarks:
            reqHand = self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(reqHand.landmark):
                
                h,w,c = frame.shape
                cx,cy = int(lm.x * w),int(lm.y * h)
                #print(cx, cy)
                landmarkList.append([id, cx, cy])
                if draw:
                    cv2.circle(frame, (cx,cy), 10,(255,0,255), cv2.FILLED)
        return landmarkList


def main():
    cap = cv2.VideoCapture(0)
    detector=handTrack()
    while True:
        success, frame = cap.read()
        if success:
            
            frame = detector.findHands(frame,True)
            landmarkList = detector.findPosition(frame)
            if len(landmarkList)!=0:
                print(landmarkList[4])
            cv2.imshow('frame', frame)

        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break
        

if __name__== "__main__":
    main()
