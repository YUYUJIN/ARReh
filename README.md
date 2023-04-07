# ARReh

Flutter로 제작된 웹 앱 형태의 재활치료 가이드이다. AR 요소를 이용하여 가이드를 제공한다.

태블릿, PC에 탑재된 카메라 센서만을 이용할 것이고 기존 ARcore 등의 추가적인 앱이 필요하지 않는 독립적인 AR 웹 앱이다. 사용자는 필요한 운동만을 선택하고 선택된 운동에 대한 가이드가 음성과 영상으로 제공된다.

## Tech Stack
- Flutter && Dart  
 프로젝트의 특성상 초기 모델은 모바일 플랫폼을 이용한 서비스였으나, 사용자의 환경 및 상황을 고려하여 다양한 환경에서 사용이 가능하도록 크로스플랫폼 지원이 되는 Flutter를 선정하게 되었다. Framework를 Flutter로 사용하게 되면서 Dart 또한 같이 사용하였다.
- WebRTC  
<img src=https://github.com/YUYUJIN/ARReh/blob/main/images/WebRTC.png></img>  
 대부분 실시간 화상회의 등으로 많이 사용되는 WebRTC이지만, 해당 프로젝트의 연산량이 상당히 많아 Latency가 짧고 프레임 단위별 결과물을 빠르게 전송시켜줄 수 있는 단순한 추가 서버를 찾고 있었고, 그 결과 위의 장점을 가진 WebRTC를 Flutter와 Python 간의 통신 서버로 사용하였다.
- Mediapipe  
<img src=https://github.com/YUYUJIN/ARReh/blob/main/images/MediapipeIndex.png></img>  
<img src=https://github.com/YUYUJIN/ARReh/blob/main/images/MediapipeGraph.png></img>  
 기존에 고려하였던 Apple사의 body tracking보다 높은 정확도를 제공하면서 Lite모델에 경우에는 실시간성을 보장하면서 빠른 Landmark 생성이 가능한 것을 확인하였다.
 실시간성이 보장되고 정확도가 요구치를 충족하기에 본 작품의 Natural feature tracking의 마커 역할을 Landmark가 충분히 수행할 수 있을 것으로 예상하고 프로젝트를 진행하였다.
- AR application using python and OpenCV  
<img src=https://github.com/YUYUJIN/ARReh/blob/main/images/ARpython.png></img>  
 본 프로젝트는 nature feature tracking 마커를 이용한 AR 콘텐츠 개발이므로 Aruco 마커를 이용한 위 작품과 큰 차이점이 있지만, OpenCV와 Numpy만으로 영상에 3D 모델을 투영시키는 알고리즘을 참고하였다. 
 3D 모델을 투영시킬 때 매쉬(mesh)와 텍스쳐(texture)를 OpenCV와 Numpy를 이용하여 영상에 그린 뒤, 왜곡된 정도를 이용하여 3D 모델의 vertices을 올바른 좌표계로 이동하여 렌더링 시켜야 된다는 것을 확인하였다. 
- Blender  
<img src=https://github.com/YUYUJIN/ARReh/blob/main/images/blender.png></img>  
 Blender를 이용하여 3D 모델을 제작할 수 있었다. 본 프로젝트에서는 Blender로 제작된 .obj 파일과 texture로 사용된 .jpg 파일을 이용하여 vertices, face, vertex, texture를 생성하여 사용하였다.

## Structure
<img src=https://github.com/YUYUJIN/ARReh/blob/main/images/structure.png></img>  
  Flutter에서는 사용자가 운동을 선택하면 선택된 값들을 기반으로 WebRTC에 http 통신을 통한 처리 요청을 발생시킨다. 이후 Audio/Video streaming을 위한 Track을 생성하여 서버에 등록한다. 서버에서 처리한 값들을 다시 받아 Video와 Audio를 사용에게 출력한다.

 Python에서는 Flutter에서 등록한 Track에서 30frames/s로 오는 Video Frame을 OpenCV, Mediapipe을 이용하여 영상처리를 진행한다. 이 결과로 사용자의 자세를 추정하고 3D 모델 투영을 위한 벡터와 공간을 계산한다. 또한 추정한 포즈를 기반으로 사전에 준비한 음원파일(.wav)에서 48000Hz, channel이 2인 Audio Frame을 생성한다. 이후 OpenCV를 이용해 3D 모델을 영상에 렌더링한다. 
 
 최종적으로 새로 수정한 Video Frame과 Audio Frame으로 데이터를 수정하여 Flutter로 전송한다.

## Posture estimation using Mediapipe
<img src=https://github.com/YUYUJIN/ARReh/blob/main/images/postureEstimation.png></img>  
 Mediapipe를 이용하여 추정한 Landmark들을 각각 벡터로 하여 사이각, 거리를 측정할 수 있다. 동작 판단의 기준이 되는 특징을 운동별로 산정하여 운동별 동작의 실행 유무를 판별할 수 있다.

## 3D model rendering using Natural feature tracking marker
  Mediapipe의 결과로 추정한 Landmark들이 정확하고 실시간으로 나온다는 것을 전제로 Natural feature tracking 마커로서 사용한다. Blender로 제작한 3D 모델들의 vertices의 x,y,z 좌표계를 영상의 픽셀 좌표로 변환하기 위해서는 최초의 마커들의 외곡, 기울기들을 이용하여 반영해야한다. 이 때, 사용자의 자세 또한 마커들 사이에 상대거리, 상대 각도를 이용하여 특징을 구하여 자세를 측정한다.  
<img src=https://github.com/YUYUJIN/ARReh/blob/main/images/Markers.png></img>  
  DP(방향 기준 좌표)(붉은 점)와 실제 3D 모델을 그릴 공간을 포함할 마커(초록선)를 추측한다. DP는 하나의 3D 공간을 추측할 때 하나만 사용하는데, 3D 모델을 그릴 때 방향을 DP로 설정한다.  
<img src=https://github.com/YUYUJIN/ARReh/blob/main/images/zEstimation.png></img>  
  근사시킬 Z축 벡터를 구하기 위해 마커 P1에서 P2까지의 거리는 왜곡 되지 않았다고 가정하고 3차원 공간을 정육면체로 근사시킬 것이다. 이 때, 정육면체의 한 변의 길이를 a라고 한다면 마커 P1에서 P2까지의 거리는 이다. 왜곡되어 나타나는 Z축의 길이를 구하기 위해서 왜곡된 정도를 구해야한다. 이 때 왜곡된 정도는 DP와 마커 P1, P2의 사이 각으로 가정한다. 왜곡이 일어지 않을 때는 Z축은 0이 되어야하고 왜곡이 최대일 때는 Z축이 가 되어야한다. Z축의 길이는 양수이기 때문에 로 근사한다.  
<img src=https://github.com/YUYUJIN/ARReh/blob/main/images/equation1.PNG></img>  
  Z축은 벡터 P1->P2에 직교한다고 가정하고, 크기는 위에 구한 크기라고 가정하여 근사한다면 연립방정식[식 1]을 세울 수 있고, 연립 방적식의 근으로 Z축 벡터를 두 개 구할 수 있다. 이때 DP와 가까운 벡터를 구하여 근사시킨 Z축 벡터를 구한다.  
<img src=https://github.com/YUYUJIN/ARReh/blob/main/images/xyEstimation.png></img>  
 Z축 근사에서 사용한 가정은 그대로 사용한다. 이후 왜곡이 없는 경우, X축, Y축에 길이는 가 되어야하고, 왜곡이 최대는 경우에는 가 되어야한다.  따라서 X축, Y축의 길이는 이다.  
<img src=https://github.com/YUYUJIN/ARReh/blob/main/images/equation2.PNG></img>  
 X축의 끝 좌표와 Y축의 끝 좌표를 지나가는 직선은 마커 P1과 P2의 중점을 지나가고 Z축과 평행하다고 가정한다. 직선의 방정식과 마커 P1과의 거리가 축의 길이가 되는 두 점의 방정식으로 연립방정식을 세워 X축과 Y축을 구한다.  
<img src=https://github.com/YUYUJIN/ARReh/blob/main/images/2d3d.png></img>  
 3D 모델이 존재하는 3차원 좌표계를 영상의 2차원 좌표계로 투영하기 위해 3차원 좌표계를 상대크기(0~1)로 고정시킨다. 위에서 구한 X축, Y축, Z축 벡터를 각각 라고 한다. 이를 이용하여 2차원 좌표계의 성분을 3차원 좌표계의 성분으로 분해하면 으로 근사할 수 있다. 이를 이용해 3D 모델의 3차원인 vertex들을 2차원으로 근사시킨다.  
<img src=https://github.com/YUYUJIN/ARReh/blob/main/images/3Dresult.png></img>  
 최종적으로 OpenCV를 이용하여 face들의 vertices를 메쉬(mesh)로 영상에 그린다. texture 또한 이 과정에서 추가한다.

## Audio Guide
 영상에 제공되는 영상 가이드로는 설명하기 힘든 부분이 존재한다. 이를 보완하기 위해 Mediapipe를 이용하여 추정한 운동 자세마다 적절한 음성 가이드를 사용자에게 제공한다. 운동 자세마다 필요한 음성을 .wav파일로 서버에 준비한 상태로 WebRTC에서 audio track을 이용하여 사용자에게 받은 Audio Frame 단위로 수신한 데이터를 전송한다.




## Getting Started

This project is a starting point for a Flutter application.

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://docs.flutter.dev/cookbook)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.
