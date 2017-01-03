# Dependency list
graph = {}

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

# Evalute for a certain variable
def partial_eval(node, input_dict={}, return_result=False):
	result = node.eval(input_dict)
	if return_result:
		return result
	else:
		print result