# LogicCircuit
A Python module to simulate logical circuits/graphs.

Inspired by the computational graph behind TensorFlow. Granted, it might be overkill but it *is* very powerful.

The module builds a graph as variables are created. Then, the graph can be evaluated to obtain an output.

### To-Do
* Implement the rest of the basic gates (NAND, NOR, XOR, XNOR)
* Implement many MSI (medium-scale integration) circuits
* Allow evaluating for more than one output at a time
* Add more descriptive error messages
* Ensure compatibility with Python 3.x
* Allow the creation of multiple graphs/circuits