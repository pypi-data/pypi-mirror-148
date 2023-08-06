import numpy as np
import queue

class DBSCAN:
    """
    DBSCAN instance, this instance does NOT have methods which return values or predict, 
    so it is important to access the computes values by using the attributes.

    Parameters:

        eps (float): The minimum radius of the distances for neighboring instances

        minpoints (int): The minimum number of points for an instance to become a core
    
    Attributes:

        pointlabel (list): The list of the sample indices.

        cl (int): The number of clusters.

    """
    def __init__(self, eps = 2, minpoints = 5):
        self.eps = eps
        self.minpoints = minpoints

    def _neigh_point(self,X , index, eps):
        """Checks for neighboring points"""
        points = []
        for i in range(len(X)):
            if (np.linalg.norm(X[i] - X[index]) <= eps):
                points.append(i)
        return points
    
    def fit(self, X):
        """
        Fits the instance

        Parameters:
            X (ndarray): ndarray of the X values
        """
        self.pointlabel  = [0] * len(X)
        pointcount = []
        self.corepoint=[]
        self.noncore=[]
        
        for i in range(len(X)):
            pointcount.append(self._neigh_point(X ,i ,self.eps))
        
        for i in range(len(pointcount)):
            if (len(pointcount[i])>=self.minpoints):
                self.pointlabel[i]=-1
                self.corepoint.append(i)
            else:
                self.noncore.append(i)

        for i in self.noncore:
            for j in pointcount[i]:
                if j in self.corepoint:
                    self.pointlabel[i]=-2

                    break
                
        self.cl = 1
        for i in range(len(self.pointlabel)):
            q = queue.Queue()
            if (self.pointlabel[i] == -1):
                self.pointlabel[i] = self.cl
                for x in pointcount[i]:
                    if(self.pointlabel[x]==-1):
                        q.put(x)
                        self.pointlabel[x]=self.cl
                    elif(self.pointlabel[x]==-1):
                        self.pointlabel[x]=self.cl
                while not q.empty():
                    neighbors = pointcount[q.get()]
                    for y in neighbors:
                        if (self.pointlabel[y]==-1):
                            self.pointlabel[y]=self.cl
                            q.put(y)
                        if (self.pointlabel[y]==-1):
                            self.pointlabel[y]=self.cl            
                self.cl=self.cl+1