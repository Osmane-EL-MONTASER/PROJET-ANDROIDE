class UnknownNodeException implements Exception {
  String errMsg() => 'The given node doesn\'t exist.';
}

class UnknownEdgeException implements Exception {
  String errMsg() => 'The given edge doesn\'t exist.';
}
