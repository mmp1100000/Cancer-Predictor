with open("./data/leukemia_train.arff", "r") as file:
    data = file.read()
data = data.split(",")
print(len(data))
for expr in data:

    if expr == "ALL" or expr == "AML":
        print("a")
        print(expr)
# dataset = arff.load(open('mydataset.arff', 'rb'))
# data = np.array(dataset['data'])