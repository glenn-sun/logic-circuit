class Graph(object):
	"""Container that holds nodes and dependencies.

	Attributes:
		_graph: A dictionary with nodes as keys and a tuple of their 
			dependencies as values.
	"""
	def __init__(self):
		self._graph = {}

	def __enter__(self):
		"""Set the global graph to this graph."""
		global _graph
		_graph = self

	def __exit__(self, type, value, traceback):
		"""Reset the global graph to the default graph."""
		global _graph
		_graph = _default_graph
	
	def __getitem__(self, key):
		"""Get a tuple of dependency nodes.
		
		Args:
			key: The node whose dependencies are wanted.
		
		Returns:
			A tuple of nodes that are dependencies for the key.

		Raises:
			KeyError: The given key is not present in the graph.
		"""
		return self._graph[key]

	def __setitem__(self, key, items):
		"""Set the dependencies of a node.

		Args:
			key: The node in question.
			items: The dependencies to set.

		Raises:
			TypeError: The dependencies are not derived from _Node.
		"""
		for item in items:
			if not isinstance(item, _Node):
				raise TypeError(item)

		self._graph[key] = items

	def partial_eval(self, node, input_dict={}, print_result=True, 
		return_result=False):
		"""Evaluate a node with certain inputs.

		Recursively walks the graph and computes each node along the way. The inputs are passed along so that they can be used whenever a Variable needs to be evaluated.

		The values of the input_dict are first converted to boolean values before being passed along.

		Args:
			node: The node to evaluate.
			input_dict: A dictionary with Variable objects as keys and bools 
				as values.
			print_result: A bool to decide if the result should be printed.
			return_result: A bool to decide if the result should be returned.

		Returns:
			The value of the node if return_result is True, else None.

		Raises:
			KeyError: Required Variable not found in input_dict, OR requested 
				node not in graph.
			AttributeError: Requested node not derived from _Node.
		"""

		if not node in self._graph:
			raise KeyError(node)

		input_dict = {k: bool(v) for k, v in input_dict.iteritems()}

		result = node.eval(self._graph, input_dict)
		if print_result:
			print result
		if return_result:
			return result


# The default graph is used when nodes are created outside a with-statement.
_default_graph = Graph()
_graph = _default_graph


class _Node(object):
	"""The base class for all nodes.

	Sets the dependencies of a node.

	Args:
		*args: A tuple of dependencies

	Raises:
		TypeError: The dependencies are not derived from _Node.
	"""
	def __init__(self, *args):
		_graph[self] = args

class ConstTrue(_Node):
	"""Return True.

	Dependencies:
		None
	"""
	def __init__(self):
		super(ConstTrue, self).__init__()

	def eval(self, graph, input_dict):
		return True

class ConstFalse(_Node):
	"""Return False.

	Dependencies:
		None
	"""
	def __init__(self):
		super(ConstFalse, self).__init__()

	def eval(self, graph, input_dict):
		return False

class Variable(_Node):
	"""Return the value assigned to this node.

	Dependencies:
		None

	Raises:
		KeyError: No value assigned to this node.
	"""
	def __init__(self):
		super(Variable, self).__init__()

	def eval(self, graph, input_dict):
		return input_dict[self]

class And(_Node):
	"""Perform a logical AND function.

	Dependencies:
		*args: A tuple of nodes.

	Returns:
		KeyError: This node is not in the current graph.
	"""
	def __init__(self, *args):
		super(And, self).__init__(*args)

	def eval(self, graph, input_dict):
		result = True # True and X = X
		for node in graph[self]:
			result = result and node.eval(graph, input_dict)
		return result

class Or(_Node):
	"""Perform a logical OR function.

	Dependencies:
		*args: A tuple of nodes.

	Returns:
		KeyError: This node is not in the current graph.
	"""
	def __init__(self, *args):
		super(Or, self).__init__(*args)
	
	def eval(self, graph, input_dict):
		result = False # False or X = X
		for node in graph[self]:
			result = result or node.eval(graph, input_dict)
		return result

class Not(_Node):
	"""Perform a logical NOT function.

	Dependencies:
		node: A node.

	Returns:
		KeyError: This node is not in the current graph.
	"""
	def __init__(self, node):
		super(Not, self).__init__(node)

	def eval(self, graph, input_dict):
		return not graph[self][0].eval(graph, input_dict)

class Nand(_Node):
	"""Perform a logical NAND function.

	Dependencies:
		*args: A tuple of nodes.

	Returns:
		KeyError: This node is not in the current graph.
	"""
	def __init__(self, *args):
		super(Nand, self).__init__(*args)

	def eval(self, graph, input_dict):
		result = True # True and X = X
		for node in graph[self]:
			result = result and node.eval(graph, input_dict)
		return not result

class Nor(_Node):
	"""Perform a logical NOR function.

	Dependencies:
		*args: A tuple of nodes.

	Returns:
		KeyError: This node is not in the current graph.
	"""
	def __init__(self, *args):
		super(Nor, self).__init__(*args)
	
	def eval(self, graph, input_dict):
		result = False # False or X = X
		for node in graph[self]:
			result = result or node.eval(graph, input_dict)
		return not result

class Xor(_Node):
	"""Perform a logical XOR function.
	
	In the case that more than 2 dependencies are passed, this node generates an even parity bit.

	Dependencies:
		*args: A tuple of nodes.

	Returns:
		KeyError: This node is not in the current graph.
	"""
	def __init__(self, *args):
		super(Xor, self).__init__(*args)

	def eval(self, graph, input_dict):
		sum_of_deps = sum([node.eval(graph, input_dict) for node in graph[self]])
		return bool(sum_of_deps % 2)

class Xnor(_Node):
	"""Perform a logical XNOR function.
	
	In the case that more than 2 dependencies are passed, this node generates an odd parity bit.

	Dependencies:
		*args: A tuple of nodes.

	Returns:
		KeyError: This node is not in the current graph.
	"""

	def __init__(self, *args):
		super(Xnor, self).__init__(*args)

	def eval(self, graph, input_dict):
		sum_of_deps = sum([node.eval(graph, input_dict) for node in graph[self]])
		return not bool(sum_of_deps % 2)

def partial_eval(node, input_dict={}, return_result=False):
	"""Call partial_eval on the current graph.

	See Graph.partial_eval for implentation details."""
	return _graph.partial_eval(node, input_dict=input_dict, return_result=return_result)