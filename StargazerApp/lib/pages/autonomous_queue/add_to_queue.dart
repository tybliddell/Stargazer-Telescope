import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:stargazer_9000/pages/autonomous_queue/reorder_queue_page.dart';
import '../../network/networking.dart';

/// Represents the search field for adding new items to the autonomous queue.
class ReorderSearchDelegate extends SearchDelegate {
  ReorderSearchDelegate(this.networkController, this.notifier);
  final NetworkController networkController;
  final ValueNotifier<SearchSuggestions> notifier;
  String lastQuery = '';
  List<bool> showFavorites = [false];

  @override
  Widget? buildLeading(BuildContext context) {
    return null;
  }

  @override
  List<Widget>? buildActions(BuildContext context) {
    return [
      StatefulBuilder(
        builder:
            (BuildContext context, void Function(void Function()) setState) {
          return ToggleButtons(
            selectedColor: const Color(0xFF538EA6),
            onPressed: (int index) {
              if (!showFavorites[0]) {
                networkController.Get(
                  {'object_type': 'favorite_star_list'},
                );
              }
              setState(() {
                showFavorites[index] = !showFavorites[index];
                // ignore: invalid_use_of_visible_for_testing_member, invalid_use_of_protected_member
                notifier.notifyListeners();
              });
            },
            isSelected: showFavorites,
            children: const <Widget>[
              Icon(Icons.star),
            ],
          );
        },
      ),
      const Padding(
        padding: EdgeInsets.all(2),
      ),
      IconButton(
        icon: const Icon(Icons.close),
        tooltip: 'Close',
        onPressed: () {
          query = '';
        },
      ),
    ];
  }

  Widget _buildConfirmEntry(BuildContext context, Map entry, bool favorite) {
    double divisionIndex = 1;
    var divisions = ["Potato", "Okay", "Good", "Great"];
    List<bool> isFav = [favorite];
    return AlertDialog(
      title: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(entry['object_name']),
          StatefulBuilder(builder:
              (BuildContext context, void Function(void Function()) setState) {
            return ToggleButtons(
              selectedColor: const Color(0xFF538EA6),
              onPressed: (int index) {
                if (!isFav[0]) {
                  // Add to favorites
                  networkController.Add(
                    {
                      'object_type': 'favorite_star_list',
                      'star': entry,
                    },
                  );
                } else {
                  networkController.Remove(
                    {
                      'object_type': 'favorite_star_list',
                      'star': entry,
                    },
                  );
                }
                networkController.Get(
                  {'object_type': 'favorite_star_list'},
                );
                setState(() {
                  isFav[index] = !isFav[index];
                  // ignore: invalid_use_of_visible_for_testing_member, invalid_use_of_protected_member
                  notifier.notifyListeners();
                });
              },
              isSelected: isFav,
              children: const <Widget>[
                Icon(Icons.star),
              ],
            );
          })
        ],
      ),
      elevation: 24.0,
      content: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          Text(entry['object_info'] as String),
          const Padding(padding: EdgeInsets.all(16)),
          StatefulBuilder(builder:
              (BuildContext context, void Function(void Function()) setState) {
            return Slider(
              thumbColor: const Color(0xFF538EA6),
              activeColor: const Color(0xFF538EA6),
              max: 3,
              divisions: 3,
              value: divisionIndex,
              label: divisions[divisionIndex.toInt()],
              onChanged: (double value) {
                setState(() {
                  divisionIndex = value;
                });
              },
            );
          })
        ],
      ),
      actions: <Widget>[
        TextButton(
          style: TextButton.styleFrom(primary: const Color(0xFF538EA6)),
          onPressed: () {
            Navigator.of(context).pop(false);
          },
          child: const Text('No'),
        ),
        TextButton(
          style: TextButton.styleFrom(primary: const Color(0xFF538EA6)),
          onPressed: () {
            entry['image_quality'] = divisionIndex.toInt();
            Navigator.of(context).pop(true);
          },
          child: const Text('Yes'),
        )
      ],
    );
  }

  @override
  Widget buildSuggestions(BuildContext context) {
    return buildStarList();
  }

  @override
  Widget buildResults(BuildContext context) {
    return buildStarList();
  }

  Widget buildStarList() {
    // Send request to Python server, and Python server may respond with previously cached response if too quick
    // Do not need to send if in favorite mode
    if (!showFavorites[0]) {
      if (query != lastQuery) {
        networkController.Get(
            {'object_type': 'star_list', 'current_query': query});
        lastQuery = query;
      }
    }

    // Change logic depending on if in favorite mode.
    return ValueListenableBuilder<SearchSuggestions>(
        valueListenable: notifier,
        builder:
            (BuildContext context, SearchSuggestions value, Widget? child) {
          if (!showFavorites[0]) {
            // NON favorites view
            return ListView(
              children: value.suggestions
                  .map<Widget>(
                    (entry) => ListTile(
                      title: Text((entry as Map)['object_name']! as String),
                      onTap: () async {
                        dynamic choice = await showDialog(
                          context: context,
                          builder: (BuildContext context) =>
                              // See if current entry is a favorite
                              _buildConfirmEntry(
                            context,
                            entry,
                            value.favorites.any(
                              (element) => mapEquals(element, entry),
                            ),
                          ),
                        );
                        if (choice.runtimeType != Null && choice) {
                          close(context, entry);
                        }
                      },
                    ),
                  )
                  .toList(),
            );
          } else {
            // favorites view
            return ListView(
                children: value.favorites.map<Widget>((entry) {
              if ((entry as Map)['object_name']
                  .toString()
                  .toLowerCase()
                  .contains(query.toLowerCase())) {
                return ListTile(
                  title: Text((entry)['object_name']! as String),
                  onTap: () async {
                    dynamic choice = await showDialog(
                        context: context,
                        builder: (BuildContext context) =>
                            _buildConfirmEntry(context, entry, true));
                    if (choice.runtimeType != Null && choice) {
                      close(context, entry);
                    }
                  },
                );
              } else {
                return Container();
              }
            }).toList());
          }
        });
  }
}
