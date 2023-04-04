import cv2 
from .module.object_module import three_d_object,augment
from . import content
import av
import mediapipe as mp
from .module import basicMethod as BM

mp_pose = mp.solutions.pose
pose=mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=0)

audio=0
audioFlag=False

class ARguide:
    def __init__(self,Activity):
        self.arrowC=three_d_object('data/3d_objects/arrowC.obj', 'data/3d_objects/texture.jpg',False)
        self.arrowS=three_d_object('data/3d_objects/arrowS.obj', 'data/3d_objects/texture.jpg',False)
        self.arrowUp=three_d_object('data/3d_objects/arrowUp.obj','data/3d_objects/texture.jpg',False)
        self.arrowDown=three_d_object('data/3d_objects/arrowDown.obj','data/3d_objects/texture.jpg',False)
        self.contents=content.content(Activity)

    def Run(self,image):
        global audio
        global audioFlag
        # 필요에 따라 성능 향상을 위해 이미지 작성을 불가능함으로 기본 설정합니다.
        image.flags.writeable = False
                    
        # # Get the width and height of the frame
        frame_height, frame_width, _ =  image.shape
    
        # # Resize the frame while keeping the aspect ratio.
        image = cv2.resize(image, (int(frame_width * (640 / frame_height)), 640))

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        size=image.shape
                    
        image, landmark_px = BM.detectPose(image, pose, display=False)
        #image=cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # 이미지 복원
        active,speech,AreaList=self.contents.run(landmark_px,size)
        """
        if isEnd:
            image=np.zeros((image.shape[0],image.shape[1]))
            image=image=cv2.putText(image,"수고하셨습니다",((image.shape[1]-50),(image.shape[0]-50)),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),1, cv2.LINE_AA)
            return image,speechText
        """
        
        if active:
            for element in AreaList:
                if element[4][0]==0:
                    image=augment(image,self.arrowC,element[0],element[1],element[2],element[3])
                elif element[4][0]==1:
                    image=augment(image,self.arrowS,element[0],element[1],element[2],element[3])
                elif element[4][0]==2:
                    image=augment(image,self.arrowUp,element[0],element[1],element[2],element[3])
                elif element[4][0]==3:
                    image=augment(image,self.arrowDown,element[0],element[1],element[2],element[3])
        
        #image=cv2.rectangle(image,(image.shape[1]-100,0),(image.shape[1],image.shape[0]),(255,255,255),-1)
        """
        if remainTimeSec:
            minute=int(remainTimeSec/60)
            sec=int(remainTimeSec%60)
            timeText='{m}:{s}'.format(m=minute,s=sec)
            image=cv2.putText(image,timeText,(image.shape[1]-80,50),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),1, cv2.LINE_AA)
        """

        if audioFlag:
            audio=speech
        return image
    
    
class audioPlayer():
    def __init__(self):
        # prepare local media
        audioFile='./audio/48k/stereo/default.wav'
        container = av.open(audioFile)
        self.frames=container.decode(audio=0)

    def getAudioFrame(self):
        global audio
        global audioFlag

        try:
            audioFrame=next(self.frames)
        except StopIteration:
            if audio==0:
                audioFile='./audio/48k/stereo/default.wav'
                audioFlag=True
            else:
                audioFile='./audio/48k/stereo/{0}.wav'.format(audio)
                audioFlag=False
                audio=0
            container = av.open(audioFile)
            self.frames=container.decode(audio=0)
            audioFrame=next(self.frames)
        
        return audioFrame



#cf backup code
#draw area of 3D object
"""
    if landmarks.all() and landmark_px.all():
            
            (xx,xy),(yx,yy),(zx,zy)=BM.getArea(tuple((landmark_px[12]).astype(int)),tuple((landmark_px[16]).astype(int)),tuple((landmark_px[20]).astype(int)))
        
            #print((xx,xy),(yx,yy),(zx,zy))
            x1,y1=tuple(landmark_px[12].astype(int))
            x2,y2=tuple(landmark_px[16].astype(int))
            self.drawArea(image,(x1,y1),(x2,y2),(xx,xy),(yx,yy),(zx,zy))
            #cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.line(image,(x1,y1),(xx,xy),(0,0,255),2)
            cv2.line(image,(x1,y1),(yx,yy),(255,0,0),2)
            cv2.line(image,(x1,y1),(zx,zy),(0,255,255),2)
"""

#draw member method
"""
    def drawArea(self,img,point1,point2,point3,point4,Zpoint):
        pts = np.zeros((4,2), dtype=np.int0)
        pts[0]=point1
        pts[1]=point2
        pts[2]=point3
        pts[3]=point4
        z=(Zpoint[0]-point1[0],Zpoint[1]-point1[1])
        sm = pts.sum(axis=1)                 # 4쌍의 좌표 각각 x+y 계산
        diff = np.diff(pts, axis = 1)       # 4쌍의 좌표 각각 x-y 계산

        topLeft = pts[np.argmin(sm)]        # x+y가 가장 값이 좌상단 좌표
        bottomRight = pts[np.argmax(sm)]     # x+y가 가장 큰 값이 우하단 좌표
        topRight = pts[np.argmin(diff)]     # x-y가 가장 작은 것이 우상단 좌표
        bottomLeft = pts[np.argmax(diff)]   # x-y가 가장 큰 값이 좌하단 좌표

        # 밑변 좌표
        pts1 = np.int0([topLeft, topRight, bottomRight , bottomLeft])
        cv2.polylines(img, [pts1],True, color=(0,255,0), thickness=2)

        pts2=np.zeros((4,2), dtype=np.int0)
        for i in range(0,4):
            pts2[i]=pts1[i]+z
            cv2.line(img,pts1[i],pts2[i],(0,255,0),2)
        
        cv2.polylines(img, [pts2],True, color=(0,255,0), thickness=2)
"""


        

