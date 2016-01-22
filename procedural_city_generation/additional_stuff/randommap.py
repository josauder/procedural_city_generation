from __future__ import division
import numpy as np
import math
import random
from scipy.spatial import Delaunay
from copy import copy


def randommap(rows, cols):
    '''terribly coded random-height-map generator, takes # of rows and cols as input as well as the minimum and maximum height for starting the randomization'''
    '''If balance is True, it will result in the map having "cube" dimensions, as in base and height having similar axis scales'''
    '''sadly only works when rows=cols'''


    #Starts off with an Array full of zeros
    arr=np.zeros((rows, cols))


    def semirand(x):
        '''Gives a number a random value within a given tolerance'''
        return x+0.002+(np.random.uniform(-0.005, +0.005))

    def fillarray(x, y):
        '''Fills row:x col:y of the array to be filled out'''

        if x!=0 and y!=0:
            arr[x][y]=(semirand(arr[x-1][y])+arr[x-1][y-1]+arr[x][y-1])/3

        elif x == 0 and y!=0:
            arr[x][y]=semirand(arr[0][y-1])

        elif y == 0 and x!=0:
            arr[x][y]=semirand(arr[x-1][0])

        elif (x+y) == 0:
            arr[0][0]=-0.1


    for i in xrange(cols):
        for k in xrange(rows):
            fillarray(i, k)



    return arr




def findarea(arr, start, lower, upper, done):
    done2=copy(done)

    def donify(xy):
        try:
            done2[xy[0], xy[1]]=1
        except:
            pass

    def check(xy):
        try:
            if done2[xy[0], xy[1]] == 0:

                return True

            return False
        except:
            return False

    front=[start]
    while len(front)>0:
        neufront=[]
        for xy in front:
            x, y=xy[0], xy[1]
            if lower<arr[x, y]<=upper:
                arr[x, y]=upper
                done[x, y]=1

                neighbors=[[x+1, y], [x-1, y], [x, y-1], [x, y+1]]
                neufront.extend([ob for ob in neighbors if check(ob)])

                [donify(ob) for ob in neighbors]
        front=neufront

    return arr, done





def getwatermap(arr, waterheight):
    arr=copy(arr)
    done=np.zeros(arr.shape)


    undone=np.argwhere(arr<waterheight)
    for x in undone:
        arr[x[0], x[1]]=waterheight
        done[x[0], x[1]]=1

    undone=np.argwhere(done == 0)
    i=waterheight+1000


    while len(undone)>0:

        arr, done=findarea(arr, undone[0], waterheight, i, done)
        i+=1000
        undone=np.argwhere(done == 0)

    arr+=waterheight-1
    arr//=1000
    return arr




def main(border, path):
    from scipy.spatial import Delaunay as delaunay

    rows, cols=border[0], border[1]




    array=randommap(rows*10, cols*10)
    array+=array.min()
    array/=array.max()
    array-=array.max()
    indices    =    np.vstack(np.unravel_index(np.arange(array.shape[0]*array.shape[1]), array.shape)).T
    points= np.column_stack((indices, array[indices[:, 0], indices[:, 1]]))
    triangles=np.sort(delaunay(indices).simplices)


    points*=np.array([0.1, 0.1, 10])
    points-=np.array([-rows/2, -cols/2, 0])

    import pickle

    with open(path+"/temp/randommap_"+str(border[0])+"_"+str(border[1]), "w") as f:
        f.write(pickle.dumps([points.tolist(), triangles.tolist()]))
    print("New random heightmap generated. If you wish to use an existing one, change the corresponding variable heightmap_name in roadmap.conf")
    return 0
