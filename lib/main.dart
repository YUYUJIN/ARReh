import 'package:flutter/material.dart';

import 'palette.dart';
import 'reh.dart';
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

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '재활운동 선택',
      theme: ThemeData(
        primarySwatch: Palette.color1,
      ),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {

  const MyHomePage({
    Key? key,
  }) : super(key: key);

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  // 리스트뷰 부위 선택 항목
  final List<String> _partList = ['전체', '허리', '고관절', '무릎'];

  final int listLength = rehItem.values.first.length;

  late List<bool> selectedList;

  final List<RehItem> rehSelectedList = <RehItem>[];

  final List<RehItem> rehSelectedPart = <RehItem>[];

  final List<String> rehSelectedName = <String>[];

  bool isListviewSelected = false;

  void initializeSelection() {
    selectedList = List<bool>.generate(listLength, (_) => false);
  }

  void _toggle(int index) {
    setState(() {
      if (rehSelectedPart.elementAt(index).part == '고관절' &&
          isListviewSelected) {
        index += 3;
      } else if (rehSelectedPart.elementAt(index).part == '무릎' &&
          isListviewSelected) {
        index += 6;
      }
    });
    if (!selectedList[index]) {
      if (index == 1 || index == 4 || index == 7) {
        rehSelectedList.add(rehList!.list!.elementAt(index));
        rehSelectedList.add(rehList!.list!.elementAt(index + 1));
      } else if (index == 2 || index == 5 || index == 8) {
        rehSelectedList.add(rehList!.list!.elementAt(index - 1));
        rehSelectedList.add(rehList!.list!.elementAt(index));
      } else {
        rehSelectedList.add(rehList!.list!.elementAt(index));
      }
    }
  }

  @override
  void initState() {
    super.initState();
    initializeSelection();
  }

  @override
  void dispose() {
    selectedList.clear();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final Size size = MediaQuery.of(context).size;
    rehList = RehList.fromJson(rehItem);

    return Scaffold(
      appBar: AppBar(
        title: Text('재활 부위 및 운동 선택'),
      ),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          Expanded(
            flex: 8,
            child: Row(
              children: [
                Expanded(
                    flex: 2,
                    child: Column(
                      children: [
                        Expanded(child: SizedBox()),
                        Expanded(
                            child: ListView.builder(
                                itemCount: _partList.length,
                                itemBuilder: (context, index) {
                                  return Card(
                                      child: ListTile(
                                    title: Text(
                                      _partList[index],
                                      style: TextStyle(
                                          fontSize: size.height * 0.018),
                                    ),
                                    onTap: () {
                                      setState(() {
                                        rehSelectedPart.clear();
                                        if (_partList[index] == '전체') {
                                          isListviewSelected = false;
                                          for (int i = 0; i < listLength; i++) {
                                            rehSelectedPart.add(
                                                rehList!.list!.elementAt(i));
                                          }
                                        } else {
                                          isListviewSelected = true;
                                          for (int i = 0; i < listLength; i++) {
                                            if (rehList!.list!
                                                    .elementAt(i)
                                                    .part ==
                                                _partList[index]) {
                                              rehSelectedPart.add(
                                                  rehList!.list!.elementAt(i));
                                            }
                                          }
                                        }
                                      });
                                    },
                                  ));
                                })),
                        Expanded(child: SizedBox()),
                      ],
                    )),
                Expanded(
                  flex: 8,
                  child: Column(
                    children: [
                      Expanded(
                        flex: 1,
                        child: Center(
                            child: Text(
                          '운동 선택',
                          style: TextStyle(fontSize: size.height * 0.04),
                        )),
                      ),
                      Expanded(
                        flex: 4,
                        child: GridView.builder(
                            itemCount: rehSelectedPart.length,
                            gridDelegate:
                                const SliverGridDelegateWithMaxCrossAxisExtent(
                              maxCrossAxisExtent: 300,
                              crossAxisSpacing: 10,
                              mainAxisSpacing: 10,
                              childAspectRatio: 1 / 1.2,
                            ),
                            itemBuilder: (BuildContext context, int index) {
                              return InkWell(
                                onTap: () {
                                  _toggle(index);
                                  rehSelectedName.clear();
                                  for (int i=0; i<rehSelectedList.length; i++){
                                    rehSelectedName.add(rehSelectedList.elementAt(i).name);
                                  }
                                },
                                child: GridTile(
                                    child: Container(
                                        child: Column(children: [
                                  Image.asset(
                                    rehSelectedPart.elementAt(index).image,
                                  ),
                                  SizedBox(height: size.height * 0.01),
                                  Text(rehSelectedPart.elementAt(index).name),
                                ]))),
                              );
                            }),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            flex: 1,
            child: Container(
              color: Palette.color4,
              child: Row(children: <Widget>[
                SizedBox(width: size.width * 0.02),
                Text("선택된 항목",
                    style: TextStyle(
                      fontSize: size.height * 0.02,
                    )),
                SizedBox(width: size.width * 0.01),
                Expanded(
                  flex: 13,
                  child: Text(
                    '$rehSelectedName',
                    style: TextStyle(
                      fontSize: size.height * 0.02,
                    ),
                  ),
                ),
                TextButton(
                  child: Text('Clear', style: TextStyle(fontSize: size.height * 0.02),),
                  onPressed: () {
                    setState((){
                      rehSelectedList.clear();
                      rehSelectedName.clear();
                    });
                  },
                ),
                Expanded(
                  child: IconButton(
                    onPressed: () async {
                      if(rehSelectedList.isNotEmpty) {
                        await Navigator.push(
                          context,
                          MaterialPageRoute(
                              builder: (context) =>
                                  rehPage(
                                    rehSelectedList: rehSelectedList,
                                  )),
                        );
                      }
                      else {
                        null;
                      }
                    },
                    icon: Icon(Icons.arrow_circle_right),
                    iconSize: size.height * 0.07,
                    color: Palette.color2,
                  ),
                )
              ]),
            ),
          ),
        ],
      ),
    );
  }

  Color getColor(Set<MaterialState> states) {
    const Set<MaterialState> interactiveStates = <MaterialState>{
      MaterialState.pressed,
      MaterialState.hovered,
      MaterialState.focused,
    };
    if (states.any(interactiveStates.contains)) {
      return Palette.color1;
    }
    return Palette.color2;
  }
}
