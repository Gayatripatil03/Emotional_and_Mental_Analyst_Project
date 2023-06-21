S1 = "i love python coding"
T1 = "coding in python is easy"
s0 = S1.lower()
s1 = T1.lower()
s0List = s0.split(" ")
s1List = s1.split(" ")
print(len(list(set(s0List)&set(s1List))))
