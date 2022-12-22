import 'package:flutter/material.dart';
import 'package:stargazer_9000/network/networking.dart';

/// Represents a single entry in the autonomous queue
class QueueEntryCard extends StatelessWidget {
  Map<String, dynamic> entry;
  bool finished;
  var divisions = ["Potato", "Okay", "Good", "Great"];
  NetworkController? networkController;

  QueueEntryCard({Key? key, required this.entry, required this.finished, this.networkController})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.fromLTRB(16.0, 16.0, 16.0, 0),
      child: ListTile(
        leading: (finished
            ? const Icon(Icons.done_all)
            : const Icon(Icons.star_outline_rounded)),
        onTap: () async {
          if (finished) {
            networkController?.Get({'object_type': 'processed_image', 'finished_id': entry['image_id']});
          } else {
            print('not finished');
          }
        },
        title: Text(
          entry['object_name'],
        ),
        subtitle: (finished
            ? Text(
                "Finished imaging at ${entry['finished_imaging']}, finished processing at ${entry['finished_processing']}\nRA: ${entry['coordinates']['ascension']}, DEC: ${entry['coordinates']['declination']}\n${entry['object_info']}")
            : Text(
                "Dictionary: ${entry['dict']}, estimated to start in ${entry['time_to_start']} seconds, quality: ${divisions[entry['image_quality'].toInt()]}\n${entry['object_info']}")),
        trailing: const Icon(Icons.info_outline),
      ),
    );
  }
}
