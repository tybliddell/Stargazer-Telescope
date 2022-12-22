import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:stargazer_9000/network/networking.dart';
import '../network/networking.dart';
import 'home/home_page.dart';

/// Represents the original login page for the app.
class LoginPage extends StatefulWidget {
  const LoginPage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  State<LoginPage> createState() => _LoginPage();
}

class _LoginPage extends State<LoginPage> with TickerProviderStateMixin {
  TextEditingController ipTextController =
      TextEditingController(text: "");
  TextEditingController portTextController =
      TextEditingController(text: "");
  bool isConnecting = false;
  DateTime now = DateTime.now();

  @override
  void dispose() {
    // Clean up the controller when the widget is disposed.
    ipTextController.dispose();
    portTextController.dispose();
    super.dispose();
  }

  /// Used to write the clientID to disk. Acts as a cookie for the client
  Future<void> writeID(dynamic decoded) async {
    // Write the id to disk
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('clientID', decoded['client_id']);
  }

    /// Used to write the clientID to disk. Acts as a cookie for the client
  void writeIPandPort(String ip, String port) async {
    // Write the id to disk
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('loginIP', ip);
    await prefs.setString('loginPort', port);
  }

  void readIPandPort() async {
    if(ipTextController.text == "" && portTextController.text == "") {
      final prefs = await SharedPreferences.getInstance();
      ipTextController.text = prefs.getString('loginIP') ?? "";
      portTextController.text = prefs.getString('loginPort') ?? "";
    }
  }

  Future<void> _connectButton() async {
    SocketStream socketStream = SocketStream();
    await socketStream.init(ipTextController.text, portTextController.text);
    NetworkController networkController = NetworkController(socketStream);

    if (!socketStream.valid) {
      // Error connecting
      showDialog(
          context: context,
          builder: (BuildContext context) => _buildErrorConnectingDialog(
              context, ipTextController.text, portTextController.text));
    } else {
      // send cookie info if present, else send null
      final prefs = await SharedPreferences.getInstance();
      final clientID = prefs.getString('clientID') ?? '';
      networkController.register('INIT', 'client_id', writeID);
      networkController.Init(
          {'object_type': 'client_id', 'client_id': clientID});
      writeIPandPort(ipTextController.text, portTextController.text);
      await Navigator.push(
        context,
        MaterialPageRoute(
            builder: (context) => HomePage(
                  networkController: networkController,
                )),
      );
      print("[page] returned from HomePage");
      socketStream.socket.destroy();
      socketStream.valid = false;
    }
    return;
  }

  Widget _buildErrorConnectingDialog(BuildContext context, ip, port) {
    return AlertDialog(
      title: const Text('Connection error'),
      elevation: 24.0,
      content: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          Text("Could not connect to $ip:$port"),
        ],
      ),
      actions: <Widget>[
        TextButton(
          onPressed: () {
            Navigator.of(context).pop();
          },
          child: const Text('Close'),
        ),
      ],
    );
  }

  Widget _buildREADMEDialog(BuildContext context) {
    return AlertDialog(
      title: const Text('About...'),
      elevation: 24.0,
      content: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: const <Widget>[
          Text("This is a placeholder for instructions or readme"),
        ],
      ),
      actions: <Widget>[
        TextButton(
          onPressed: () {
            Navigator.of(context).pop();
          },
          child: const Text('Close'),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    readIPandPort();
    return MaterialApp(
      home: Container(
        decoration: const BoxDecoration(
            image: DecorationImage(
                image: AssetImage("assets/images/star_bg.jpg"),
                fit: BoxFit.cover)),
        child: Scaffold(
          backgroundColor: Colors.transparent,
          appBar: AppBar(
            title: Text(widget.title),
            backgroundColor: Colors.transparent,
            shadowColor: Colors.blueGrey,
          ),
          body: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Row(
                  children: <Widget>[
                    const Spacer(),
                    Expanded(
                      child: TextField(
                        style: const TextStyle(
                          color: Colors.white,
                          //backgroundColor: Colors.white24
                        ),
                        readOnly: isConnecting,
                        cursorColor: Colors.white,
                        controller: ipTextController,
                        decoration: const InputDecoration(
                          border: UnderlineInputBorder(),
                          labelStyle: TextStyle(color: Colors.white),
                          labelText: 'IP:',
                        ),
                      ),
                      flex: 2,
                    ),
                    const Spacer(),
                    Expanded(
                      child: TextField(
                        style: const TextStyle(color: Colors.white),
                        readOnly: isConnecting,
                        cursorColor: Colors.white,
                        controller: portTextController,
                        decoration: const InputDecoration(
                          border: UnderlineInputBorder(),
                          labelStyle: TextStyle(color: Colors.white),
                          labelText: 'Port:',
                        ),
                      ),
                    ),
                    const Spacer()
                  ],
                ),
                const SizedBox(height: 30),
                isConnecting
                    ? const CircularProgressIndicator(
                        color: Colors.white,
                      )
                    : ElevatedButton(
                        style: ButtonStyle(
                            backgroundColor: MaterialStateProperty.all<Color>(
                                const Color(0xFF538EA6))),
                        onPressed: () async {
                          setState(() => isConnecting = true);
                          await _connectButton();
                          setState(() => isConnecting = false);
                        },
                        child: const Text('Connect!')),
              ],
            ),
          ),
          floatingActionButton: FloatingActionButton(
            onPressed: () {
              showDialog(
                  context: context,
                  builder: (BuildContext context) =>
                      _buildREADMEDialog(context));
            },
            tooltip: 'Read',
            backgroundColor: const Color(0xFF538EA6),
            child: const Icon(Icons.book),
          ),
        ),
      ),
    );
  }
}
