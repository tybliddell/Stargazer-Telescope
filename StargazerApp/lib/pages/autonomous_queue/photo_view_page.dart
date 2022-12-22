import 'dart:io';

import 'package:flutter/material.dart';
import 'package:photo_view/photo_view.dart';
import 'package:stargazer_9000/models/application_bar.dart';

class PhotoViewPage extends StatelessWidget {
  final String filepath;

  PhotoViewPage({required this.filepath});

  @override
  Widget build(BuildContext context) {
    print(filepath);
    return Scaffold(
      appBar: ApplicationToolbar(
        background: 
             "assets/images/autonomous_banner.png",
        textColor: Colors.white,
        title: const Text("Photo View"),
      ),
      body: PhotoView(
        imageProvider: FileImage(File(filepath)),
      ),
    );
  }
}
