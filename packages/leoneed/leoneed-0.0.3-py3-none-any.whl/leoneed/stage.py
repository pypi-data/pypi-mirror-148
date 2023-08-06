import numpy as np
from . import needle
from . import stella
class Sequence(object):
    def __init__(self, nodes, loss=stella.Loss_Simple):
        self.__nodes = nodes
        for k in range(len(self.__nodes) - 1):
            """
            if isinstance(self.__nodes[k + 1], needle.Mul_Matrix):
                raise Exception("The implementation of gradient after Matmul hasnot finished yet!")
                """
            assert self.__nodes[k].numoutput == self.__nodes[k + 1].numinput
        self.__loss = loss(self.__nodes[-1].numoutput)
    def __getitem__(self, idx):
        return self.__nodes[idx]
    def mean_loss(self, X: np.ndarray, y: np.ndarray):
        outputensors = [ np.mat(X) ]
        assert outputensors[0].shape == ( 1 , self.__nodes[0].numinput )
        for k in range(len(self.__nodes)):
            outputensors.append(self.__nodes[k](outputensors[k]))
        y_pred = outputensors[-1]
        y_true = np.mat(y)
        assert y_true.shape == ( 1 , self.__nodes[-1].numoutput )
        return self.__loss(y_pred, y_true)[0].mean()
    def predict(self, X: np.ndarray):
        outputensors = [ np.mat(X) ]
        assert outputensors[0].shape == ( 1 , self.__nodes[0].numinput )
        for k in range(len(self.__nodes)):
            outputensors.append(self.__nodes[k](outputensors[k]))
        return outputensors[-1]
    def fit_sample(self, X: np.ndarray, y: np.ndarray):
        outputensors = [ np.mat(X) ]
        assert outputensors[0].shape == ( 1 , self.__nodes[0].numinput )
        for k in range(len(self.__nodes)):
            outputensors.append(self.__nodes[k](outputensors[k]))
        y_pred = outputensors[-1]
        y_true = np.mat(y)
        assert y_true.shape == ( 1 , self.__nodes[-1].numoutput )
        loss, d_loss = self.__loss(y_pred, y_true)
        for k in range(len(self.__nodes)):
            d_loss = self.__nodes[-k - 1].update(d_loss, outputensors[-k - 2], outputensors[-k - 1])
        return self, loss.mean()
def fclayers(numinput, numunits, *args, **kwargs):
    return [
        needle.Mul_Matrix(( numinput , numunits ), *args, **kwargs),
        needle.Add_Vector(numunits),
        needle.Activation_Tanh(numunits),
        ]
def Fool_Connection(numinput, numunits, *args, **kwargs):
    return Sequence([
        *fclayers(numinput, numunits, *args, **kwargs),
        ])
def Auto_Encoder(numvisible, numhidden, w1=None, w2=None):
    return Sequence([
        *fclayers(numvisible, numhidden, initval=w1),
        *fclayers(numhidden, numvisible, initval=w2),
        ])