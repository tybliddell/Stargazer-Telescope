import 'package:flutter/material.dart';

/// A single 'mode' of the telescope
class Mode {
  String name;
  int type;
  String background;
  Color textColor;

  Mode({required this.name, required this.type, required this.background, required this.textColor});
}
