import numpy as np
from . import basicMethod as BM

class elbow2knee:
    def __init__(self):
        None
    
    def pazeCheck(self,landmark_px,lastPaze):
        DUnit=BM.calculateDistancePx(landmark_px[7],landmark_px[8]) #1unit maybe 50
        if lastPaze>0:
            if BM.calculateDistancePx(landmark_px[14],landmark_px[25])<(DUnit*4): #maybe 200
                return 2
            if BM.calculateDistancePx(landmark_px[13],landmark_px[26])<(DUnit*4): #maybe 200
                return 4
            if (lastPaze==2) or (lastPaze==3):
                return 3
            else:
                return 1
        else:
            if (BM.calPXangle(landmark_px[24],landmark_px[12],landmark_px[26])[2]<150) and (BM.calPXangle(landmark_px[23],landmark_px[11],landmark_px[25])[2]<150):
                return -1
            elif (BM.calculateDistancePx(landmark_px[16],landmark_px[8])<DUnit)and(BM.calculateDistancePx(landmark_px[15],landmark_px[7])<DUnit):
                return 1
            else:
                return 0
    
    def pazeGuide(self,landmark_px,currentPaze,directPoint):
        drawNum=2
        area=np.zeros((drawNum,5,2),dtype=np.int32)
        center=np.zeros((drawNum,2),dtype=np.int32)
        xaxis=np.zeros((drawNum,2),dtype=np.int32)
        yaxis=np.zeros((drawNum,2),dtype=np.int32)
        zaxis=np.zeros((drawNum,2),dtype=np.int32)
        objType=np.zeros((drawNum,2),dtype=np.int32)
        N=0

        if currentPaze==-1:
            return False,area,1
        if currentPaze==0:
            x1, y1 = tuple((landmark_px[16]).astype(int))
            x2, y2 = tuple((landmark_px[8]).astype(int))
            x3, y3 = directPoint[0]
            (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
            center[N]=[x1,y1]
            xaxis[N]=[xx-x1,xy-y1]
            yaxis[N]=[yx-x1,yy-y1]
            zaxis[N]=[zx-x1,zy-y1]
            objType[N]=[0,0]
            N+=1

            x1, y1 = tuple((landmark_px[15]).astype(int))
            x2, y2 = tuple((landmark_px[7]).astype(int))
            x3, y3 = directPoint[0]
            (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
            center[N]=[x1,y1]
            xaxis[N]=[xx-x1,xy-y1]
            yaxis[N]=[yx-x1,yy-y1]
            zaxis[N]=[zx-x1,zy-y1]
            objType[N]=[0,0]
            N+=1
            text=3

        elif currentPaze==1:
            x1, y1 = tuple((landmark_px[14]).astype(int))
            x2, y2 = tuple((landmark_px[23]).astype(int))
            x3, y3 = directPoint[0]
            (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
            center[N]=[x1,y1]
            xaxis[N]=[xx-x1,xy-y1]
            yaxis[N]=[yx-x1,yy-y1]
            zaxis[N]=[zx-x1,zy-y1]
            objType[N]=[0,0]
            N+=1

            x1, y1 = tuple((landmark_px[25]).astype(int))
            x2, y2 = tuple((landmark_px[24]).astype(int))
            x3, y3 = directPoint[0]
            (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
            center[N]=[x1,y1]
            xaxis[N]=[xx-x1,xy-y1]
            yaxis[N]=[yx-x1,yy-y1]
            zaxis[N]=[zx-x1,zy-y1]
            objType[N]=[0,0]
            N+=1

            text=4
            
        elif currentPaze==3:
            x1, y1 = tuple((landmark_px[13]).astype(int))
            x2, y2 = tuple((landmark_px[24]).astype(int))
            x3, y3 = directPoint[0]
            (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
            center[N]=[x1,y1]
            xaxis[N]=[xx-x1,xy-y1]
            yaxis[N]=[yx-x1,yy-y1]
            zaxis[N]=[zx-x1,zy-y1]
            objType[N]=[0,0]
            N+=1

            x1, y1 = tuple((landmark_px[26]).astype(int))
            x2, y2 = tuple((landmark_px[23]).astype(int))
            x3, y3 = directPoint[0]
            (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
            center[N]=[x1,y1]
            xaxis[N]=[xx-x1,xy-y1]
            yaxis[N]=[yx-x1,yy-y1]
            zaxis[N]=[zx-x1,zy-y1]
            objType[N]=[0,0]
            N+=1

            text=4

        else:
            return False,area,0

        for i in range(drawNum):
            area[i][0]=center[i]
            area[i][1]=xaxis[i]
            area[i][2]=yaxis[i]
            area[i][3]=zaxis[i]
            area[i][4]=objType[i]

        return True,area,text

class hamstring():
    def __init__(self,isLeft):
        self.isLeft=isLeft
    
    def pazeCheck(self,landmark_px,lastPaze):
        DUnit=BM.calculateDistancePx(landmark_px[7],landmark_px[8]) #1unit maybe 50
        #DUnit=50
        #left paze
        if self.isLeft:
            if lastPaze>2:
                if BM.calPXangle(landmark_px[26],landmark_px[24],landmark_px[28])[2]<90:
                    return 3
                else:
                    return 4
            else:
                if (BM.calPXangle(landmark_px[24],landmark_px[12],landmark_px[26])[2]>150) and (BM.calPXangle(landmark_px[23],landmark_px[11],landmark_px[25])[2]>150):
                    return -1
                elif ((BM.calculateDistancePx(landmark_px[11],landmark_px[12])>50)) and (BM.calculateDistancePx(landmark_px[23],landmark_px[24])>50):
                    return 0
                elif (BM.calPXangle(landmark_px[23],landmark_px[11],landmark_px[25])[2]>60) and (BM.calPXangle(landmark_px[24],landmark_px[12],landmark_px[26])[2]<140):
                    return 1
                elif BM.calculateDistancePx(landmark_px[11],landmark_px[25])<(DUnit*2):
                    return 2
                else:
                    return 3

        #right paze
        else:
            if lastPaze>0:
                if BM.calPXangle(landmark_px[25],landmark_px[23],landmark_px[27])[2]<90:
                    return 1
                else:
                    return 2
            else:
                if (BM.calPXangle(landmark_px[24],landmark_px[12],landmark_px[26])[2]<60) and (BM.calPXangle(landmark_px[23],landmark_px[11],landmark_px[25])[2]>140):
                    return 1
                else:
                    return 0

    def pazeGuide(self,landmark_px,currentPaze,directPoint):
        drawNum=2
        area=np.zeros((drawNum,5,2),dtype=np.int32)
        center=np.zeros((drawNum,2),dtype=np.int32)
        xaxis=np.zeros((drawNum,2),dtype=np.int32)
        yaxis=np.zeros((drawNum,2),dtype=np.int32)
        zaxis=np.zeros((drawNum,2),dtype=np.int32)
        objType=np.zeros((drawNum,2),dtype=np.int32)
        N=0
        if self.isLeft:
            if currentPaze==-1:
                return False,area,2
            elif currentPaze==0:
                x1, y1 = tuple((landmark_px[11]).astype(int))
                x2, y2 = tuple((landmark_px[12]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[0,0]
                N+=1

                x1, y1 = tuple((landmark_px[23]).astype(int))
                x2, y2 = tuple((landmark_px[24]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[0,0]
                N+=1

                text=5
            elif currentPaze==1:
                x1, y1 = tuple((landmark_px[25]).astype(int))
                x2, y2 = tuple((landmark_px[23]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[2,0]
                N+=1

                x1, y1 = tuple((landmark_px[28]).astype(int))
                x2, y2 = tuple((landmark_px[24]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[0,0]
                N+=1

                text=6
            elif currentPaze==2:
                x1, y1 = tuple((landmark_px[11]).astype(int))
                x2, y2 = tuple((landmark_px[25]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[1,0]
                N+=1

                x1, y1 = tuple((landmark_px[11]).astype(int))
                x2, y2 = tuple((landmark_px[23]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[3,0]
                N+=1

                text=7
            elif currentPaze==3:
                x1, y1 = tuple((landmark_px[24]).astype(int))
                x2, y2 = tuple((landmark_px[26]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[2,0]
                N+=1

                x1, y1 = tuple((landmark_px[11]).astype(int))
                x2, y2 = tuple((landmark_px[23]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[3,0]
                N+=1

                text=8
            elif currentPaze==4:
                x1, y1 = tuple((landmark_px[24]).astype(int))
                x2, y2 = tuple((landmark_px[26]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[2,0]
                N+=1

                x1, y1 = tuple((landmark_px[11]).astype(int))
                x2, y2 = tuple((landmark_px[23]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[3,0]
                N+=1

                text=9
            else:
                return False,area,0
            
            for i in range(drawNum):
                area[i][0]=center[i]
                area[i][1]=xaxis[i]
                area[i][2]=yaxis[i]
                area[i][3]=zaxis[i]
                area[i][4]=objType[i]

            return True,area,text
        else:
            if currentPaze==0:
                return False,area,10
            elif currentPaze==1:
                x1, y1 = tuple((landmark_px[23]).astype(int))
                x2, y2 = tuple((landmark_px[25]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[2,0]
                N+=1

                x1, y1 = tuple((landmark_px[12]).astype(int))
                x2, y2 = tuple((landmark_px[24]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[3,0]
                N+=1

                text=8
            elif currentPaze==2:
                x1, y1 = tuple((landmark_px[23]).astype(int))
                x2, y2 = tuple((landmark_px[25]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[2,0]
                N+=1

                x1, y1 = tuple((landmark_px[12]).astype(int))
                x2, y2 = tuple((landmark_px[24]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[3,0]
                N+=1

                text=9
            else:
                return False,area,0
            
            for i in range(drawNum):
                area[i][0]=center[i]
                area[i][1]=xaxis[i]
                area[i][2]=yaxis[i]
                area[i][3]=zaxis[i]
                area[i][4]=objType[i]

            return True,area,text

class hitJoint():
    def __init__(self):
        None

    def pazeCheck(self,landmark_px,lastPaze):
        DUnit=BM.calculateDistancePx(landmark_px[9],landmark_px[10]) #1unit maybe 50

        if lastPaze>0:
            if BM.calPXangle(landmark_px[11],landmark_px[23],landmark_px[25])[2]<50:
                return 1
            elif BM.calPXangle(landmark_px[12],landmark_px[24],landmark_px[26])[2]<50:
                return 2
            else:
                return lastPaze
        else:
            if (BM.calPXangle(landmark_px[24],landmark_px[12],landmark_px[26])[2]>150) and (BM.calPXangle(landmark_px[23],landmark_px[11],landmark_px[25])[2]>150):
                return -1
            elif (BM.calPXangle(landmark_px[23],landmark_px[7],landmark_px[25])[2]>30) and (BM.calPXangle(landmark_px[24],landmark_px[8],landmark_px[26])[2]>30):
                return 0
            else:
                return 1
    
    def pazeGuide(self,landmark_px,currentPaze,directPoint):
        drawNum=2
        area=np.zeros((drawNum,5,2),dtype=np.int32)
        center=np.zeros((drawNum,2),dtype=np.int32)
        xaxis=np.zeros((drawNum,2),dtype=np.int32)
        yaxis=np.zeros((drawNum,2),dtype=np.int32)
        zaxis=np.zeros((drawNum,2),dtype=np.int32)
        objType=np.zeros((drawNum,2),dtype=np.int32)
        N=0

        if currentPaze==-1:
            return False,None,2
        elif currentPaze==0:
            x1, y1 = tuple((landmark_px[26]).astype(int))
            x2, y2 = tuple((landmark_px[24]).astype(int))
            x3, y3 = directPoint[0]
            (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
            center[N]=[x1,y1]
            xaxis[N]=[xx-x1,xy-y1]
            yaxis[N]=[yx-x1,yy-y1]
            zaxis[N]=[zx-x1,zy-y1]
            objType[N]=[2,0]
            N+=1

            x1, y1 = tuple((landmark_px[25]).astype(int))
            x2, y2 = tuple((landmark_px[23]).astype(int))
            x3, y3 = directPoint[0]
            (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
            center[N]=[x1,y1]
            xaxis[N]=[xx-x1,xy-y1]
            yaxis[N]=[yx-x1,yy-y1]
            zaxis[N]=[zx-x1,zy-y1]
            objType[N]=[2,0]
            N+=1

            text=15
        elif currentPaze==1:
            x1, y1 = tuple((landmark_px[26]).astype(int))
            x2, y2 = tuple((landmark_px[24]).astype(int))
            x3, y3 = directPoint[0]
            (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
            center[N]=[x1,y1]
            xaxis[N]=[xx-x1,xy-y1]
            yaxis[N]=[yx-x1,yy-y1]
            zaxis[N]=[zx-x1,zy-y1]
            objType[N]=[2,0]
            N+=1

            x1, y1 = tuple((landmark_px[25]).astype(int))
            x2, y2 = tuple((landmark_px[23]).astype(int))
            x3, y3 = directPoint[0]
            (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
            center[N]=[x1,y1]
            xaxis[N]=[xx-x1,xy-y1]
            yaxis[N]=[yx-x1,yy-y1]
            zaxis[N]=[zx-x1,zy-y1]
            objType[N]=[2,0]
            N+=1

            text=16
        elif currentPaze==2:
            x1, y1 = tuple((landmark_px[26]).astype(int))
            x2, y2 = tuple((landmark_px[24]).astype(int))
            x3, y3 = directPoint[0]
            (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
            center[N]=[x1,y1]
            xaxis[N]=[xx-x1,xy-y1]
            yaxis[N]=[yx-x1,yy-y1]
            zaxis[N]=[zx-x1,zy-y1]
            objType[N]=[2,0]
            N+=1

            x1, y1 = tuple((landmark_px[25]).astype(int))
            x2, y2 = tuple((landmark_px[23]).astype(int))
            x3, y3 = directPoint[0]
            (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
            center[N]=[x1,y1]
            xaxis[N]=[xx-x1,xy-y1]
            yaxis[N]=[yx-x1,yy-y1]
            zaxis[N]=[zx-x1,zy-y1]
            objType[N]=[2,0]
            N+=1

            text=16
        else:
            return False,area,0
        
        for i in range(drawNum):
            area[i][0]=center[i]
            area[i][1]=xaxis[i]
            area[i][2]=yaxis[i]
            area[i][3]=zaxis[i]
            area[i][4]=objType[i]

        return True,area,text

class adductor():
    def __init__(self,isLeft):
        self.isLeft=isLeft

    def pazeCheck(self,landmark_px,lastPaze):
        DUnit=BM.calculateDistancePx(landmark_px[9],landmark_px[10]) #1unit maybe 50
        if self.isLeft:
            if (BM.calPXangle(landmark_px[24],landmark_px[12],landmark_px[26])[2]>150) and (BM.calPXangle(landmark_px[23],landmark_px[11],landmark_px[25])[2]>150):
                return -1
            elif BM.calPXangle(landmark_px[25],landmark_px[23],landmark_px[27])[2]<140:
                return 0
            else:
                return 1
        else:
            if (BM.calPXangle(landmark_px[24],landmark_px[12],landmark_px[26])[2]>150) and (BM.calPXangle(landmark_px[23],landmark_px[11],landmark_px[25])[2]>150):
                return -1
            elif BM.calPXangle(landmark_px[26],landmark_px[24],landmark_px[28])[2]<140:
                return 0
            else:
                return 1
    
    def pazeGuide(self,landmark_px,currentPaze,directPoint):
        drawNum=1
        area=np.zeros((drawNum,5,2),dtype=np.int32)
        center=np.zeros((drawNum,2),dtype=np.int32)
        xaxis=np.zeros((drawNum,2),dtype=np.int32)
        yaxis=np.zeros((drawNum,2),dtype=np.int32)
        zaxis=np.zeros((drawNum,2),dtype=np.int32)
        objType=np.zeros((drawNum,2),dtype=np.int32)
        N=0

        if self.isLeft:
            if currentPaze==-1:
                return False,None,2
            elif currentPaze==0:
                x1, y1 = tuple((landmark_px[25]).astype(int))
                x2, y2 = tuple((landmark_px[27]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[3,0]
                N+=1

                text=18
            elif currentPaze==1:
                x1, y1 = tuple((landmark_px[11]).astype(int))
                x2, y2 = tuple((landmark_px[23]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[3,0]
                N+=1

                text=19
            else:
                return False,area,0
        else:
            if currentPaze==-1:
                return False,None,2
            elif currentPaze==0:
                x1, y1 = tuple((landmark_px[26]).astype(int))
                x2, y2 = tuple((landmark_px[28]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[3,0]
                N+=1

                text=20
            elif currentPaze==1:
                x1, y1 = tuple((landmark_px[12]).astype(int))
                x2, y2 = tuple((landmark_px[24]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[3,0]
                N+=1

                text=19
            else:
                return False,area,0
        
        for i in range(drawNum):
            area[i][0]=center[i]
            area[i][1]=xaxis[i]
            area[i][2]=yaxis[i]
            area[i][3]=zaxis[i]
            area[i][4]=objType[i]

        return True,area,text

class GMsquat():
    def __init__(self):
        None

    def pazeCheck(self,landmark_px,lastPaze):
        #DUnit=BM.calculateDistancePx(landmark_px[9],landmark_px[10]) #1unit maybe 50
        DUnit=50
        if lastPaze>0:
            if (BM.calPXangle(landmark_px[23],landmark_px[11],landmark_px[25])[2]<70) and (BM.calPXangle(landmark_px[24],landmark_px[12],landmark_px[26])[2]<70):
                return 2
            else:
                return 1
        else:
            if (BM.calPXangle(landmark_px[24],landmark_px[12],landmark_px[26])[2]<150) and (BM.calPXangle(landmark_px[23],landmark_px[11],landmark_px[25])[2]<150):
                return -1
            elif (BM.calculateDistancePx(landmark_px[11],landmark_px[12])>DUnit) and (BM.calculateDistancePx(landmark_px[23],landmark_px[24])>DUnit):
                return 0
            else:
                return 1
    
    def pazeGuide(self,landmark_px,currentPaze,directPoint):
        drawNum=2
        area=np.zeros((drawNum,5,2),dtype=np.int32)
        center=np.zeros((drawNum,2),dtype=np.int32)
        xaxis=np.zeros((drawNum,2),dtype=np.int32)
        yaxis=np.zeros((drawNum,2),dtype=np.int32)
        zaxis=np.zeros((drawNum,2),dtype=np.int32)
        objType=np.zeros((drawNum,2),dtype=np.int32)
        N=0

        if currentPaze==-1:
            return False,area,1
        elif currentPaze==0:
            return False,area,22
        elif currentPaze==1:
            x1, y1 = tuple((landmark_px[11]).astype(int))
            x2, y2 = tuple((landmark_px[25]).astype(int))
            x3, y3 = directPoint[0]
            (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
            center[N]=[x1,y1]
            xaxis[N]=[xx-x1,xy-y1]
            yaxis[N]=[yx-x1,yy-y1]
            zaxis[N]=[zx-x1,zy-y1]
            objType[N]=[0,0]
            N+=1

            x1, y1 = tuple((landmark_px[23]).astype(int))
            x2, y2 = tuple((landmark_px[25]).astype(int))
            x3, y3 = directPoint[1]
            (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
            center[N]=[x1,y1]
            xaxis[N]=[xx-x1,xy-y1]
            yaxis[N]=[yx-x1,yy-y1]
            zaxis[N]=[zx-x1,zy-y1]
            objType[N]=[2,0]
            N+=1

            text=23
        else:
            return False,area,0
        
        for i in range(drawNum):
            area[i][0]=center[i]
            area[i][1]=xaxis[i]
            area[i][2]=yaxis[i]
            area[i][3]=zaxis[i]
            area[i][4]=objType[i]

        return True,area,text

class oneLagStand():
    def __init__(self,isLeft):
        self.isLeft=isLeft

    def pazeCheck(self,landmark_px,lastPaze):
        #DUnit=BM.calculateDistancePx(landmark_px[9],landmark_px[10]) #1unit maybe 50
        DUnit=50
        if self.isLeft:
            if lastPaze>1:
                if BM.calPXangle(landmark_px[25],landmark_px[23],landmark_px[27])[2]>110:
                    return 3
                else:
                    return 2
            else:
                if (BM.calPXangle(landmark_px[24],landmark_px[12],landmark_px[26])[2]<150) and (BM.calPXangle(landmark_px[23],landmark_px[11],landmark_px[25])[2]<150):
                    return -1
                elif (BM.calculateDistancePx(landmark_px[11],landmark_px[12])>DUnit) and (BM.calculateDistancePx(landmark_px[23],landmark_px[24])>DUnit):
                    return 0
                elif BM.calPXangle(landmark_px[25],landmark_px[23],landmark_px[27])[2]>100:
                    return 1
                else:
                    return 2
        else:
            if lastPaze>1:
                if BM.calPXangle(landmark_px[26],landmark_px[24],landmark_px[28])[2]>110:
                    return 3
                else:
                    return 2
            else:
                if (BM.calPXangle(landmark_px[24],landmark_px[12],landmark_px[26])[2]<150) and (BM.calPXangle(landmark_px[23],landmark_px[11],landmark_px[25])[2]<150):
                    return -1
                elif (BM.calculateDistancePx(landmark_px[11],landmark_px[12])>DUnit) and (BM.calculateDistancePx(landmark_px[23],landmark_px[24])>DUnit):
                    return 0
                elif BM.calPXangle(landmark_px[26],landmark_px[24],landmark_px[28])[2]>100:
                    return 1
                else:
                    return 2
    
    def pazeGuide(self,landmark_px,currentPaze,directPoint):
        drawNum=1
        area=np.zeros((drawNum,5,2),dtype=np.int32)
        center=np.zeros((drawNum,2),dtype=np.int32)
        xaxis=np.zeros((drawNum,2),dtype=np.int32)
        yaxis=np.zeros((drawNum,2),dtype=np.int32)
        zaxis=np.zeros((drawNum,2),dtype=np.int32)
        objType=np.zeros((drawNum,2),dtype=np.int32)
        N=0

        if self.isLeft:
            if currentPaze==-1:
                return False,None,1
            elif currentPaze==0:
                return False,None,25
            elif currentPaze==1:
                x1, y1 = tuple((landmark_px[25]).astype(int))
                x2, y2 = tuple((landmark_px[23]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[2,0]
                N+=1

                text=26
            elif currentPaze==2:
                x1, y1 = tuple((landmark_px[27]).astype(int))
                x2, y2 = tuple((landmark_px[25]).astype(int))
                x3, y3 = directPoint[3]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[2,0]
                N+=1

                text=27
            else:
                return False,area,0
        else:
            if currentPaze==-1:
                return False,None,1
            elif currentPaze==0:
                return False,None,28
            elif currentPaze==1:
                x1, y1 = tuple((landmark_px[26]).astype(int))
                x2, y2 = tuple((landmark_px[24]).astype(int))
                x3, y3 = directPoint[0]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[2,0]
                N+=1

                text=29
            elif currentPaze==2:
                x1, y1 = tuple((landmark_px[28]).astype(int))
                x2, y2 = tuple((landmark_px[26]).astype(int))
                x3, y3 = directPoint[3]
                (xx,xy),(yx,yy),(zx,zy)=BM.getArea((x1,y1),(x2,y2),(x3,y3))
                center[N]=[x1,y1]
                xaxis[N]=[xx-x1,xy-y1]
                yaxis[N]=[yx-x1,yy-y1]
                zaxis[N]=[zx-x1,zy-y1]
                objType[N]=[2,0]
                N+=1

                text=30
            else:
                return False,area,0
        
        for i in range(drawNum):
            area[i][0]=center[i]
            area[i][1]=xaxis[i]
            area[i][2]=yaxis[i]
            area[i][3]=zaxis[i]
            area[i][4]=objType[i]

        return True,area,text






