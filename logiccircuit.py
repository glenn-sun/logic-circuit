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
		result = True
		for node in graph[self]:
			result = result and node.eval()
		return result

# Evalute for a certain variable
def partial_eval(node, return_result=False):
	result = node.eval()
	if return_result:
		return result
	else:
		print result