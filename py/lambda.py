from functional import seq

data = [4, 10, 7, 8]

result = (
    seq(data)
    .chunk(2)
    .map(lambda pair: pair[0] * pair[1])
    .sum()
)

print(result)  

# More examples (group by, zip, reduce)

seq(["a", "bb", "c"]).group_by(len) #[[a, c], bb]
seq([1,2,3,4]).reduce(lambda a, b: a + b) # 10
seq([1,2,3]).zip([10,20,30])  # [(1, 10), (2, 20), (3, 30)]
