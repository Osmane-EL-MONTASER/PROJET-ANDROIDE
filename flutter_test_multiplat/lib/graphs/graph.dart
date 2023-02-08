import 'package:flutter_test_multiplat/graphs/edge.dart';
import 'package:flutter_test_multiplat/graphs/exceptions/graphexceptions.dart';
import 'package:flutter_test_multiplat/graphs/node.dart';

class Graph {
  late Map<String, Edge> _edges;
  late Map<String, Node> _nodes;

  /// Constructs an empty [Graph]
  Graph() {
    _edges = <String, Edge>{};
    _nodes = <String, Node>{};
  }

  /// Constructs a [Graph] from a [Map] of [nodes] and
  /// a [Map] of [Edges].
  Graph.fromMaps(
      {required Map<String, Node> nodes, required Map<String, Edge> edges}) {
    _nodes = nodes;
    _edges = edges;
  }

  /// Returns the [Edge] from the node [from] to the node
  /// [to] if it exists.
  ///
  /// Throws an [UnknownEdgeException] when the given
  /// [from] and [to] nodes don't correspond to an Edge.
  Edge? getEdgeFromTo(Node from, Node to) {
    Edge? edge;

    //Creating the key [String] to access the corresponding edge.
    String edgeIndex = '${from.label};${to.label}';

    edge = _edges[edgeIndex];

    if (edge == null) {
      throw (UnknownEdgeException());
    }

    return edge;
  }

  /// Gives a [Node] object corresponding to its given
  /// [id].
  ///
  /// Throws an [UnknownNodeException] when the given
  /// [id] doesn't correspond to an existing node.
  Node getNodeWithId(int id) {
    Node? node;

    node = _nodes[id];

    if (node == null) {
      throw (UnknownNodeException());
    }

    return node;
  }

  /// Creates an [Edge] from [from] to [to] in the graph.
  void addEdgeFromTo(Node from, Node to, double weight, {String? label}) {
    String edgeIndex = '${from.label};${to.label}';
    label ??= edgeIndex;

    _edges[edgeIndex] = Edge(from: from, to: to, label: label, weight: weight);

    //print(
    //'${_edges.values.first.from.label} -> ${_edges.values.first.to.label}');
  }

  void addNode(Node node) {
    _nodes[node.label] = node;
  }
}
