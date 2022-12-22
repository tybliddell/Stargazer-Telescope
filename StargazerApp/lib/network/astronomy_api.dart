import 'dart:convert';
import 'package:http/http.dart' as http;

const id = '257de4f3-108c-4ecc-8430-b1c13550ae40';
const secret =
    '5a8c2ee018d82da72ebccdc57a9999b5a9f2d117a99ad7b2ebf5650aa25a153709b6f0eac8c8b1da7046be8b714ec1ba14069fb86ef7a5e8c12c3731df1cecdcb4d8c63f17c63dad0cfb0a0bd259be92e0fcbf1162fae831f9d091b0b727764ba97603b3fa6bc7d6836706446eaa126a';

class APIReq {
  static encodeString(str) {
    return base64.encode(utf8.encode(str));
  }

  static Future<http.Response> attemptCurlRequest() {
    return http.get(
      Uri.parse('https://api.astronomyapi.com/api/v2/bodies'),
      headers: {
        'Authorization': 'Basic ' + encodeString('$id:$secret'),
      },
    );
  }
}
