from __future__ import division
import matplotlib.pyplot as plt
class Weg(object):
    def __init__(self, k1, k2, strassennetz=True):
        print "WEG CREATED XD"
        self.k1=k1
        self.k2=k2

        self.nebenstrasse=False
        self.color='black'
        self.linewidth=3
        if (k1.nebenstrasse or k2.nebenstrasse):
            self.nebenstrasse=True
            self.linewidth=1
            self.color='blue'

        if strassennetz:
            self.k1.nachbarn.append(k2)
            self.k2.nachbarn.append(k1)
            self.k1.wege.append(self)
            self.k2.wege.append(self)


            self.v=k2.coords-k1.coords
        self.r1=[]
        self.r2=[]


    def selfplot(self):
        plt.plot([self.k1.coords[0], self.k2.coords[0]], [self.k1.coords[1], self.k2.coords[1]], color=self.color, linewidth=self.linewidth)

    def __repr__(self):
        return self.k1.__repr__()+self.k2.__repr__()


    def delete(self):
        self.k1.nachbarn.remove(self.k2)
        self.k2.nachbarn.remove(self.k1)
        self.k1.wege.remove(self)
        self.k2.wege.remove(self)
