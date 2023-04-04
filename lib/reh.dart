import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:flutter_webrtc/flutter_webrtc.dart';
import 'package:http/http.dart' as http;

import 'palette.dart';
import 'afterReh.dart';
import 'model/RehItem.dart';

final rehItem = {
  "list": [
    {
      "part": "허리",
      "image": "assets/part/elbowToknee.png",
      "name": "팔꿈치 무릎 맞닿기",
      "time": 90,
    },
    {
      "part": "허리",
      "image": "assets/part/Hamstring.png",
      "name": "햄스트링 스트레칭(좌)",
      "time": 60,
    },
    {
      "part": "허리",
      "image": "assets/part/Hamstring.png",
      "name": "햄스트링 스트레칭(우)",
      "time": 60,
    },
    {
      "part": "고관절",
      "image": "assets/part/gogwanjeol.png",
      "name": "고관절 좌우 풀어주기",
      "time": 60
    },
    {
      "part": "고관절",
      "image": "assets/part/Naejeon.png",
      "name": "내전근 스트레칭(좌)",
      "time": 60,
    },
    {
      "part": "고관절",
      "image": "assets/part/Naejeon.png",
      "name": "내전근 스트레칭(우)",
      "time": 60,
    },
    {
      "part": "무릎",
      "image": "assets/part/Goodmorning.png",
      "name": "굿모닝스쿼트",
      "time": 60,
    },
    {
      "part": "무릎",
      "image": "assets/part/oneLeg.png",
      "name": "한발 서기(좌)",
      "time": 60,
    },
    {
      "part": "무릎",
      "image": "assets/part/oneLeg.png",
      "name": "한발 서기(우)",
      "time": 60,
    },
  ]
};
RehList? rehList;

class Ticker {
  const Ticker();

  Stream<int> tick({required int ticks}) {
    return Stream.periodic(Duration(seconds: 1), (x) => ticks - x).take(ticks);
  }
}

class rehPage extends StatefulWidget {
  final List<RehItem> rehSelectedList;

  const rehPage({
    Key? key,
    required this.rehSelectedList,
  }) : super(key: key);

  @override
  _rehPageState createState() => _rehPageState(rehSelectedList);
}

class _rehPageState extends State<rehPage> {
  int index = 0;
  List<RehItem> rehSelectedList;

  _rehPageState(this.rehSelectedList);

  late int listLength = rehSelectedList.length;

  RTCPeerConnection? _peerConnection;
  final _localRenderer = RTCVideoRenderer();

  late String transformType = rehSelectedList.elementAt(0).name;

  MediaStream? _localStream;

  RTCDataChannelInit? _dataChannelDict;
  RTCDataChannel? _dataChannel;

  bool _inCalling = true;

  late bool _loading = false;

  void _onTrack(RTCTrackEvent event) {
    print("TRACK EVENT: ${event.streams.map((e) => e.id)}, ${event.track.id}");
    if (event.track.kind == "video") {
      print("HERE");
      _localRenderer.srcObject = event.streams[0];
    }
  }

  void _onDataChannelState(RTCDataChannelState? state) {
    switch (state) {
      case RTCDataChannelState.RTCDataChannelClosed:
        print("Camera Closed!!!!!!!");
        break;
      case RTCDataChannelState.RTCDataChannelOpen:
        print("Camera Opened!!!!!!!");
        break;
      default:
        print("Data Channel State: $state");
    }
  }

  Future<bool> _waitForGatheringComplete(_) async {
    print("WAITING FOR GATHERING COMPLETE");
    if (_peerConnection!.iceGatheringState ==
        RTCIceGatheringState.RTCIceGatheringStateComplete) {
      return true;
    } else {
      await Future.delayed(Duration(seconds: 1));
      return await _waitForGatheringComplete(_);
    }
  }

  Future<void> _negotiateRemoteConnection() async {
    return _peerConnection!
        .createOffer()
        .then((offer) {
          return _peerConnection!.setLocalDescription(offer);
        })
        .then(_waitForGatheringComplete)
        .then((_) async {
          var des = await _peerConnection!.getLocalDescription();
          var headers = {
            'Content-Type': 'application/json',
          };
          var request = http.Request(
            'POST',
            Uri.parse(
                'http://192.168.0.100:8080/offer'), // CHANGE URL HERE TO LOCAL SERVER
          );
          request.body = json.encode(
            {
              "sdp": des!.sdp,
              "type": des.type,
              "video_transform": transformType,
            },
          );
          request.headers.addAll(headers);

          http.StreamedResponse response = await request.send();

          String data = "";
          if (response.statusCode == 200) {
            data = await response.stream.bytesToString();
            var dataMap = json.decode(data);
            print(dataMap);
            await _peerConnection!.setRemoteDescription(
              RTCSessionDescription(
                dataMap["sdp"],
                dataMap["type"],
              ),
            );
          } else {
            print(response.reasonPhrase);
          }
        });
  }

  Future<void> _makeCall() async {
    setState(() {
      _loading = true;
    });
    var configuration = <String, dynamic>{
      'sdpSemantics': 'unified-plan',
    };

    //* Create Peer Connection
    if (_peerConnection != null) return;
    _peerConnection = await createPeerConnection(
      configuration,
    );

    _peerConnection!.onTrack = _onTrack;
    // _peerConnection!.onAddTrack = _onAddTrack;

    //* Create Data Channel
    _dataChannelDict = RTCDataChannelInit();
    _dataChannelDict!.ordered = true;
    _dataChannel = await _peerConnection!.createDataChannel(
      "chat",
      _dataChannelDict!,
    );
    _dataChannel!.onDataChannelState = _onDataChannelState;
    // _dataChannel!.onMessage = _onDataChannelMessage;

    final mediaConstraints = <String, dynamic>{
      'audio': true,
      'video': {
        'mandatory': {
          'minWidth':
              '500', // Provide your own width, height and frame rate here
          'minHeight': '500',
          'minFrameRate': '30',
        },
        //'facingMode': 'user',
        'facingMode': 'environment',
        'optional': [],
      }
    };

    try {
      var stream = await navigator.mediaDevices.getUserMedia(mediaConstraints);
      //_mediaDevicesList = await navigator.mediaDevices.enumerateDevices();
      _localStream = stream;
      //_localRenderer.srcObject = _localStream;

      stream.getTracks().forEach((element) {
        _peerConnection!.addTrack(element, stream);
      });

      print("NEGOTIATE");
      await _negotiateRemoteConnection();
    } catch (e) {
      print(e.toString());
    }
    if (!mounted) return;

    setState(() {
      _inCalling = true;
      _loading = false;
    });
  }

  Future<void> _stopCall() async {
    try {
      //await _localStream?.dispose();
      await _dataChannel?.close();
      await _peerConnection?.close();
      _peerConnection = null;
      _localRenderer.srcObject = null;
    } catch (e) {
      print(e.toString());
    }
    setState(() {
      _inCalling = false;
    });
  }

  Future<void> _nextCall() async {
    try {
      //await _localStream?.dispose();
      await _dataChannel?.close();
      await _peerConnection?.close();
      _peerConnection = null;
      _localRenderer.srcObject = null;
    } catch (e) {
      print(e.toString());
    }
    setState(() {
      _inCalling = false;
    });

    _makeCall();
  }

  Future<void> initLocalRenderers() async {
    await _localRenderer.initialize();
  }

  @override
  void initState() {
    super.initState();

    initLocalRenderers();
    _makeCall();
  }

  @override
  Widget build(BuildContext context) {
    final Size size = MediaQuery.of(context).size;

    return Scaffold(
      body: Column(mainAxisAlignment: MainAxisAlignment.end, children: [
        Row(children: [
          Expanded(
            child: IconButton(
              onPressed: () {
                _stopCall();
                Navigator.pop(context);
              },
              icon: Icon(Icons.arrow_circle_left_outlined),
              iconSize: size.height * 0.05,
              color: Palette.color2,
            ),
          ),
          Expanded(flex: 9, child: SizedBox()),
        ]),
        Expanded(
          child: Column(
            children: [
              Expanded(
                  flex: 1,
                  child: Column(children: [
                    Expanded(
                        flex: 1,
                        child: Container(
                            //color: Colors.amber,
                            alignment: Alignment.center,
                            child: Text(
                              '${index + 1}번째 운동 : ' +
                                  rehSelectedList.elementAt(index).name,
                              style: TextStyle(
                                fontSize: size.height * 0.03,
                              ),
                            ))),
                    StreamBuilder(
                        stream: tick(),
                        builder: (context, AsyncSnapshot<int> snapshot) {
                          if (!snapshot.hasData) {
                            return Expanded(flex: 1, child: Container());
                          } else {
                            return Expanded(
                                flex: 1,
                                child: Container(
                                  alignment: Alignment.center,
                                  child: Text(
                                    '남은 시간 : ${snapshot.data}',
                                    style: TextStyle(
                                      fontSize: size.height * 0.02,
                                    ),
                                  ),
                                ));
                          }
                        })
                  ])),
              Expanded(
                  flex: 10,
                  child: Row(children: [
                    Expanded(flex: 1, child: SizedBox()),
                    Expanded(
                        flex: 3,
                        child: Scaffold(
                          body: OrientationBuilder(
                            builder: (context, orientation) {
                              return SafeArea(
                                child: Padding(
                                  padding: const EdgeInsets.all(10),
                                  child: Column(
                                    mainAxisSize: MainAxisSize.min,
                                    children: [
                                      Padding(
                                        padding: const EdgeInsets.all(5),
                                        child: ConstrainedBox(
                                          constraints: BoxConstraints.tightFor(
                                            width: size.width > 500
                                                ? size.width * 0.7
                                                : size.width - 20,
                                            height: size.height > 500
                                                ? size.height * 0.7
                                                : size.height - 20,
                                          ),
                                          // constraints: BoxConstraints(maxHeight: 1000),
                                          child: AspectRatio(
                                            aspectRatio: 1,
                                            child: Stack(
                                              children: [
                                                Positioned.fill(
                                                  child: Container(
                                                    child: _loading
                                                        ? Center(
                                                            child:
                                                                CircularProgressIndicator(
                                                              strokeWidth: 4,
                                                            ),
                                                          )
                                                        : Container(),
                                                  ),
                                                ),
                                                Positioned.fill(
                                                  child: RTCVideoView(
                                                    _localRenderer,
                                                    mirror: true,
                                                  ),
                                                ),
                                              ],
                                            ),
                                          ),
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              );
                            },
                          ),
                        )),
                    Expanded(flex: 1, child: SizedBox()),
                  ])),
            ],
          ),
        ),
      ]),
    );
  }

  Stream<int> tick() async* {
    if (_loading) {
      yield* Stream.empty();
    } else {
      int time = rehSelectedList.elementAt(index).time;
      for (;;) {
        yield time;
        await Future.delayed(const Duration(seconds: 1));
        time--;
        if(time == 0) {
          if(index == listLength - 1){
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => AfterRehPage()),
            );
          }
          else{
            index += 1;
            transformType = rehSelectedList.elementAt(index).name;
            _nextCall();
            break;
          }
        }
      }
    }
  }
}
