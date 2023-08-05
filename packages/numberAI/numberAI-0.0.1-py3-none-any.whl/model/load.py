from model import Model

model = Model.load()
output = model.predict([[1]])
print(output)