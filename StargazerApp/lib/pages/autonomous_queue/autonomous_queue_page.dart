import 'dart:convert';
import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:stargazer_9000/models/application_bar.dart';
import 'package:stargazer_9000/pages/autonomous_queue/photo_view_page.dart';
import 'package:stargazer_9000/pages/autonomous_queue/reorder_queue_page.dart';
import '../../network/networking.dart';
import '../../pages/autonomous_queue/queue_entry_card.dart';
import '../../models/expandable_fab.dart';
import 'package:path_provider/path_provider.dart' as syspaths;

/// Represents the page that allows viewing the autonomous queue.
class AutonomousPage extends StatefulWidget {
  const AutonomousPage({Key? key, required this.networkController})
      : super(key: key);

  final NetworkController networkController;

  @override
  State<AutonomousPage> createState() => _AutonomousPage();
}

class Queues {
  List<dynamic> current = [];
  List<dynamic> finished = [];
  Queues();
}

class _AutonomousPage extends State<AutonomousPage> {
  late int queueRegisterId, imageRegisterId;
  Queues queues = Queues();

  List<Map<String, dynamic>> modes = [];
  int cardID = 0;

  void updateList(List<dynamic> newList) {
    if (listEquals(newList, queues.current)) {
      print('no change necessary');
    } else {
      widget.networkController
          .Set({'current_queue': newList, 'object_type': 'autonomous_queue'});
      widget.networkController.Get({'object_type': 'autonomous_queue'});
    }
  }

  void updateQueues(dynamic decoded) {
    setState(() {
      queues.current = decoded['current_queue'];
      queues.finished = decoded['finished_queue'];
    });
  }

  Future<void> displayImage(dynamic decoded) async {
    // decoded['image'] is the image
    final appDir = await syspaths.getTemporaryDirectory();
    String path = '${appDir.path}/temp.jpg';
    File file = File(path);
    print('file created');
    String temp = decoded['image'];
    // Convert the string into a list of bytes
    List<int> imageBytes = base64Decode(temp);
    // Write the list of bytes to the file
    await file.writeAsBytes(imageBytes);
    print('file written');
    await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => PhotoViewPage(filepath: path),
      ),
    );
  }

  @override
  void dispose() {
    widget.networkController.deregister(queueRegisterId);
    widget.networkController.deregister(imageRegisterId);
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
    imageRegisterId = widget.networkController
        .register("SET", "processed_image", displayImage);
    queueRegisterId = widget.networkController
        .register("SET", "autonomous_queue", updateQueues);
    widget.networkController.Get({'object_type': 'autonomous_queue'});
  }

  @override
  Widget build(BuildContext context) {
    dynamic childColumn;
    if (queues.current.isEmpty && queues.finished.isEmpty) {
      childColumn = Column();
    } else {
      var finishedCards = queues.finished
          .map((entry) => QueueEntryCard(
              entry: entry,
              finished: true,
              networkController: widget.networkController))
          .toList();
      var currentCards = queues.current
          .map((entry) => QueueEntryCard(entry: entry, finished: false))
          .toList();
      childColumn = SingleChildScrollView(
        child: Column(
          children: finishedCards + currentCards,
        ),
      );
    }
    return Scaffold(
      appBar: ApplicationToolbar(
        background: widget.networkController.isValid()
            ? "assets/images/autonomous_banner.png"
            : "assets/images/red_image.png",
        textColor: Colors.white,
        title: const Text("Autonomous queue"),
        actions: [
          IconButton(
              icon: const Icon(Icons.refresh),
              tooltip: 'Refresh Queue',
              onPressed: () async {
                widget.networkController
                    .Get({'object_type': 'autonomous_queue'});
              }),
        ],
      ),
      body: childColumn,
      floatingActionButton: ExpandableFab(
        color: const Color(0xFF538EA6),
        icon: Icons.create,
        distance: 112.0,
        children: [
          ActionButton(
              color: const Color(0xFF538EA6),
              iconColor: Colors.white,
              onPressed: () {
                // if (queues.current.isNotEmpty || queues.finished.isNotEmpty) {
                //   setState(() {
                //     queues.finished = [];
                //     Map<String, dynamic> temp = {};
                //     temp['current_queue'] = queues.current;
                //     temp['finished_queue'] = queues.finished;
                //     temp['object_type'] = 'autonomous_queue';
                //     widget.networkController.Set(temp);
                //   });
                // }
                print('not implemented');
              },
              icon: const Icon(Icons.clear_all),
              tooltip: "Clear finished queue"),
          ActionButton(
            onPressed: () async {
              updateList(
                await Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => ReorderPage(
                      networkController: widget.networkController,
                      currentQueue: (queues.current.isEmpty
                          ? []
                          : List.from(queues.current)),
                      finishedQueue: (queues.current.isEmpty
                          ? []
                          : List.from(queues.finished)),
                    ),
                  ),
                ),
              );
            },
            color: const Color(0xFF538EA6),
            iconColor: Colors.white,
            icon: const Icon(Icons.compare_arrows_rounded),
            tooltip: "Change current queue",
          ),
        ],
      ),
    );
  }
}
