from fuzzylogic.classes import FuzzyVariable, FuzzySystem, FuzzyRule

# Create fuzzy variables for the input and output
input_var = FuzzyVariable('input', 0, 100, 10)
output_var = FuzzyVariable('output', 0, 10, 1)

# Add fuzzy sets to the input variable
input_var.add_triangular('low', 0, 25, 50)
input_var.add_triangular('medium', 25, 50, 75)
input_var.add_triangular('high', 50, 75, 100)

# Add fuzzy sets to the output variable
output_var.add_triangular('low', 0, 2.5, 5)
output_var.add_triangular('medium', 2.5, 5, 7.5)
output_var.add_triangular('high', 5, 7.5, 10)

# Create a fuzzy rule
rule = FuzzyRule(
    (input_var['low'],),
    (output_var['low'],)
)

# Create a fuzzy system
system = FuzzySystem()
system.variables['input'] = input_var
system.variables['output'] = output_var
system.rules.append(rule)

# Evaluate the fuzzy system
input_value = 30
output_value = system.compute({'input': input_value})['output']

print(f"Input: {input_value}")
print(f"Output: {output_value}")
