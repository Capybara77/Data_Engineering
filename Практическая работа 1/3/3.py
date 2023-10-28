import math

filename = "text_3_var_48"
var = 48

with open(filename) as file:
    lines = file.readlines()

all_lines = []

for line in lines:
    nums = line.strip().split(",")
    new_nums = []

    for i in range(len(nums)):
        if nums[i] == "NA":
            num = float((int(nums[i - 1]) + int(nums[i + 1])) / 2)
            if math.sqrt(num) >= (var + 50):
                new_nums.append(num)
        else:
            num = float(nums[i])
            if math.sqrt(num) >= (var + 50):
                new_nums.append(num)

    all_lines.append(new_nums)

output_filename = "result_" + filename

with open(output_filename, "w") as output_file:
    for row in all_lines:
        for num in row:
            output_file.write(str(int(num)) + ",")
        output_file.write("\n")
