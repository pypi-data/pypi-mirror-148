from model import Model
import numpy as np
import json

f = open('data.json', 'r')
data = json.load(f)
f.close()

inputs = []
outputs = []
for i in data:
    inputs.append(i[0])
    outputs.append(i[1])

# 1 = +
# 2 = -

# use it to make a counter
model = Model(1, 1)
model.learn_rate(0.001)
model.create_layer([1, 1], [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]], [[2], [3], [4], [5], [6], [7], [8], [9], [10], [11]])
model.train(inputs, outputs, epochs=5)
model.train_with_layers(inputs)
model.train_with_layers(inputs)
output = model.predict(np.array([[1]]))
print(output)
for i in output:
    print(round(i[0]))

model.save()