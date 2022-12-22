import 'package:flutter/material.dart';

/// Represents a more diverse appBar for a Scaffold. It can use a custom background, passed by path as a string.
class ApplicationToolbar extends StatelessWidget with PreferredSizeWidget {
  ApplicationToolbar(
      {Key? key,
      required this.background,
      required this.textColor,
      required this.title,
      this.leading,
      this.actions})
      : super(key: key);

  final String background;
  final Color textColor;
  final Text title;
  Widget? leading;
  List<Widget>? actions;

  @override
  Widget build(BuildContext context) {
    return Container(
      child: AppBar(
        actions: actions,
        leading: leading,
        backgroundColor: Colors.transparent,
        shadowColor: Colors.transparent,
        foregroundColor: textColor,
        title: title,
      ),
      decoration: (BoxDecoration(
        image:
            DecorationImage(image: AssetImage(background), fit: BoxFit.cover),
      )),
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);
}
