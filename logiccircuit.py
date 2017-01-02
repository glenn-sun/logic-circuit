# Dependency list
graph = {}

# Base class for all nodes
class Node(object):
	def __init__(self, *args):
		graph[self] = args

class ConstTrue(Node):
	def __init__(self):
		super(ConstTrue, self).__init__()

class ConstFalse(Node):
	def __init__(self):
		super(ConstFalse, self).__init__()

class And(Node):
	def __init__(self, *args):
		super(And, self).__init__(args)