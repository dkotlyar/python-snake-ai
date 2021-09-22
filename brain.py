import numpy as np

class Brain:
    def __init__(self):
        self.inputs = 10
        self.output = [
            np.array([[1, 0], [0, 1]]),  # движение прямо
            np.array([[0, -1], [1, 0]]), # поворот направо
            np.array([[0, 1], [-1, 0]])  # поворот налево
        ]
        layers_config = [
            [12, 'relu'],
            [6, 'sigmoid'],
            [len(self.output), 'softmax']
        ]

        layers = []
        lastSize = self.inputs
        for lc in layers_config:
            w = 2 * np.random.rand(lastSize, lc[0]) - 1
            b = 2 * np.random.rand(lc[0]) - 1
            layers.append([w, b, lc[1]])
            lastSize = lc[0]
        self.layers = layers

    def predict(self, inputs):
        return self.output[np.argmax(self.predictLowLevel(inputs))]

    def predictLowLevel(self, inputs):
        o = inputs
        for layer in self.layers:
            weights = layer[0]
            bias = layer[1]
            af = layer[2]

            o = self.activation(np.dot(o, weights) + bias, af)
        return o

    def activation(self, nparr, f):
        if (f == 'relu'):
            return self.relu(nparr)
        elif (f == 'sigmoid'):
            return self.sigmoid(nparr)
        elif (f == 'softmax'):
            return self.softmax(nparr)
        else:
            raise Exception('Unknown activation function ' + f)

    def relu(self, nparr):
        return [x if x >= 0 else 0 for x in nparr]

    def sigmoid(self, nparr):
        return [1 / (1 + np.exp(-x)) for x in nparr]

    def softmax(self, nparr):
        if (len(nparr.shape) == 1):
            return self.softmax(np.expand_dims(nparr, axis=0))[0]
        return self.aerinkim_softmax(nparr)

    # https://aerinykim.medium.com/how-to-implement-the-softmax-derivative-independently-from-any-loss-function-ae6d44363a9d
    def aerinkim_softmax(self, signal):
        assert len(signal.shape) == 2
        # Calculate activation signal
        e_x = np.exp( signal )
        signal = e_x / np.sum( e_x, axis = 1, keepdims = True )
        return signal

    def combine(mom, dad):
        layers = []
        for ml, dl in zip(mom.layers, dad.layers):
            layerWShape = ml[0].shape
            layerBShape = ml[1].shape

            momGenome = ml[0].flatten(), ml[1].flatten()
            dadGenome = dl[0].flatten(), dl[1].flatten()

            prob = np.random.rand(len(momGenome[0])), np.random.rand(len(momGenome[1]))

            childGenome = (
                np.array([m if p < 0.49 else d if p < 0.98 else 2 * np.random.rand() - 1 for m,d,p in zip(momGenome[0], dadGenome[0], prob[0])]),
                np.array([m if p < 0.49 else d if p < 0.98 else 2 * np.random.rand() - 1 for m,d,p in zip(momGenome[1], dadGenome[1], prob[1])])
            )

            w = childGenome[0].reshape(layerWShape)
            b = childGenome[1].reshape(layerBShape)
            layers.append([w, b, ml[2]])

        child = Brain()
        child.layers = layers

        return child