import 'package:flutter/material.dart';

class Palette {
  static const MaterialColor color1 = MaterialColor(
    0xff5F7161,
    // 0% comes in here, this will be color picked if no shade is selected when defining a Color property which doesn’t require a swatch.
    <int, Color>{
      50: Color(0xff6f7f71), //10%
      100: Color(0xff7f8d81), //20%
      200: Color(0xff8f9c90), //30%
      300: Color(0xff9faaa0), //40%
      400: Color(0xffafb8b0), //50%
      500: Color(0xffbfc6c0), //60%
      600: Color(0xffcfd4d0), //70%
      700: Color(0xffdfe3df), //80%
      800: Color(0xffeff1ef), //90%
      900: Color(0xffffffff), //100%
    },
  );
  static const MaterialColor color2 = MaterialColor(
      0xff6D8B74,
      <int, Color>{
        50: Color(0xff7c9782), //10%
        100: Color(0xff8aa290), //20%
        200: Color(0xff99ae9e), //30%
        300: Color(0xffa7b9ac), //40%
        400: Color(0xffb6c5ba), //50%
        500: Color(0xffc5d1c7), //60%
        600: Color(0xffd3dcd5), //70%
        700: Color(0xffe2e8e3), //80%
        800: Color(0xfff0f3f1), //90%
        900: Color(0xffffffff), //100%
      }
  );
  static const MaterialColor color3 = MaterialColor(
      0xffEFEAD8,
      <int, Color>{
        50: Color(0xfff1ecdc), //10%
        100: Color(0xfff2eee0), //20%
        200: Color(0xfff4f0e4), //30%
        300: Color(0xfff5f2e8), //40%
        400: Color(0xfff7f5ec), //50%
        500: Color(0xfff9f7ef), //60%
        600: Color(0xfffaf9f3), //70%
        700: Color(0xfffcfbf7), //80%
        800: Color(0xfffdfdfb), //90%
        900: Color(0xffffffff), //100%
      }
  );
  static const MaterialColor color4 = MaterialColor(
      0xffD0C9C0,
      <int, Color>{
        50: Color(0xffd5cec6), //10%
        100: Color(0xffd9d4cd), //20%
        200: Color(0xffded9d3), //30%
        300: Color(0xffe3dfd9), //40%
        400: Color(0xffe8e4e0), //50%
        500: Color(0xffece9e6), //60%
        600: Color(0xfff1efec), //70%
        700: Color(0xfff6f4f2), //80%
        800: Color(0xfffafaf9), //90%
        900: Color(0xffffffff), //100%
      }
  );
} // you can define define int 500 as the default shade and add your lighter tints above and darker tints below.