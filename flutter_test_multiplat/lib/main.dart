import 'package:flutter/material.dart';
import 'package:flutter_test_multiplat/graphs/graph.dart';
import 'package:flutter_test_multiplat/graphs/node.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Projet ANDROIDE - Cyclistes Protégés',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(title: 'Projet ANDROIDE'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  Graph graph = Graph();
  Node n1 = Node(label: 'intersec1');
  Node n2 = Node(label: 'intersec2');
  Node n3 = Node(label: 'intersec3');
  Node n4 = Node(label: 'intersec4');

  _MyHomePageState() {
    graph.addNode(n1);
    graph.addNode(n2);
    graph.addNode(n3);
    graph.addNode(n4);

    graph.addEdgeFromTo(n1, n3, 7.0, label: 'Rue des rues');
  }

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'You have pushed the button this many times:',
            ),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ),
    );
  }
}
