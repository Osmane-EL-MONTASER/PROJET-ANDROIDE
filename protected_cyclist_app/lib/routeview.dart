import 'dart:ffi';

import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:protected_cyclist_app/api/requests.dart';
import 'package:protected_cyclist_app/routeconfig.dart';
import 'package:bottom_drawer/bottom_drawer.dart';

class RouteView extends StatefulWidget {
  final String startAddress;
  final String endAddress;
  final String maxDistance;
  final double epsValue = 0.1;

  const RouteView(
      {super.key,
      required this.startAddress,
      required this.endAddress,
      required this.maxDistance,
      required epsValue});

  @override
  State<RouteView> createState() => _RouteViewState();
}

class _RouteViewState extends State<RouteView> {
  late List<PCARoute> routes;
  late PCARoute selectedRoute;
  late List<LatLng> selectedWaypoints;
  int selectedIndex = 0;

  bool isLoading = false;

  @override
  void initState() {
    super.initState();
    _loadRoutes();
  }

  Future<void> _loadRoutes() async {
    setState(() {
      isLoading = true;
    });

    routes = await fetchRoutes(widget.startAddress, widget.endAddress,
        double.parse(widget.maxDistance), widget.epsValue);
    setState(() {
      selectedRoute = routes[0];
      selectedWaypoints =
          selectedRoute.waypoints.map((e) => LatLng(e[0], e[1])).toList();
      selectedWaypoints.insert(
          0, LatLng(selectedRoute.startPos[1], selectedRoute.startPos[0]));
      selectedWaypoints
          .add(LatLng(selectedRoute.endPos[1], selectedRoute.endPos[0]));
      isLoading = false;
    });
  }

  void _onWaypointsChanged(List<LatLng> waypoints, PCARoute selected) {
    setState(() {
      selectedWaypoints = waypoints;
      selectedRoute = selected;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Vos itinéraires'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
      ),
      body: Center(
        child: isLoading
            ? const CircularProgressIndicator()
            : Stack(
                alignment: Alignment.center,
                children: [
                  SizedBox(
                    width: MediaQuery.of(context).size.width,
                    height: MediaQuery.of(context).size.height - 90,
                    child: FlutterMap(
                      options: MapOptions(
                        center: LatLng(48.8566, 2.3522),
                        zoom: 13.25,
                      ),
                      nonRotatedChildren: [
                        AttributionWidget.defaultWidget(
                          source: 'OpenStreetMap contributors',
                          onSourceTapped: null,
                        ),
                      ],
                      children: [
                        TileLayer(
                          urlTemplate:
                              'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                          userAgentPackageName: 'Secu\'Velo',
                        ),
                        PolylineLayer(
                          polylineCulling: false,
                          polylines: [
                            Polyline(
                              points: selectedWaypoints,
                              color: Colors.black,
                              strokeWidth: 8,
                            ),
                          ],
                        ),
                        MarkerLayer(
                          markers: [
                            Marker(
                                point: LatLng(selectedRoute.startPos[1],
                                    selectedRoute.startPos[0]),
                                width: 64,
                                height: 64,
                                builder: (context) => Image.network(
                                    'https://media.discordapp.net/attachments/699967068275212380/1099328783334506546/image.png?width=289&height=401')),
                            Marker(
                                point: LatLng(selectedRoute.endPos[1],
                                    selectedRoute.endPos[0]),
                                width: 64,
                                height: 64,
                                builder: (context) => Image.network(
                                    'https://media.discordapp.net/attachments/699967068275212380/1099328783334506546/image.png?width=289&height=401')),
                          ],
                        ),
                      ],
                    ),
                  ),
                  RouteConfig(
                    startAddress: widget.startAddress,
                    endAddress: widget.endAddress,
                    routes: routes,
                    selectedWaypoints: selectedWaypoints,
                    onWaypointsChanged: _onWaypointsChanged,
                  ),
                ],
              ),
      ),
    );
  }
}
