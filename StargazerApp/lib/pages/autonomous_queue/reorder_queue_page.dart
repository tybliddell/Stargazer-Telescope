import 'package:flutter/material.dart';
import 'package:stargazer_9000/models/application_bar.dart';
import 'package:stargazer_9000/network/networking.dart';
import '../../models/expandable_fab.dart';
import 'add_to_queue.dart';

/// Represents the reordering page for the autonomous queue mode.
class ReorderPage extends StatefulWidget {
  const ReorderPage({
    Key? key,
    required this.networkController,
    required this.currentQueue,
    required this.finishedQueue,
  }) : super(key: key);

  final NetworkController networkController;
  final List<Map<String, dynamic>> currentQueue;
  final List<Map<String, dynamic>> finishedQueue;

  @override
  State<ReorderPage> createState() => _ReorderPage();
}

class SearchSuggestions {
  SearchSuggestions();
  List<dynamic> suggestions = [];
  List<dynamic> favorites = [];
}

class _ReorderPage extends State<ReorderPage> {
  int cardID = 0;
  late int suggestionsId, favoritesId;
  late List<dynamic> startingQueue;
  late SearchSuggestions searchSuggestions;
  late ReorderSearchDelegate searchDelegate;

  // The ValueNotifier is used to notify the ReorderSearchDelegate to rebuild.
  // This must happen otherwise the delegate's view is one step behind the internal data.
  late ValueNotifier<SearchSuggestions> notifier;

  // Callback for when the ReorderableListView has changed.
  void reorderData(int oldindex, int newindex) {
    setState(() {
      if (newindex > oldindex) {
        newindex -= 1;
      }
      final items = widget.currentQueue.removeAt(oldindex);
      widget.currentQueue.insert(newindex, items);
    });
  }

  void updateSuggestions(Map<String, dynamic> decoded) {
    notifier.value.suggestions = (decoded['stars'] as List);
    // ignore: invalid_use_of_visible_for_testing_member, invalid_use_of_protected_member
    notifier.notifyListeners();
  }

  void updateFavorites(Map<String, dynamic> decoded) {
    searchSuggestions.favorites = (decoded['stars'] as List);
    // ignore: invalid_use_of_visible_for_testing_member, invalid_use_of_protected_member
    notifier.notifyListeners();
  }

  @override
  void dispose() {
    super.dispose();
    widget.networkController.deregister(suggestionsId);
    widget.networkController.deregister(favoritesId);
  }

  @override
  void initState() {
    super.initState();
    searchSuggestions = SearchSuggestions();
    notifier = ValueNotifier<SearchSuggestions>(searchSuggestions);
    searchDelegate = ReorderSearchDelegate(widget.networkController, notifier);
    suggestionsId = widget.networkController
        .register("SET", "star_list", updateSuggestions);
    favoritesId = widget.networkController
        .register("SET", "favorite_star_list", updateFavorites);
    startingQueue = List.from(widget.currentQueue);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: ApplicationToolbar(
        leading: IconButton(
          onPressed: () {
            ScaffoldMessenger.of(context).removeCurrentSnackBar();
            Navigator.of(context).pop(startingQueue);
          },
          icon: const Icon(Icons.arrow_back),
        ),
        title: const Text('Reordering...'),
        background: widget.networkController.isValid()
            ? "assets/images/autonomous_banner.png"
            : "assets/images/red_image.png",
        textColor: Colors.white,
      ),
      body: ReorderableListView(
        onReorder: reorderData,
        children: [
          for (var item in widget.currentQueue)
            Dismissible(
                background: Container(color: Colors.red),
                key: ValueKey(cardID++),
                child: ListTile(
                    title: Text(item['object_name']),
                    subtitle: Text(
                        "Quality: ${item['image_quality']}\n${item['object_info']}"),
                    trailing: const Icon(Icons.reorder)),
                onDismissed: (direction) {
                  var delIndex = widget.currentQueue.indexOf(item);
                  setState(() {
                    widget.currentQueue.remove(item);
                  });
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      backgroundColor: const Color(0xFF538EA6),
                      content: Text("Task ${item['object_info']} deleted",
                          style: const TextStyle(color: Colors.white)),
                      action: SnackBarAction(
                        textColor: Colors.white,
                        label: 'Undo',
                        onPressed: () {
                          if (mounted) {
                            setState(() {
                              widget.currentQueue.insert(delIndex, item);
                            });
                          }
                        },
                      ),
                    ),
                  );
                }),
        ],
        buildDefaultDragHandles: true,
      ),
      floatingActionButton: ExpandableFab(
        color: const Color(0xFF538EA6),
        icon: Icons.create,
        distance: 112.0,
        children: [
          // ADD button
          ActionButton(
            icon: const Icon(Icons.add),
            iconColor: Colors.white,
            tooltip: 'Add',
            color: const Color(0xFF538EA6),
            onPressed: () async {
              // Wait for ReorderSearchDelegate to finish.
              dynamic temp = await showSearch(
                context: context,
                delegate: searchDelegate,
              );
              // Update state based on chosen option
              if (temp != null) {
                setState(() {
                  widget.currentQueue.add(temp);
                });
              }
            },
          ),
          // CONFIRM button
          ActionButton(
            icon: const Icon(Icons.check),
            iconColor: Colors.white,
            color: const Color(0xFF538EA6),
            tooltip: 'Confirm',
            onPressed: () {
              ScaffoldMessenger.of(context).removeCurrentSnackBar();
              Navigator.of(context).pop(widget.currentQueue);
            },
          )
        ],
      ),
    );
  }
}
