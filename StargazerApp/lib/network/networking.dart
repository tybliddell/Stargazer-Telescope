// ignore_for_file: non_constant_identifier_names
import 'dart:convert';
import 'package:tuple/tuple.dart';
import 'dart:async';
import 'dart:io';

/// Bundles a socket and a multi-subscription stream to allow multiple listeners to the same socket.
/// After creation, init(ip, port) must be called on the object to initialize it.
/// Automatically handles socket errors or closing using the valid flag to communicate any changes.
/// Times out connecting to (ip, port) after 5 seconds.
class SocketStream {
  late Socket socket;
  late StreamController stream;
  late bool valid;

  SocketStream() {
    valid = false;
  }

  init(ip, port) async {
    stream = StreamController.broadcast();
    valid = true;

    // Verify args
    if (ip == "" || port == "") {
      valid = false;
      return;
    }
    try {
      int.parse(port);
    } on FormatException {
      valid = false;
      return;
    }

    print('[status] attempting connection to $ip:$port');
    await Socket?.connect(ip, int.parse(port),
            timeout: const Duration(seconds: 5))
        .then((sock) {
      socket = sock;
      print('[status] connected to: '
          '${sock.remoteAddress.address}:${socket.remotePort}');

      socket.listen((List<int> event) {
        //print("[message]: " +
        //utf8.decode(event).replaceAll('\r\n\r\n', '\\r\\n\\r\\n'));
        stream.add(utf8.decode(event));
      }, onDone: () {
        print('[status] destroying socket');
        valid = false;
        socket.destroy();
      }, onError: (error) {
        valid = false;
        print("[error] error during listening");
      });
    }).catchError(
      (onError) {
        print("[error] could not connect to $ip:$port");
        valid = false;
      },
    );
  }
}

/// The NetworkController handles interfacing with a SocketStream. It allows different pages to 'register' functions to it with a specific
/// request_type and object_type. When the NetworkController receives a message through the SocketStream used in construction, it will invoke all callbacks
/// that match the incoming request_type and object_type. Pages should be sure to deregister with the returned id from register when the
/// page is destroyed.
///
/// The NetworkController allows a simple interface for pages to interact on specific json messages. Multiple NetworkControllers may also be
/// listening to the same SocketStream, allowing for even greater flexibility.
class NetworkController {
  SocketStream socketStream;
  late Map<int, Tuple3<String, String, Function>> callbacks;
  late int id;
  String currentMessage = "";
  NetworkController(this.socketStream) {
    socketStream.stream.stream.listen(onMessage);
    callbacks = {};
    id = 0;
  }

  int register(String request_type, String object_type, Function callback) {
    int next_id = id++;
    callbacks[next_id] =
        Tuple3<String, String, Function>(request_type, object_type, callback);
    return next_id;
  }

  void deregister(int id) {
    callbacks.remove(id);
  }

  bool isValid() {
    return socketStream.valid;
  }

  void onMessage(dynamic socket_message) {
    //decode json
    currentMessage += socket_message;
    if (!currentMessage.endsWith('\r\n\r\n')) return;
    Map<String, dynamic> decoded = jsonDecode(currentMessage);

    //call appropriate handlers
    for (var curr in callbacks.values) {
      if (curr.item1 == decoded['request_type'] &&
          curr.item2 == decoded['object_type']) {
        curr.item3.call(decoded);
      }
    }
    currentMessage = "";
  }

  void Set(Map<String, dynamic> message) {
    message['request_type'] = 'SET';
    message['timestamp'] = DateTime.now().toString();
    socketStream.socket.write(jsonEncode(message) + '\r\n\r\n');
  }

  void Get(Map<String, dynamic> message) {
    message['request_type'] = 'GET';
    message['timestamp'] = DateTime.now().toString();
    socketStream.socket.write(jsonEncode(message) + '\r\n\r\n');
  }

  void Init(Map<String, dynamic> message) {
    message['request_type'] = 'INIT';
    message['timestamp'] = DateTime.now().toString();
    socketStream.socket.write(jsonEncode(message) + '\r\n\r\n');
  }

  void Add(Map<String, dynamic> message) {
    message['request_type'] = 'ADD';
    message['timestamp'] = DateTime.now().toString();
    socketStream.socket.write(jsonEncode(message) + '\r\n\r\n');
  }

  void Remove(Map<String, dynamic> message) {
    message['request_type'] = 'REMOVE';
    message['timestamp'] = DateTime.now().toString();
    socketStream.socket.write(jsonEncode(message) + '\r\n\r\n');
  }
}
