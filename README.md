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

## Trouble Shooting
<details>
<summary>WebRTC</summary>

<details>
<summary>개요</summary>

초기 Flutter와 Python의 데이터 상호 전달을 위해 http get/post 통신 및 Flask를 이용하였다. Flutter에서 데이터를 요청하면 Python에서 웹캠 자원을 사용한 후, 웹캠의 영상에 대해 프레임 단위로 AR 처리를 하여 Flask와 Flutter 간 http 통신을 하였다. 이 때, 이미지 통신에 제한되는 부분이 있어 이미지를 base64 String 코드로 인코딩하여 플러터에서 보낸 후, 이를 Flutter에서 디코딩 하는 방식을 사용했었다. 이런 방식으로 진행했을 때, Python에서의 영상 처리 속도에 제한이 있어 초당 5프레임 정도밖에 가져오지 못했다. 따라서 해당 문제점을 피하기 위해 실시간 통신이 가능하며 Latency가 짧은 통신 방식을 이용해야 된다고 판단하였다.
</details>
<details>
<summary>적용</summary>

WebRTC는 앱, 웹에 적합하며 Latency도 짧고, Dart 및 Python에서도 http 통신을 위한 설계가 가능하여 많은 연산량을 가지는 코드를 짜더라도 안정적으로 프레임 단위별 전송이 가능했다. 또한 비디오 프레임에 대한 전송이 원활하여 오디오 프레임에 대한 처리도 가능해졌으며 비디오, 오디오 모두 실시간으로 처리하여 끊김없이 전송하기 때문에 위의 문제를 해결할 수 있었다.
</details>
</details>

<details>
<summary>StreamBuiler</summary>

<details>
<summary>개요</summary>

사용자가 초기 화면에서 운동을 선택한 후, 다음 운동 화면으로 넘겨주는 데이터는 사용자가 선택한 운동 리스트였다. 운동을 진행하는 화면에서 남은 시간과 사용자가 운동하는 모습을 출력해준 뒤, 남은 시간이 0이 되고 나면 다음 운동 화면으로 넘겨줘야 하는데, 위젯 내에서의 dart 언어 사용은 위젯의 State를 설정하는 setState() 외에서는 대부분 사용하지 못하는 경우가 많아 리스트가 아닌 단일 값으로만 화면을 출력하게 되어 조건문과 반복문도 사용하지 못해 화면 변경에 제한이 있었다. 따라서 일정 충족 값을 만족할 때, 스크린은 그대로이고 위젯들만 변경되는 Builder를 찾아 레이아웃을 다시 설계해야 위젯 전환이 부드럽다.
</details>
<details>
<summary>적용</summary>

운동 화면인 reh.dart 파일과 비디오를 송출하는 WebRTC 기반 p2pVideo.dart를 하나로 합쳤다. 변수들을 public으로 설정하는 방법들도 있었으나, 그렇게되면 p2pVideo.dart에 있는 메소드들을 원활하게 사용하기가 어렵게 되어 합치게 되었다. 하나로 합친 dart 파일의 내부에서 운동 순서, 이름, 남은 시간에 대한 정보들을 스스로 일정 충족 값에 해당되면 자동으로 State를 바꿔주는 StreamBuilder를 이용해 설계하였다. 그 후, 비디오 화면에 해당되는 부분은 기존 p2pVideo.dart의 카메라 송출을 요청하는 _makeCall 메소드, 송출 정지를 요청하는 _stopCall 메소드, 이 두 가지를 하나로 합쳐 stop 후 자동으로 다시 make를 하는 _nextCall을 만들었다. StreamBuilder로 바뀐 운동의 남은 시간이 0초가 되면 _nextCall을 호출하는 방식으로 비디오, 오디오를 모두 새로운 값으로 받아와 문제를 해결할 수 있었다.
</details>
</details>

<details>
<summary>Mediapipe 모델 사용 조정</summary>

<details>
<summary>개요</summary>

Mediapipe를 이용해 Natural feature tracking 마커를 생성할 때 Lite 모델을 사용하여도 WebRTC를 이용하여 영상 정보를 주고받을 때 딜레이가 생겼다. 또한 마커가 정확하게 생성되어 tracking이 되지 않아도 가이드가 시작되는 경우가 존재하였다.
</details>
<details>
<summary>적용</summary>

Mediapipe 모델을 불러오는 과정을 매 영상마다가 아닌 클라이언트에서 서버로 WebRTC request에서 track를 생성하는 과정에서 한번 불러오고 동일한 모델을 사용하도록 조정하였다. 또한 Lite 모델의 복잡도를 1에서 0으로 낮췄다. 모델의 복잡도가 낮아지면서 정확도에 문제가 발생하였지만, 테스트 환경에서는 자세추정과 3D 모델 렌더링을 위한 마커 생성에서는 큰 제약이 되지 않았다. 
 마커가 정확하지 않고, 너무 적은 양의 마커만 생성되어 정확성이 의심되는 경우에는 가이드에서 영상을 수정하지 못하도록 제한하였다.
</details>
</details>

<details>
<summary>Audio track 동기화</summary>

<details>
<summary>개요</summary>

WebRTC에서 Audio를 발생시킬 때 영상처리로 분류된 자세별로 음성이 다르게 생성되어 전송되지 않는 경우가 발생하였다. 또한 음성을 준비하여도 음성의 크기, 발음, 빠르기가 손상되어 전송되어 제대로 된 음성 가이드가 나오지 않는 경우가 발생하였다.
</details>
<details>
<summary>적용</summary>

 Audio track 생성 시 Audio Frame으로 보내주는 객체를 생성하여 등록하였고, Audio 선정 시 Flag를 사용하여 상호배제를 구현하였다. 사전에 준비한 .wav 파일의 음성이 22050Hz, channel이 1로 샘플링 된 것을 확인하고, 구현된 WebRTC에서 클라이언트에서 서버로 보내는 Audio Frame이 48000Hz, channel이 2인 것을 확인하였다. 기존의 음원 파일들에서 Audio Frame을 추출하였을 때, 48000Hz, channel이 2인 Audio Frame이 추출되도록 Upsampling, Resampling 과정을 거쳐 준비하였다.
</details>
</details>

<details>
<summary>수학 모델의 근사 오류 수정</summary>

<details>
<summary>개요</summary>

위에 근사 모델을 사용하여 영상에서 3D 모델을 렌더링할 3차원 공간을 생성할 때 연립방정식이 허근을 가지거나(실제 픽셀 값이 나오기에 허근을 가질 수 없다), 수학적인 도메인 에러가 발생하는 경우가 있었다.
</details>
<details>
<summary>적용</summary>

 수학 모델을 간소화하고 Python 라이브러리인 sympy를 이용하여 검산을 실시하였다. 이후에 마커들의 기울기, 왜곡 등이 정상적으로 존재하는 수 있는 경우를 계산하였고, 이외에는 강제로 왜곡 정도를 고정하였다.
</details>
</details>

## Examples
<img src=https://github.com/YUYUJIN/ARReh/blob/main/images/example1.png></img>  
 실제 프로그램 가동 사진  
<img src=https://github.com/YUYUJIN/ARReh/blob/main/images/example2.png></img>  
메인화면  
<img src=https://github.com/YUYUJIN/ARReh/blob/main/images/example3.png></img>
프로그램 동작 화면

## Reference
MediaPipe Pose : https://google.github.io/mediapipe/solutions/pose.html
AR application using python and OpenCV: 
https://github.com/jayantjain100/Augmented-Reality/blob/master/object_module.py  
flutter-webrtc_python-aiortc-opencv : 
https://flutterawesome.com/flutter-webrtc-demo-with-python-server-to-perform-image-processing-on-video-frames-using-opencv/

## Getting Started

This project is a starting point for a Flutter application.

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://docs.flutter.dev/cookbook)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.


