import 'package:flutter/material.dart';
import '../../models/mode.dart';
import '../../network/networking.dart';
import '../autonomous_queue/autonomous_queue_page.dart';

/// Display for a mode. Also handles pushing the appropriate page and passing the NetworkController into that new page.
class ModeCard extends StatelessWidget {
  Mode mode;
  NetworkController networkController;
  String? background;
  Color? textColor;

  ModeCard(
      {Key? key,
      required this.mode,
      required this.networkController,
      this.background,
      this.textColor})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(30),
          image: DecorationImage(
              image: (background == null
                  ? const AssetImage('assets/images/transparent_image.png')
                  : AssetImage(background!)),
              fit: BoxFit.cover),
        ),
        child: Card(
          color: Colors.transparent,
          shadowColor: Colors.transparent,
          child: ListTile(
            onTap: () async {
              if (mode.type == 1) {
                // Get current queue
                // Get the current queue
                // build autonomous page
                await Navigator.push(
                  context,
                  MaterialPageRoute(
                      builder: (context) => AutonomousPage(
                            networkController: networkController,
                          )),
                );
                print("[page] returned from autonomous page");
              } else if (mode.type == 2) {
              } else if (mode.type == 3) {}
            },
            title: Padding(
              padding: const EdgeInsets.all(12.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: <Widget>[
                  Text(
                    mode.name,
                    style: TextStyle(
                      fontSize: 17.0,
                      color: (textColor == null ? Colors.black : textColor!),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ));
  }
}
