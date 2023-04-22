import 'package:flutter/material.dart';
import 'routeview.dart';

class PCAppHome extends StatefulWidget {
  const PCAppHome({super.key});

  @override
  State<PCAppHome> createState() => _PCAppHomeState();
}

class _PCAppHomeState extends State<PCAppHome> {
  final ButtonStyle flatButtonStyle = TextButton.styleFrom(
    foregroundColor: Colors.black,
    minimumSize: const Size(88, 44),
    padding: const EdgeInsets.symmetric(horizontal: 16.0),
    shape: const RoundedRectangleBorder(
      borderRadius: BorderRadius.all(Radius.circular(2.0)),
    ),
    backgroundColor: Colors.black12,
  );

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
          const SizedBox(
            width: 300,
            child: TextField(
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Adresse de départ',
              ),
            ),
          ),
          const SizedBox(
            height: 10,
          ),
          const SizedBox(
            width: 300,
            child: TextField(
              decoration: InputDecoration(
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
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const RouteView()),
              );
            },
            child: const Text('Générer l\'itinéraire'),
          )
        ],
      ),
    );
  }
}
