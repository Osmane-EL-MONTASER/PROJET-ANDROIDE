import 'package:flutter/material.dart';
import 'api/requests.dart';
import 'routeview.dart';

class PCAppHome extends StatefulWidget {
  const PCAppHome({super.key});

  @override
  State<PCAppHome> createState() => _PCAppHomeState();
}

class _PCAppHomeState extends State<PCAppHome> {
  final ButtonStyle flatButtonStyle = TextButton.styleFrom(
    foregroundColor: Colors.white,
    minimumSize: const Size(88, 44),
    padding: const EdgeInsets.symmetric(horizontal: 16.0),
    shape: const RoundedRectangleBorder(
      borderRadius: BorderRadius.all(Radius.circular(2.0)),
    ),
    backgroundColor: Color.fromARGB(35, 0, 0, 0),
  );

  final TextEditingController _startAddressController = TextEditingController();
  final TextEditingController _endAddressController = TextEditingController();

  @override
  void dispose() {
    _startAddressController.dispose();
    _endAddressController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Image.network(
            'https://media.discordapp.net/attachments/699967068275212380/1098708155397058621/logo.PNG?width=622&height=492',
            width: 64,
            height: 64,
          ),
          const Text('Sécu\'Vélo',
              style: TextStyle(fontSize: 48, fontFamily: 'RaleWay')),
          const SizedBox(
            height: 100,
          ),
          SizedBox(
            width: 300,
            child: TextField(
              controller: _startAddressController,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Adresse de départ',
              ),
            ),
          ),
          const SizedBox(
            height: 10,
          ),
          SizedBox(
            width: 300,
            child: TextField(
              controller: _endAddressController,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Adresse d\'arrivée',
              ),
            ),
          ),
          const SizedBox(
            height: 25,
          ),
          TextButton(
            style: flatButtonStyle,
            onPressed: () {
              if (_startAddressController.text.isNotEmpty &&
                  _endAddressController.text.isNotEmpty) {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                      builder: (context) => RouteView(
                          startAddress: _startAddressController.text,
                          endAddress: _endAddressController.text)),
                );
              }
            },
            child: const Text('Générer l\'itinéraire'),
          )
        ],
      ),
    );
  }
}