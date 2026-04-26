def sub_values(question_base, values: list):
    return question_base.format(*values)

example_base = "The diagram shows {0} blocks in contact on a smooth surface. A {1}N force acts on block {2}, and the surface can be considered frictionless. Calculate: "
values = [2, 48, "J"]
print(sub_values(example_base, values))