filename = "text_2_var_48"

with open(filename) as file:
    lines = file.readlines()

result = list()

for line in lines:
    line_sum = sum(map(int, line.strip().split("/")))
    result.append(line_sum)

with open(filename + "_result", "w") as file:
    file.write("\n".join(map(str, result)))
