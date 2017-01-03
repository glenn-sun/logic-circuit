# Dependency list
graph = {}

# Base class for all nodes
class Node(object):
	def __init__(self, *args):
		graph[self] = args

class ConstTrue(Node):
	def __init__(self):
		super(ConstTrue, self).__init__()

	def eval(self):
		return True

class ConstFalse(Node):
	def __init__(self):
		super(ConstFalse, self).__init__()

	def eval(self):
		return False

class And(Node):
	def __init__(self, *args):
		super(And, self).__init__(*args)

	def eval(self):
		result = True # True and X = X
		for node in graph[self]:
			result = result and node.eval()
		return result

class Or(Node):
	def __init__(self, *args):
		super(Or, self).__init__(*args)
	
	def eval(self):
		result = False # False or X = X
		for node in graph[self]:
			result = result or node.eval()
		return result

class Not(Node):
	def __init__(self, node):
		super(Not, self).__init__(node)

	def eval(self):
		return not graph[self][0].eval()

# Evalute for a certain variable
def partial_eval(node, return_result=False):
	result = node.eval()
	if return_result:
		return result
	else:
		print result