import numpy as np

class Model:
    # make a model that takes inputs and outputs and generates a new output based on the inputs and outputs
    def __init__(self, inputs, outputs, layers=[]):
        self.inputs = inputs
        self.outputs = outputs
        self.weights = np.random.rand(inputs, outputs)
        self.bias = np.random.rand(outputs)
        self.layers = layers
        self.learning_rate = 0.001
    
    def predict(self, inputs, good=None):
        output = np.dot(inputs, self.weights) + self.bias
        return output
    
    def test(self, inputs, expected_outputs, rounding=True):
        if not rounding:
            predicted_outputs = self.predict(inputs)
            error = predicted_outputs - expected_outputs
            return 1 - np.count_nonzero(error) / inputs.shape[0]
        else:
            predicted_outputs = self.predict(inputs)
            # round everything
            predicted_outputs = np.round(predicted_outputs)
            error = predicted_outputs - expected_outputs
            return 1 - np.count_nonzero(error) / inputs.shape[0]

    def train(self, inputs, expected_outputs, epochs=1, batch_size=1):
        # add a loading bar
        loading_bar = 0
        loss = 0
        accurate = 0
        inputs = np.array(inputs)
        expected_outputs = np.array(expected_outputs)
        for epoch in range(epochs):
            print("\r" + "< " + "=" * int(loading_bar) + " > loss: " + str(int(loss)) + " accurate: " + str(accurate), end="")
            for i in range(0, inputs.shape[0], batch_size):
                loss = 0
                predicted_outputs = self.predict(inputs[i:i+batch_size])
                error = predicted_outputs - expected_outputs[i:i+batch_size]
                # but what if weights is nan
                self.weights /= np.sum(self.weights)
                # and now fix the error that 1 length arrays are not accepted
                if np.any(error):
                    # what if the array is only 1 long
                    if error.shape[0] == 1:
                        error = np.array([error])
                    # non-broadcastable output operand with shape (1,1) doesn't match the broadcast shape (1,1,1)
                    # reshape it
                    error = np.reshape(error, (batch_size, self.outputs))
                    self.weights -= self.learning_rate * np.dot(inputs[i:i+batch_size].T, error)
                    self.bias -= self.learning_rate * np.sum(error, axis=0)
            # add to the loading bar using procentage of 100
            loading_bar += 100 / epochs
            # calculate the loss
            loss += np.sum(np.square(self.predict(inputs) - expected_outputs))
            # and now calculate how accurate it is
            accurate = self.test(inputs, expected_outputs)
        print("\n")
    
    def train_batch(self, inputs, expected_outputs, epochs=1):
        for epoch in range(epochs):
            predicted_outputs = self.predict(inputs)
            error = predicted_outputs - expected_outputs
            self.weights -= self.learning_rate * np.dot(inputs.T, error)
            self.bias -= self.learning_rate * np.sum(error, axis=0)
        return self.test(inputs, expected_outputs, epochs)
    
    def train_smart(self, inputs, expected_outputs, epochs=1, batch_size=1):
        for epoch in range(epochs):
            for i in range(0, inputs.shape[0], batch_size):
                predicted_outputs = self.predict(inputs[i:i+batch_size])
                error = predicted_outputs - expected_outputs[i:i+batch_size]
                self.weights -= self.learning_rate * np.dot(inputs[i:i+batch_size].T, error)
                self.bias -= self.learning_rate * np.sum(error, axis=0)
                # if the error is too big, train it again
                if np.any(error):
                    self.train(inputs, expected_outputs, epochs)
    def train_perfect(self, inputs, expected_outputs, epochs=1, batch_size=1):
        # repeat the training process untill the error is pritty low but if it takes too long, stop it
        for epoch in range(epochs):
            for i in range(0, inputs.shape[0], batch_size):
                predicted_outputs = self.predict(inputs[i:i+batch_size])
                error = predicted_outputs - expected_outputs[i:i+batch_size]
                self.weights -= self.learning_rate * np.dot(inputs[i:i+batch_size].T, error)
                self.bias -= self.learning_rate * np.sum(error, axis=0)
                # if the error is bigger than a corner, train it again
                if np.any(error):
                    self.train_smart(inputs, expected_outputs, epochs)

    def train_check(self, inputs, expected_outputs, epochs=1, loop=1):
        for i in range(loop):
            predicted_outputs = self.predict(inputs)
            error = predicted_outputs - expected_outputs
            # train it again if its wrong
            if np.any(error):
                self.train_smart(inputs, expected_outputs, epochs)
            else: self.train(inputs, expected_outputs, epochs)
            # return the ammount of right predictions
        return 1 - np.count_nonzero(error) / inputs.shape[0]

    def layer(self, model, inputs, outputs):
        return [Model(model[0], model[1]), inputs, outputs]
    def get_layer_model(self, layer):
        return self.layers[layer][0]
    def create_layer(self, model, inputs, outputs):
        self.layers.append([Model(model[0], model[1]), inputs, outputs])
    def train_layers(self, inputs, expected_outputs, epochs=1, batch_size=1):
        for layer in self.layers:
            layer[0].train(layer[1], layer[2], epochs)
    def train_with_layers(self, inputs):
        for layer in self.layers:
            self.train(inputs, layer[0].predict(inputs))

    def save(self, filename="model.npy"):
        np.save(filename, self.weights)
        np.save(filename + '_bias', self.bias)
    def load(self, filename="model.npy"):
        self.weights = np.load(filename)
        self.bias = np.load(filename + '_bias')

    def returnData(self):
        return self.weights, self.bias
    
    def learn_rate(self, learning_rate):
        self.learning_rate = learning_rate