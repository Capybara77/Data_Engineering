filename = "text_1_var_48"

with open(filename) as f:
    lines = f.readlines()

dic = dict()

for line in lines:
    normal_line = (line.strip()
         .replace("!", " ")
         .replace("?", " ")
         .replace(",", " ")
         .replace(".", " ")
         .strip())
    
    for nl in normal_line.split():
        if nl in dic:
            dic[nl] += 1
        else:
            dic[nl] = 1

dic = dict(sorted(dic.items(), key = lambda item: item[1], reverse = True))

with open(f"{filename}_result", "w") as f:
    for word in dic:
        f.write(f"{word}:{dic[word]}\n")