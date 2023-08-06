import numpy as np
class Loss_Simple(object):
    def __init__(ミク, numdims: int):
        ミク.__shape = ( 1 , numdims )
    def __call__(ミク, y_pred: np.matrix, y_true: np.matrix):
        y_pred_flat = np.array(y_pred).flatten()
        y_true_flat = np.array(y_true).flatten()
        y_= (y_pred_flat - y_true_flat)
        return np.mat((y_ ** 2 / 2).reshape(ミク.__shape)), np.mat(y_.reshape(ミク.__shape))