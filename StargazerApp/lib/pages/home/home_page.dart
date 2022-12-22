import 'package:flutter/material.dart';
import 'package:stargazer_9000/models/application_bar.dart';
import '../../network/networking.dart';
import 'photo_mode.dart';
import '../../models/mode.dart';

/// Represents the homepage of the app. Displays all of the different telescope modes using a GridView of ModeCards.
class HomePage extends StatefulWidget {
  const HomePage({Key? key, required this.networkController}) : super(key: key);

  final NetworkController networkController;

  @override
  State<HomePage> createState() => _HomePage();
}

class _HomePage extends State<HomePage> {
  late int registerId;
  List<Mode> modes = [
    Mode(
      name: "Autonomous Mode",
      type: 1,
      background: "assets/images/autonomous_widget.png",
      textColor: Colors.white,
    ),
    Mode(
      name: "Under Development",
      type: 2,
      background: "assets/images/nothing_here.png",
      textColor: Colors.black,
    ),
  ];

  @override
  void dispose() {
    //widget.networkController.deregister(registerId);
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
    registerId = 0;
    //registerId = widget.networkController.register("GET", "autonomous_queue", someFunc);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: ApplicationToolbar(
        textColor: Colors.white,
        background: widget.networkController.isValid()
            ? "assets/images/default_banner.png"
            : "assets/images/red_image.png",
        title: const Text("Telescope mode selection"),
      ),
      body: GridView.count(
        crossAxisCount: 2,
        crossAxisSpacing: 10,
        mainAxisSpacing: 10,
        padding: const EdgeInsets.all(10),
        children: modes
            .map((mode) => ModeCard(
                  mode: mode,
                  networkController: widget.networkController,
                  background: mode.background,
                  textColor: mode.textColor,
                ))
            .toList(),
      ),
    );
  }
}
