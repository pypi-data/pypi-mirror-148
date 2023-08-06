import numpy as np
from itertools import combinations_with_replacement


class PolyExp:
    def __init__(self, degree) -> None:
        self.degree = degree
    def evalnum(self, X):
            """Converts ndarray to poly features"""
            ret = []
            for j in range(len(X)):
                l = np.ndarray.tolist(X[j])
                l.append("c")
                t = []
                for i in combinations_with_replacement(l, self.degree):
                    t.append(i)
                t = [list(_) for _ in t]
                for i in range(len(t)):
                    while "c" in t[i]:
                        t[i].remove("c")
                    t[i] = np.prod(t[i])
                t = np.array(t)
                t = np.sort(t)
                ret.append(t)
            ret = np.array(ret)
            ret = np.sort(ret, 1)
            return ret
class LinearRegressor:
    '''Linear Regressor instance'''
    def __init__(self):
        pass

    def _compute(self, x, y):
        try:
            var = np.dot(x.T,x)
            var = np.linalg.inv(var)
            var = np.dot(var,x.T)
            var = np.dot(var,y)
            self.__thetas = var
        except Exception as e:
            raise e
    
    def fit(self, X, y):
        '''
        Trains the `LinearRegressor` instance, returns none

        Parameters:
            X (ndarray): the training input

            y (ndarray): the training output

        Returns none
        '''
        x = np.array(X)
        ones_ = np.ones(x.shape[0])
        x = np.c_[ones_,x]
        y = np.array(y)
        self._compute(x,y)
    
    def predict(self, X):
        '''
        predicts `y` value for the `x` input

        Parameter:
            X (ndarray): X value to be predicted

        Returns y (ndarray): the predicted values for the supplied X
        '''
        x = np.array(X)
        ones_ = np.ones(x.shape[0])
        x = np.c_[ones_,x]
        result = np.dot(x,self.__thetas)
        return result  

class SingLinearRegressor:
    '''
    Linear Regressor for `x` being a single value (as opposed to an ndarray)

    Slightly faster than `LinearRegressor`, good for large amounts of data

    '''
    def __init__(self):
        self.bet0: float
        self.bet1: float

    def fit(self, X, y: np.array) -> None:
        '''
        Trains the `LinearRegressor` instance, returns none

        Parameters:
            X (ndarray): the training input

            y (ndarray): the training output

        Returns none
        '''
        n = np.size(X)

        meanX = np.mean(X)
        meany = np.mean(y)

        cc_xy = np.sum(y*X) - n*meany*meanX
        cc_xx = np.sum(X*X) - n*meanX*meanX

        bet1 = cc_xy / cc_xx
        bet0 = meany - bet1*meanX

        self.bet0 = bet0
        self.bet1 = bet1

    def predict(self, x: float) -> float:
        '''
        Predicts `y` value for instance `x`

        Parameter:
            x (float): float representing single data instance

        Returns: y float representing value for `x` instance
        '''
        pred = self.bet0 + self.bet1*x
        return pred

class PolyRegressor:
    """Polynomial Regressor instance, uses the degree of the data"""
    def __init__(self, degree=2):
        self.degree = degree
    
    lin = LinearRegressor()

    def fit(self, X, y):
        """
        Fits the `PolyRegressor` instance

        Parameters:
            X (ndarray): ndarray of shape (num_samples, num_features) for input
            
            y (ndarray): numpy array of shape (num_samples,) for output

        returns none
        """
        X = PolyExp(self.degree).evalnum(X)
        #X = self.evalnum(X)
        self.lin.fit(X, y)

    def predict(self, X):
        """
        Predicts y values for supplied X

        Parameter:
            X (ndarray): X value to be predicted

        Returns y (ndarray): the predicted values for the supplied X
        """
        X = PolyExp(self.degree).evalnum(X)
        return self.lin.predict(X)