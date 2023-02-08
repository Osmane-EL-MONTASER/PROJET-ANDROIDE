import 'package:flutter_test_multiplat/graphs/node.dart';

class Edge {
  late String _label;
  late double _weight;
  late Node _from;
  late Node _to;

  Edge(
      {required Node from,
      required Node to,
      required String label,
      required double weight}) {
    _label = label;
    _weight = weight;
    _from = from;
    _to = to;
  }

  String get label => _label;

  double get weight => _weight;

  Node get from => _from;

  Node get to => _to;
}
