# LogicCircuit
A Python module to simulate logical circuits/graphs.

Inspired by the computational graph behind TensorFlow. Granted, it might be overkill but it *is* very powerful.

The module builds a graph as variables are created. Then, the graph can be evaluated to obtain an output.

### Usage
Start by cloning or downloading the project, then import it into Python. Only Python 2.7 has been tested at the moment.

```python
import logiccircuit as lc
```

Then, build your circuit. In this example, Z = AB + C

```python
A = lc.Variable()
B = lc.Variable()
C = lc.Variable()
M = lc.And(A, B)
Z = lc.Or(M, C)
```

Currently the following gates are availiable:

Name | # of Arguments
--- | ---
ConstTrue | 0
ConstFalse | 0
Variable | 0
And | 2 or more
Or | 2 or more
Not | 1

There are two ways to evaluate a circuit: `partial_eval` and `eval`. `partial_eval` evaulates the circuit for a specific set of inputs, while `eval` generates a full truth table. Input variables in the truth table are in the order they were defined.

```python
lc.partial_eval(Z, input_dict={A: True, B: True, C: False})

# Output:
# True

lc.eval(Z)

# Output:
# 000|0
# 001|1
# 010|0
# 011|1
# 100|0
# 101|1
# 110|1
# 111|1
```

### To-Do
* Implement the rest of the basic gates (NAND, NOR, XOR, XNOR)
* Implement many MSI (medium-scale integration) circuits
* Allow evaluating for more than one output at a time
* Add more descriptive error messages
* Ensure compatibility with Python 3.x
* Allow the creation of multiple graphs/circuits