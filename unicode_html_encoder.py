inp = input("Write your text\n")
res = ""
for i in inp:
    res+=f"&#{ord(i)};"
print(res)
