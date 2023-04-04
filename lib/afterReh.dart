import 'package:flutter/material.dart';

import 'main.dart';

class AfterRehPage extends StatelessWidget {
  Widget build(BuildContext context) {
    final Size size = MediaQuery.of(context).size;

    return Scaffold(
      body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                ' - 수고하셨습니다 - ',
                style: TextStyle(
                  fontSize: size.height * 0.02,
                ),
              ),
              OutlinedButton(
                  onPressed: () async {
                    await Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => MyHomePage()),
                    );
                  },
                  child: Text(
                    ' Go to Home ',
                    style: TextStyle(
                      fontSize: size.height * 0.02,
                    ),
                  ),
              ),
            ],
      )),
    );
  }
}
