import 'package:bottom_drawer/bottom_drawer.dart';
import 'package:flutter/material.dart';
import 'package:protected_cyclist_app/api/requests.dart';
import 'package:latlong2/latlong.dart';

class RouteConfig extends StatefulWidget {
  final String startAddress;
  final String endAddress;

  final List<PCARoute> routes;
  late List<LatLng> selectedWaypoints;
  final void Function(List<LatLng>, PCARoute) onWaypointsChanged;

  RouteConfig(
      {super.key,
      required this.startAddress,
      required this.endAddress,
      required this.routes,
      required this.selectedWaypoints,
      required this.onWaypointsChanged});

  @override
  _RouteConfigState createState() => _RouteConfigState();
}

class _RouteConfigState extends State<RouteConfig> {
  /// create a bottom drawer controller to control the drawer.
  BottomDrawerController controller = BottomDrawerController();
  late PCARoute selectedRoute;
  int selectedIndex = 0;

  @override
  void initState() {
    super.initState();
    selectedRoute = widget.routes[0];
  }

  void _nextRoute() {
    List<LatLng> selectedWaypoints = [];

    setState(() {
      if (selectedIndex == widget.routes.length - 1) {
        selectedIndex = 0;
      } else {
        selectedIndex++;
      }

      selectedRoute = widget.routes[selectedIndex];
      selectedWaypoints =
          selectedRoute.waypoints.map((e) => LatLng(e[0], e[1])).toList();
      selectedWaypoints.insert(
          0, LatLng(selectedRoute.startPos[1], selectedRoute.startPos[0]));
      selectedWaypoints
          .add(LatLng(selectedRoute.endPos[1], selectedRoute.endPos[0]));
    });

    widget.onWaypointsChanged(selectedWaypoints, selectedRoute);
  }

  void _previousRoute() {
    List<LatLng> selectedWaypoints = [];

    setState(() {
      if (selectedIndex == 0) {
        selectedIndex = widget.routes.length - 1;
      } else {
        selectedIndex--;
      }

      selectedRoute = widget.routes[selectedIndex];
      selectedWaypoints =
          selectedRoute.waypoints.map((e) => LatLng(e[0], e[1])).toList();
      selectedWaypoints.insert(
          0, LatLng(selectedRoute.startPos[1], selectedRoute.startPos[0]));
      selectedWaypoints
          .add(LatLng(selectedRoute.endPos[1], selectedRoute.endPos[0]));
    });

    widget.onWaypointsChanged(selectedWaypoints, selectedRoute);
  }

  final ButtonStyle flatButtonStyle = TextButton.styleFrom(
    foregroundColor: Colors.white,
    minimumSize: const Size(44, 28),
    padding: const EdgeInsets.symmetric(horizontal: 16.0),
    shape: const RoundedRectangleBorder(
      borderRadius: BorderRadius.all(Radius.circular(2.0)),
    ),
    backgroundColor: const Color.fromARGB(25, 255, 255, 255),
  );

  @override
  Widget build(BuildContext context) {
    return BottomDrawer(
      /// your customized drawer header.
      header: const Padding(
        padding: EdgeInsets.all(16.0),
        child: Text(
          'Informations sur vos trajets',
          style: TextStyle(
              fontSize: 28, color: Colors.white, fontFamily: 'Raleway'),
        ),
      ),

      /// your customized drawer body.
      body: SizedBox(
        width: MediaQuery.of(context).size.width * 0.95,
        child: Column(
          children: [
            const Divider(
              color: Colors.white,
              height: 8.0,
              indent: 5,
              endIndent: 5,
            ),
            Padding(
              padding: const EdgeInsets.only(top: 16.0),
              child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    Text(
                      'Départ : ${widget.startAddress}',
                      style: const TextStyle(
                          fontSize: 16,
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontFamily: 'Raleway'),
                    ),
                    Text(
                      'Arrivée : ${widget.endAddress}',
                      style: const TextStyle(
                          fontSize: 16,
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontFamily: 'Raleway'),
                    )
                  ]),
            ),
            Padding(
              padding: const EdgeInsets.only(top: 32.0),
              child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    Text(
                      '${selectedRoute.time} secondes',
                      style: const TextStyle(
                          fontSize: 16,
                          color: Colors.white,
                          fontFamily: 'Raleway'),
                    ),
                    Text(
                      '${selectedRoute.distance} km',
                      style: const TextStyle(
                          fontSize: 16,
                          color: Colors.white,
                          fontFamily: 'Raleway'),
                    )
                  ]),
            ),
            Padding(
              padding: const EdgeInsets.only(top: 32.0),
              child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    ElevatedButton(
                      onPressed: _previousRoute,
                      style: flatButtonStyle,
                      child: const Icon(Icons.skip_previous),
                    ),
                    ElevatedButton(
                      onPressed: _nextRoute,
                      style: flatButtonStyle,
                      child: const Icon(Icons.skip_next),
                    ),
                  ]),
            ),
          ],
        ),
      ),

      /// your customized drawer header height.
      headerHeight: 65,

      /// your customized drawer body height.
      drawerHeight: MediaQuery.of(context).size.height * 0.35,

      /// drawer background color.
      color: const Color.fromARGB(245, 45, 45, 45),

      /// drawer controller.
      controller: controller,
    );
  }
}
