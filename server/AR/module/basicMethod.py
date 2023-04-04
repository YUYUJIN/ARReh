import cv2
import mediapipe as mp
import numpy as np
import math
from numba import jit
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def detectPose(image, pose, display=True):
    '''
    This function performs pose detection on an image.
    Args:
        image: The input image with a prominent person whose pose landmarks needs to be detected.
        pose: The pose setup function required to perform the pose detection.
        display: A boolean value that is if set to true the function displays the original input image, the resultant image, 
                 and the pose landmarks in 3D plot and returns nothing.
    Returns:
        output_image: The input image with the detected pose landmarks drawn.
        landmarks: A list of detected landmarks converted into their original scale.
    '''
    # Create a copy of the input image.
    output_image = image.copy()
    
    # Convert the image from BGR into RGB format.
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Perform the Pose Detection.
    results = pose.process(imageRGB)
    
    # Retrieve the height and width of the input image.
    height, width, _ = image.shape
    
    # Initialize a list to store the detected landmarks.
    #landmarks = []

    # Initialize a np array to store the detected landmarks.
    #landmarks=np.zeros((33,3))
    landmark_px=np.zeros((33,2))
    
    # Check if any landmarks are detected.
    if results.pose_landmarks:
        # Draw Pose landmarks on the output image.
        # mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
        #                             connections=mp_pose.POSE_CONNECTIONS)
        
        # Iterate over the detected landmarks.
        i=0
        for landmark in results.pose_landmarks.landmark:
            
            # Append the landmark into the list.
            #landmarks.append((int(landmark.x * width), int(landmark.y * height),
            #                      (landmark.z * width)))
            
            landmark_px[i]=[int(landmark.x*width),int(landmark.y*height)]
            i+=1

        # Iterate over the detected landmarks.
        """
        i=0
        for landmark in results.pose_world_landmarks.landmark:
            
            # Append the landmark into the list.
            #landmarks.append((int(landmark.x * width), int(landmark.y * height),
            #                      (landmark.z * width)))
            landmarks[i]=[(landmark.x*width), (landmark.y*height), (landmark.z*width)]
            i+=1
        """
    # Return the output image and the found landmarks.
    return output_image, landmark_px
"""
def calculateAngle3D(landmark1, landmark2, landmark3):
    '''
    This function calculates angle between three different landmarks.
    Args:
        landmark1: The first landmark containing the x,y and z coordinates.
        landmark2: The second landmark containing the x,y and z coordinates.
        landmark3: The third landmark containing the x,y and z coordinates.
    Returns:
        angle: The calculated angle between the three landmarks.

    '''

    # Get the required landmarks coordinates.
    x1, y1, z1 = landmark1
    x2, y2, z2 = landmark2
    x3, y3, z3 = landmark3

    # vectors landmark2 to landmark1, landmark2 to landmark3
    vector1=np.array([x1-x2,y1-y2,z1-z2])
    vector2=np.array([x3-x2,y3-y2,z3-z2])

    # Calculate the angle between the three points
    vector1size=np.linalg.norm(vector1)
    vector2size=np.linalg.norm(vector2)
    vectorDot=vector1.dot(vector2)
    angle = math.degrees(math.acos(vectorDot/(vector1size*vector2size)))
    
    # Check if the angle is less than zero.
    if angle < 0:

        # Add 360 to the found angle.
        angle = 0
    
    # Return the calculated angle.
    return angle

def calculateAngle2D(landmark1, landmark2, landmark3):
    '''
    This function calculates angle between three different landmarks.
    Args:
        landmark1: The first landmark containing the x,y and z coordinates.
        landmark2: The second landmark containing the x,y and z coordinates.
        landmark3: The third landmark containing the x,y and z coordinates.
    Returns:
        angle: The calculated angle between the three landmarks.

    '''

    # Get the required landmarks coordinates.
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    # Calculate the angle between the three points
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    
    # Check if the angle is less than zero.
    if angle < 0:

        # Add 360 to the found angle.
        angle = 0
    
    # Return the calculated angle.
    return angle

def calculateDistance2D(landmark1, landmark2):
    # Get the required landmarks coordinates.
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2

    # Calculate the distance between the two points
    distance = math.sqrt(math.pow((x2-x1),2)+math.pow((y2-y1),2))
    
    # Check if the distance is less than zero.
    if distance < 0:
        distance=0
    
    # Return the calculated distance.
    return distance

def calculateDistance3D(landmark1, landmark2):
    # Get the required landmarks coordinates.
    x1, y1, z1 = landmark1
    x2, y2, z2 = landmark2

    # Calculate the distance between the two points
    distance = math.sqrt(math.pow((x2-x1),2)+math.pow((y2-y1),2)+math.pow((z2-z1),2))
    
    # Check if the distance is less than zero.
    if distance < 0:
        distance=0
    
    # Return the calculated distance.
    return distance
"""
def calculateSidePx(point1, point2):
    # Get the required landmarks coordinates.
    x1, y1 = point1
    x2, y2 = point2

    # Calculate the distance between the two points
    distance = math.sqrt(math.pow((x2-x1),2)+math.pow((y2-y1),2))
    
    # Check if the distance is less than zero.
    if distance < 0:
        distance=0
    
    side=distance*(math.sqrt(2)/2)
    return distance,side
"""
def findZpoint(point1,point2,side):
    x1,y1=point1
    x2,y2=point2
    
    x=Symbol('x')
    y=Symbol('y')

    s1=(x1-x)**2+(y1-y)**2-side**2
    s2=((x1-x2)*(x1-x))+((y1-y2)*(y1-y))

    result=solve((s1,s2),x,y,dict=False)

    return result

def findXYpoint(point1,point2,Zpoint,side):
    x1,y1=point1
    x2,y2=point2
    zx,zy=Zpoint
    
    x=Symbol('x')
    y=Symbol('y')

    mx,my=((x1+x2)/2,(y1+y2)/2)

    #y-my=gradient*(x-mx)
    s1=((zy-y1)/(zx-x1))*(x-mx)-y+my
    s2=(x1-x)**2+(y1-y)**2-(side**2)

    result=solve((s1,s2),x,y,dict=False)
    if len(result)>1:
        return result
    else:
        result=[[mx,my],[mx,my]]
        return result
"""

def findZpoint(point1,point2,side):
    x1,y1=point1
    x2,y2=point2
    result=[[0,0],[0,0]]

    #(x1-x)**2+(y1-y)**2-side**2
    #((x1-x2)*(x1-x))+((y1-y2)*(y1-y))
    if ((y1-y2)==0) or ((x1-x2)==0):
        result[0]=[x1,y1]
        result[1]=[x1,y1]
    else:
        """
        h=(x1-x2)/(y1-y2)
    
        #ax**2+bx+c
        a=1+math.pow(h,2)
        b=(2*x1*a)*(-1)
        c=math.pow(x1,2)*a-math.pow(side,2)

        result[0][0]=((-b+(math.sqrt(math.pow(b,2)-4*a*c)))/2*a)
        result[1][0]=((-b-(math.sqrt(math.pow(b,2)-4*a*c)))/2*a)
        result[0][1]=h*(x1-result[0][0])+y1
        result[1][1]=h*(x1-result[1][0])+y1
        """
        result[0][0]=(x1**2 - x1*x2 + y1**2 - y1*y2 + (-y1 + y2)*(side*(x1 - x2)/math.sqrt(x1**2 - 2*x1*x2 + x2**2 + y1**2 - 2*y1*y2 + y2**2) + y1))/(x1 - x2)
        result[0][1]=side*(x1 - x2)/math.sqrt(x1**2 - 2*x1*x2 + x2**2 + y1**2 - 2*y1*y2 + y2**2) + y1
        result[1][0]=(x1**2 - x1*x2 + y1**2 - y1*y2 + (-y1 + y2)*(-side*(x1 - x2)/math.sqrt(x1**2 - 2*x1*x2 + x2**2 + y1**2 - 2*y1*y2 + y2**2) + y1))/(x1 - x2)
        result[1][1]=-side*(x1 - x2)/math.sqrt(x1**2 - 2*x1*x2 + x2**2 + y1**2 - 2*y1*y2 + y2**2) + y1
    return result

def findXYpoint(point1,point2,Zpoint,side):
    x1,y1=point1
    x2,y2=point2
    zx,zy=Zpoint
    mx,my=((x1+x2)/2,(y1+y2)/2)
    result=[[0,0],[0,0]]

    #y-my=gradient*(x-mx)
    #((zy-y1)/(zx-x1))*(x-mx)-y+my
    #(x1-x)**2+(y1-y)**2-(side**2)
    
    if ((zx-x1)==0) or ((zy-y1)==0) or (((x1-x2)==0)) or ((y1-y2)==0):
        result[0]=[mx,my]
        result[1]=[mx,my]
    else:
        """
        h=(zy-y1)/(zx-x1)
        s=(my-y1-(mx*h))

        #ax**2+bx+c
        a=math.pow(h,2)+1
        b=(2*h*s)-2*x1
        c=math.pow(x1,2)+math.pow(s,2)-math.pow(side,2)

        result[0][0]=((-b+(math.sqrt(math.pow(b,2)-4*a*c)))/2*a)
        result[1][0]=((-b-(math.sqrt(math.pow(b,2)-4*a*c)))/2*a)
        result[0][1]=h*(result[0][0]-mx)+my
        result[1][1]=h*(result[1][0]-mx)+my
        """
        result[0][0]=(mx*y1 - mx*zy - my*x1 + my*zx + (x1 - zx)*((y1 - zy)*math.sqrt(-mx**2*y1**2 + 2*mx**2*y1*zy - mx**2*zy**2 + 2*mx*my*x1*y1 - 2*mx*my*x1*zy - 2*mx*my*y1*zx + 2*mx*my*zx*zy - 2*mx*x1*y1*zy + 2*mx*x1*zy**2 + 2*mx*y1**2*zx - 2*mx*y1*zx*zy - my**2*x1**2 + 2*my**2*x1*zx - my**2*zx**2 + 2*my*x1**2*zy - 2*my*x1*y1*zx - 2*my*x1*zx*zy + 2*my*y1*zx**2 + side**2*x1**2 - 2*side**2*x1*zx + side**2*y1**2 - 2*side**2*y1*zy + side**2*zx**2 + side**2*zy**2 - x1**2*zy**2 + 2*x1*y1*zx*zy - y1**2*zx**2)/(x1**2 - 2*x1*zx + y1**2 - 2*y1*zy + zx**2 + zy**2) + (-mx*x1*y1 + mx*x1*zy + mx*y1*zx - mx*zx*zy + my*x1**2 - 2*my*x1*zx + my*zx**2 + x1**2*y1 - x1**2*zy - x1*y1*zx + x1*zx*zy + y1**3 - 2*y1**2*zy + y1*zy**2)/(x1**2 - 2*x1*zx + y1**2 - 2*y1*zy + zx**2 + zy**2)))/(y1 - zy)
        result[0][1]=(y1 - zy)*math.sqrt(-mx**2*y1**2 + 2*mx**2*y1*zy - mx**2*zy**2 + 2*mx*my*x1*y1 - 2*mx*my*x1*zy - 2*mx*my*y1*zx + 2*mx*my*zx*zy - 2*mx*x1*y1*zy + 2*mx*x1*zy**2 + 2*mx*y1**2*zx - 2*mx*y1*zx*zy - my**2*x1**2 + 2*my**2*x1*zx - my**2*zx**2 + 2*my*x1**2*zy - 2*my*x1*y1*zx - 2*my*x1*zx*zy + 2*my*y1*zx**2 + side**2*x1**2 - 2*side**2*x1*zx + side**2*y1**2 - 2*side**2*y1*zy + side**2*zx**2 + side**2*zy**2 - x1**2*zy**2 + 2*x1*y1*zx*zy - y1**2*zx**2)/(x1**2 - 2*x1*zx + y1**2 - 2*y1*zy + zx**2 + zy**2) + (-mx*x1*y1 + mx*x1*zy + mx*y1*zx - mx*zx*zy + my*x1**2 - 2*my*x1*zx + my*zx**2 + x1**2*y1 - x1**2*zy - x1*y1*zx + x1*zx*zy + y1**3 - 2*y1**2*zy + y1*zy**2)/(x1**2 - 2*x1*zx + y1**2 - 2*y1*zy + zx**2 + zy**2)
        result[1][0]=(mx*y1 - mx*zy - my*x1 + my*zx + (x1 - zx)*(-(y1 - zy)*math.sqrt(-mx**2*y1**2 + 2*mx**2*y1*zy - mx**2*zy**2 + 2*mx*my*x1*y1 - 2*mx*my*x1*zy - 2*mx*my*y1*zx + 2*mx*my*zx*zy - 2*mx*x1*y1*zy + 2*mx*x1*zy**2 + 2*mx*y1**2*zx - 2*mx*y1*zx*zy - my**2*x1**2 + 2*my**2*x1*zx - my**2*zx**2 + 2*my*x1**2*zy - 2*my*x1*y1*zx - 2*my*x1*zx*zy + 2*my*y1*zx**2 + side**2*x1**2 - 2*side**2*x1*zx + side**2*y1**2 - 2*side**2*y1*zy + side**2*zx**2 + side**2*zy**2 - x1**2*zy**2 + 2*x1*y1*zx*zy - y1**2*zx**2)/(x1**2 - 2*x1*zx + y1**2 - 2*y1*zy + zx**2 + zy**2) + (-mx*x1*y1 + mx*x1*zy + mx*y1*zx - mx*zx*zy + my*x1**2 - 2*my*x1*zx + my*zx**2 + x1**2*y1 - x1**2*zy - x1*y1*zx + x1*zx*zy + y1**3 - 2*y1**2*zy + y1*zy**2)/(x1**2 - 2*x1*zx + y1**2 - 2*y1*zy + zx**2 + zy**2)))/(y1 - zy)
        result[1][1]=-(y1 - zy)*math.sqrt(-mx**2*y1**2 + 2*mx**2*y1*zy - mx**2*zy**2 + 2*mx*my*x1*y1 - 2*mx*my*x1*zy - 2*mx*my*y1*zx + 2*mx*my*zx*zy - 2*mx*x1*y1*zy + 2*mx*x1*zy**2 + 2*mx*y1**2*zx - 2*mx*y1*zx*zy - my**2*x1**2 + 2*my**2*x1*zx - my**2*zx**2 + 2*my*x1**2*zy - 2*my*x1*y1*zx - 2*my*x1*zx*zy + 2*my*y1*zx**2 + side**2*x1**2 - 2*side**2*x1*zx + side**2*y1**2 - 2*side**2*y1*zy + side**2*zx**2 + side**2*zy**2 - x1**2*zy**2 + 2*x1*y1*zx*zy - y1**2*zx**2)/(x1**2 - 2*x1*zx + y1**2 - 2*y1*zy + zx**2 + zy**2) + (-mx*x1*y1 + mx*x1*zy + mx*y1*zx - mx*zx*zy + my*x1**2 - 2*my*x1*zx + my*zx**2 + x1**2*y1 - x1**2*zy - x1*y1*zx + x1*zx*zy + y1**3 - 2*y1**2*zy + y1*zy**2)/(x1**2 - 2*x1*zx + y1**2 - 2*y1*zy + zx**2 + zy**2)
        
        # print(result[0][0])
        # print(result[1][0])
        # print()
        
    return result
"""
def calPXangle(point1,directPoint1,directPoint2):
    x1,y1=point1
    x2,y2=directPoint1
    x3,y3=directPoint2

    #vector1=(x2-x1,y2-y1)
    #vector2=(x3-x1,y3-y1)
    
    #Vsize1=math.sqrt(math.pow(vector1[0],2)+math.pow(vector1[1],2))
    #Vsize2=math.sqrt(math.pow(vector2[0],2)+math.pow(vector2[1],2))
    #print(((vector1[0]*vector2[0])+(vector1[1]*vector2[1]))/(Vsize1/Vsize2))
    #angle=math.acos(((vector1[0]*vector2[0])+(vector1[1]*vector2[1]))/(Vsize1*Vsize2))

    # vectors landmark2 to landmark1, landmark2 to landmark3
    vector1=np.array([x2-x1,y2-y1])
    vector2=np.array([x3-x1,y3-y1])

    # Calculate the angle between the three points
    #vector1size=np.linalg.norm(vector1)
    #vector2size=np.linalg.norm(vector2)
    size=np.linalg.norm(vector1)*np.linalg.norm(vector2)
    if size==0:
        size=0.01
    vectorDot=vector1.dot(vector2)
    angle = math.acos(vectorDot/size)
    degree=math.degrees(angle)

    #return cos,sin
    return math.cos(angle), math.sin(angle), degree
    #return 1,1
"""

def calPXangle(point1,directPoint1,directPoint2):
    # Get the required landmarks coordinates.
    x1, y1 = point1
    x2, y2 = directPoint1
    x3, y3 = directPoint2

    # vectors landmark2 to landmark1, landmark2 to landmark3
    vector1=[x2-x1,y2-y1]
    vector2=[x3-x1,y3-y1]

    # Calculate the angle between the three points
    # vector1size=math.sqrt(math.pow(vector1[0],2)+math.pow(vector1[1],2))
    # vector2size=math.sqrt(math.pow(vector2[0],2)+math.pow(vector2[1],2))
    size=math.sqrt(math.pow(vector1[0],2)+math.pow(vector1[1],2))*math.sqrt(math.pow(vector2[0],2)+math.pow(vector2[1],2))
    vectorDot=(vector1[0]*vector2[0])+(vector1[1]*vector2[1])
    if size==0:
        angle=math.acos(1)
    elif vectorDot/size>1:
        angle=math.acos(0)
    elif vectorDot/size<-1:
        angle=math.acos(0)
    else:
        angle = math.acos(vectorDot/size)
    degree=math.degrees(angle)
    #return cos,sin
    return math.cos(angle), math.sin(angle),degree
    #return 1,1


@jit(nopython=True)
def pointToPx(points,center,xaxis,yaxis,zaxis):
        faceSize=int(points.size/3)     #[x,y,z],[x,y,z],...
        pxPoint = np.zeros((faceSize,2), dtype=np.int0)
        i=0
        for point in points:
            x,z,y=point        #??
            px=x*xaxis[0]-y*yaxis[0]+z*zaxis[0]+center[0] #??
            py=x*xaxis[1]-y*yaxis[1]+z*zaxis[1]+center[1] #??
            pxPoint[i]=(int(px),int(py))
            i+=1

        return pxPoint


def getArea(point1,point2,directPoint):
    distance,side=calculateSidePx(point1,point2)

    cos,sin,_=calPXangle(point1,point2,directPoint)

    zSize=side*abs(sin)
    xySize=side*(((1-(math.sqrt(2)/2))*abs(cos))+(math.sqrt(2)/2))
        
    resultZ=findZpoint(point1,point2,zSize)
    
    distanceZ1,_=calculateSidePx(directPoint,resultZ[0])
    distanceZ2,_=calculateSidePx(directPoint,resultZ[1])
    if distanceZ1 < distanceZ2:
        zx,zy=resultZ[0]
    else:
        zx,zy=resultZ[1]
        
    resultXY=findXYpoint(point1,point2,(zx,zy),xySize)

    if((resultXY[0][0]+resultXY[0][1])>(resultXY[1][0]+resultXY[1][1])):
        xx,xy=resultXY[1]
        yx,yy=resultXY[0]
    else:
        xx,xy=resultXY[0]
        yx,yy=resultXY[1]
    
    #return x-axis,y-axis,z-axis
    return (xx.astype(int), xy.astype(int)),(yx.astype(int), yy.astype(int)),(zx.astype(int), zy.astype(int))

def calculateDistancePx(point1, point2):
    # Get the required landmarks coordinates.
    x1, y1 = point1
    x2, y2 = point2

    # Calculate the distance between the two points
    distance = math.sqrt(math.pow((x2-x1),2)+math.pow((y2-y1),2))
    
    # Check if the distance is less than zero.
    if distance < 0:
        distance=0
    
    return distance