import 'dart:convert';
import 'dart:typed_data';

import 'package:http/http.dart' as http;
import 'dart:convert' show utf8;

class PCARoute {
  final List<List<dynamic>> waypoints;
  final double distance;
  final int time;
  final List<double> startPos;
  final List<double> endPos;
  final double distance2;
  final double distance3;
  final double distance4;

  PCARoute({
    required this.waypoints,
    required this.distance,
    required this.time,
    required this.startPos,
    required this.endPos,
    required this.distance2,
    required this.distance3,
    required this.distance4,
  });
}

Future<List<PCARoute>> fetchRoutes(
    String startAddress, String endAddress, double maxDistance, double epsValue) async {
  final response = await http.get(
      Uri.parse(
          'http://127.0.0.1:5000/protected_cyclist_api/route?start_address=$startAddress&end_address=$endAddress&max_distance=$maxDistance&eps=$epsValue'),
      headers: {'Content-Type': 'application/json; charset=utf-8'});

  if (response.statusCode == 200) {
    final jsonResponse = json.decode(response.body);
    final jsonRouteList = jsonResponse['route'] as List;
    final startPos = List<double>.from(jsonResponse['start_pos']);
    final endPos = List<double>.from(jsonResponse['end_pos']);

    return jsonRouteList.map((jsonRoute) {
      final jsonWaypoints = jsonRoute['waypoints'] as List;
      final waypoints = jsonWaypoints.map((waypoint) {
        return [waypoint[0].toDouble(), waypoint[1].toDouble()];
      }).toList();
      return PCARoute(
        waypoints: waypoints,
        distance: jsonRoute['distance'].toDouble(),
        distance2: jsonRoute['distance2'].toDouble(),
        distance3: jsonRoute['distance3'].toDouble(),
        distance4: jsonRoute['distance4'].toDouble(),
        time: jsonRoute['time'],
        startPos: startPos,
        endPos: endPos,
      );
    }).toList();
  } else {
    throw Exception('Failed to load route');
  }
}
