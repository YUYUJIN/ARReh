from .module import poseCheck as PC

class content:
    def __init__(self,Activity):
        self.Activity=Activity
        self.currentPaze=0
        self.currentRun=False
        self.directPoint=[]
    
    def run(self,landmark_px,size):
        self.directPoint=[(0,0),(size[1],0),(0,size[0]),(size[1],size[0])]
        
        #all method return meet format that active,speechText,AreaList
        if self.Activity=='팔꿈치 무릎 맞닿기':
            return self.elbow2kneeAct(landmark_px)
        elif self.Activity=='햄스트링 스트레칭(좌)':
            return self.hamstringAct(landmark_px,True)
        elif self.Activity=='햄스트링 스트레칭(우)':
            return self.hamstringAct(landmark_px,False)
        elif self.Activity=='고관절 좌우 풀어주기':
            return self.hitJointAct(landmark_px)
        elif self.Activity=='내전근 스트레칭(좌)':
            return self.adductorAct(landmark_px,True)
        elif self.Activity=='내전근 스트레칭(우)':
            return self.adductorAct(landmark_px,False)
        elif self.Activity=='굿모닝스쿼트':
            return self.GMsquatAct(landmark_px)
        elif self.Activity=='한발 서기(좌)':
            return self.oneLagStandAct(landmark_px,True)
        elif self.Activity=='한발 서기(우)':
            return self.oneLagStandAct(landmark_px,False)
        else:
            return False,0,0

    def elbow2kneeAct(self,landmark_px):
        if landmark_px.any():
            if self.currentRun:
                guide=PC.elbow2knee()

                self.currentPaze=guide.pazeCheck(landmark_px,self.currentPaze)
                isGuide,area,speech=guide.pazeGuide(landmark_px,self.currentPaze,self.directPoint)

                return isGuide,speech,area
            else:
                self.currentRun=True
                return False,12,None
        else:
            return False,1,None
            
    def hamstringAct(self,landmark_px,isLeft):
        if landmark_px.any():
            if self.currentRun:
                guide=PC.hamstring(isLeft)

                self.currentPaze=guide.pazeCheck(landmark_px,self.currentPaze)
                isGuide,area,speech=guide.pazeGuide(landmark_px,self.currentPaze,self.directPoint)

                return isGuide,speech,area
            else:
                self.currentRun=True
                return False,13,None
        else:
            return False,2,None

    def hitJointAct(self,landmark_px):
        if landmark_px.any():
            if self.currentRun:
                guide=PC.hitJoint()

                self.currentPaze=guide.pazeCheck(landmark_px,self.currentPaze)
                isGuide,area,speech=guide.pazeGuide(landmark_px,self.currentPaze,self.directPoint)

                return isGuide,speech,area
            else:
                self.currentRun=True
                return False,14,None
        else:
            return False,2,None

    def adductorAct(self,landmark_px,isLeft):
        if landmark_px.any():
            if self.currentRun:
                guide=PC.adductor(isLeft)

                self.currentPaze=guide.pazeCheck(landmark_px,self.currentPaze)
                isGuide,area,speech=guide.pazeGuide(landmark_px,self.currentPaze,self.directPoint)

                return isGuide,speech,area
            else:
                self.currentRun=True
                return False,17,None
        else:
            return False,2,None

    def GMsquatAct(self,landmark_px):
        if landmark_px.any():
            if self.currentRun:
                guide=PC.GMsquat()

                self.currentPaze=guide.pazeCheck(landmark_px,self.currentPaze)
                isGuide,area,speech=guide.pazeGuide(landmark_px,self.currentPaze,self.directPoint)

                return isGuide,speech,area
            else:
                self.currentRun=True
                return False,21,None
        else:
            return False,1,None
    
    def oneLagStandAct(self,landmark_px,isLeft):
        if landmark_px.any():
            if self.currentRun:
                guide=PC.oneLagStand(isLeft)

                self.currentPaze=guide.pazeCheck(landmark_px,self.currentPaze)
                isGuide,area,speech=guide.pazeGuide(landmark_px,self.currentPaze,self.directPoint)

                return isGuide,speech,area
            else:
                self.currentRun=True
                return False,21,None
        else:
            return False,1,None