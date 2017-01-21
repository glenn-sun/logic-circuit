# Dependency list
default_graph = {}
graph = default_graph
variables = []

# Base class for all nodes
class Node(object):
	def __init__(self, *args):
		graph[self] = args

class ConstTrue(Node):
	def __init__(self):
		super(ConstTrue, self).__init__()

	def eval(self, input_dict):
		return True

class ConstFalse(Node):
	def __init__(self):
		super(ConstFalse, self).__init__()

	def eval(self, input_dict):
		return False

class Variable(Node):
	def __init__(self):
		super(Variable, self).__init__()
		variables.append(self)

	def eval(self, input_dict):
		return input_dict[self]

class And(Node):
	def __init__(self, *args):
		super(And, self).__init__(*args)

	def eval(self, input_dict):
		result = True # True and X = X
		for node in graph[self]:
			result = result and node.eval(input_dict)
		return result

class Or(Node):
	def __init__(self, *args):
		super(Or, self).__init__(*args)
	
	def eval(self, input_dict):
		result = False # False or X = X
		for node in graph[self]:
			result = result or node.eval(input_dict)
		return result

class Not(Node):
	def __init__(self, node):
		super(Not, self).__init__(node)

	def eval(self, input_dict):
		return not graph[self][0].eval(input_dict)

class Nand(Node):
	def __init__(self, *args):
		super(Nand, self).__init__(*args)

	def eval(self, input_dict):
		result = True # True and X = X
		for node in graph[self]:
			result = result and node.eval(input_dict)
		return not result

class Nor(Node):
	def __init__(self, *args):
		super(Nor, self).__init__(*args)
	
	def eval(self, input_dict):
		result = False # False or X = X
		for node in graph[self]:
			result = result or node.eval(input_dict)
		return not result

class Xor(Node):
	def __init__(self, *args):
		super(Xor, self).__init__(*args)

	def eval(self, input_dict):
		sum_of_deps = sum([node.eval(input_dict) for node in graph[self]])
		return bool(sum_of_deps % 2)

class Xnor(Node):
	def __init__(self, *args):
		super(Xnor, self).__init__(*args)

	def eval(self, input_dict):
		sum_of_deps = sum([node.eval(input_dict) for node in graph[self]])
		return not bool(sum_of_deps % 2)

# Evalute for a certain variable
def partial_eval(node, input_dict={}, return_result=False):
	result = node.eval(input_dict)
	if return_result:
		return result
	else:
		print result

class Graph(object):
	def __init__(self):
		self.graph = {}

	def __enter__(self):
		graph = self.graph

	def __exit__(self, type, value, traceback):
		graph = default_graph
		
# Generate a full truth table
def eval(node):
	input_dict = {}
	results = []
	for i in range(2**len(variables)):
		partial_result = ""
		# Convert decimal to bits in reverse (000..., 100..., 010..., 110...)
		for var in variables:
			input_dict[var] = i % 2
			partial_result += str(i % 2)
			i /= 2

		partial_result += '|' + str(int(node.eval(input_dict)))

		results.append(partial_result)

	for partial_result in sorted(results):
		print partial_result