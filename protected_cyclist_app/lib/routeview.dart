import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

class RouteView extends StatefulWidget {
  const RouteView({super.key});

  @override
  State<RouteView> createState() => _RouteViewState();
}

class _RouteViewState extends State<RouteView> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Votre itinéraire'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
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
                        points: [
                          LatLng(48.898191, 2.3860098),
                          LatLng(48.8976299, 2.3854683),
                          LatLng(48.898265, 2.3857381),
                          LatLng(48.898191, 2.3860098),
                          LatLng(48.8988746, 2.3832761),
                          LatLng(48.898265, 2.3857381),
                          LatLng(48.8989354, 2.3825564),
                          LatLng(48.8988746, 2.3832761),
                          LatLng(48.8989015, 2.3810565),
                          LatLng(48.8989354, 2.3825564),
                          LatLng(48.8988769, 2.3798375),
                          LatLng(48.8989015, 2.3810565),
                          LatLng(48.8988446, 2.3781333),
                          LatLng(48.8988769, 2.3798375),
                          LatLng(48.898809, 2.3764127),
                          LatLng(48.8988446, 2.3781333),
                          LatLng(48.898806, 2.3762704),
                          LatLng(48.898809, 2.3764127),
                          LatLng(48.8988036, 2.3761536),
                          LatLng(48.898806, 2.3762704),
                          LatLng(48.8987637, 2.3742284),
                          LatLng(48.8988036, 2.3761536),
                          LatLng(48.8987612, 2.3741172),
                          LatLng(48.8987637, 2.3742284),
                          LatLng(48.8987594, 2.3740003),
                          LatLng(48.8987612, 2.3741172),
                          LatLng(48.8987106, 2.3713465),
                          LatLng(48.8987594, 2.3740003),
                          LatLng(48.8987244, 2.3711722),
                          LatLng(48.8987106, 2.3713465),
                          LatLng(48.898724, 2.3703361),
                          LatLng(48.8987244, 2.3711722),
                          LatLng(48.8987236, 2.3702433),
                          LatLng(48.898724, 2.3703361),
                          LatLng(48.8987233, 2.3701562),
                          LatLng(48.8987236, 2.3702433),
                          LatLng(48.8986969, 2.3683735),
                          LatLng(48.8987233, 2.3701562),
                          LatLng(48.898659, 2.366707),
                          LatLng(48.8986969, 2.3683735),
                          LatLng(48.8986568, 2.3665541),
                          LatLng(48.898659, 2.366707),
                          LatLng(48.8986414, 2.3656145),
                          LatLng(48.8986568, 2.3665541),
                          LatLng(48.8986184, 2.3643165),
                          LatLng(48.8986414, 2.3656145),
                          LatLng(48.8986147, 2.364145),
                          LatLng(48.8986184, 2.3643165),
                          LatLng(48.8985877, 2.3629046),
                          LatLng(48.8986147, 2.364145),
                          LatLng(48.8985716, 2.3611003),
                          LatLng(48.8985877, 2.3629046),
                          LatLng(48.8985444, 2.3595365),
                          LatLng(48.8985716, 2.3611003),
                          LatLng(48.8985372, 2.3593709),
                          LatLng(48.8985444, 2.3595365),
                          LatLng(48.8985244, 2.3590203),
                          LatLng(48.8985372, 2.3593709)
                        ],
                        color: Colors.black,
                        strokeWidth: 8,
                      ),
                    ],
                  ),
                  MarkerLayer(
                    markers: [
                      Marker(
                          point: LatLng(48.898191, 2.3860098),
                          width: 64,
                          height: 64,
                          builder: (context) => Image.network(
                              'https://media.discordapp.net/attachments/699967068275212380/1099328783334506546/image.png?width=289&height=401')),
                      Marker(
                          point: LatLng(48.8985372, 2.3593709),
                          width: 64,
                          height: 64,
                          builder: (context) => Image.network(
                              'https://media.discordapp.net/attachments/699967068275212380/1099328783334506546/image.png?width=289&height=401')),
                    ],
                  ),
                ],
              ),
            )
          ],
        ),
      ),
    );
  }
}
