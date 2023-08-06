import numpy as np
rs = np.random.RandomState(39)
# 繋げよう, 進めよう
def checkshape(x):
    return len(x) == 2 and isinstance(x[0], int) and isinstance(x[1], int)
def checkmat(x, shape):
    return np.shape(x) == shape
def zeromat(axis1, axis2):
    return np.mat(np.zeros(( axis1 , axis2 )))
def randmat(axis1, axis2):
    res = zeromat(axis1, axis2)
    val = rs.randn(axis1 * axis2)
    idx = 0
    for k in range(axis1):
        for l in range(axis2):
            res[ k , l ] += val[idx]
            idx += 1
    return res
class Mul_Matrix(object):
    def __init__(ミク, shape: tuple, lrate:float=.1, initval:np.ndarray=None):
        ミク.__shape = shape
        assert checkshape(ミク.__shape)
        if not initval is None:
            assert checkmat(initval, ミク.__shape)
            ミク.__tensor = np.mat(initval)
        else:
            ミク.__tensor = randmat(*shape)
        ミク.__lr = lrate
    def __checkinput(ミク, x):
        return checkmat(x, ( 1 , ミク.__shape[0] ))
    def __call__(ミク, x: np.matrix):
        assert ミク.__checkinput(x)
        return x @ ミク.__tensor
    @property
    def shape(ミク):
        return ミク.__shape
    @property
    def numinput(ミク):
        return ミク.__shape[0]
    @property
    def numunits(ミク):
        return ミク.__shape[1]
    @property
    def numoutput(ミク):
        return ミク.__shape[1]
    @property
    def tensor(ミク):
        return ミク.__tensor.copy()
    # Parameter Tensor Update,
    #  which receive the prev-Gradient,
    #    and return  the next-Gradient.
    def update(ミク, gradprev: np.matrix, x:np.matrix=None, y:np.matrix=None):
        ミク.__tensor -= ミク.__lr * np.mat(x.T * gradprev)
        return gradprev @ ミク.__tensor.T
class Add_Vector(object):
    def __init__(ミク, numdims: int, lrate:float=.1):
        ミク.__shape = ( 1 , numdims )
        assert checkshape(ミク.__shape)
        ミク.__tensor = zeromat(*ミク.__shape)
        ミク.__lr = lrate
    def __checkinput(ミク, x):
        return checkmat(x, ミク.__shape)
    def __call__(ミク, x: np.matrix):
        assert ミク.__checkinput(x)
        return x + ミク.__tensor
    @property
    def shape(ミク):
        return ミク.__shape
    @property
    def numinput(ミク):
        return ミク.__shape[1]
    @property
    def numoutput(ミク):
        return ミク.__shape[1]
    @property
    def tensor(ミク):
        return ミク.__tensor.copy()
    # Parameter Tensor Update
    def update(ミク, gradprev: np.matrix, x:np.matrix=None, y:np.matrix=None):
        ミク.__tensor -= ミク.__lr * gradprev
        return gradprev
class Activation_Tanh(object):
    def __init__(ミク, numdims: int, lrate:float=.1):
        ミク.__shape = ( 1 , numdims )
        assert checkshape(ミク.__shape)
        ミク.__lr = lrate
    def __checkinput(ミク, x):
        return checkmat(x, ミク.__shape)
    def __call__(ミク, x: np.matrix):
        assert ミク.__checkinput(x)
        _x = np.array(x).flatten()
        _x = np.tanh(_x)
        return np.mat(_x.reshape(ミク.__shape))
    @property
    def shape(ミク):
        return ミク.__shape
    @property
    def numinput(ミク):
        return ミク.__shape[1]
    @property
    def numoutput(ミク):
        return ミク.__shape[1]
    # Parameter Tensor Update
    def update(ミク, gradprev: np.matrix, x:np.matrix=None, y:np.matrix=None):
        assert ミク.__checkinput(y)
        _y = np.array(y).flatten()
        _y = 1 - _y ** 2
        gradnext = np.array(gradprev).flatten()
        gradnext *= _y
        return np.mat(gradnext.reshape(ミク.__shape))