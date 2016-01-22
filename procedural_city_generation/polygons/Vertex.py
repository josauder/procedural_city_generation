import matplotlib.pyplot as plt
from config import Variables
plotbool=False
try:

    #Try except cause otherwise jsontools wont work because it tries to initialize variables
    if Variables().plot == 1:
        plotbool=True
except:
    pass


class Vertex(object):
    def __init__(self, coords):
        self.coords=coords
        self.neighbours=[]
        self.minor_road=False
        self.seed=False

    def __getitem__(self, i):
        return self.coords[i]


    def __cmp__(self, other):
        if isinstance(other, Vertex):
            if self[0]>other[0]:
                return 1
            elif self[0]<other[0]:
                return -1
            else:
                if self[1]>other[1]:
                    return 1
                elif self[1]<other[1]:
                    return -1
            return 0



    def connection(self, other):
        if other not in self.neighbours:
            self.neighbours.append(other)
        if self not in other.neighbours:
            other.neighbours.append(self)

        if plotbool:
#        if True:
            col='black'
            width=3
            if self.minor_road or other.minor_road:
                col='blue'
                width=1

            plt.plot([self.coords[0], other.coords[0]], [self.coords[1], other.coords[1]], color=col, linewidth=width)


    def __repr__(self):
        return "Vertex"+str(self.coords)+"\n"
