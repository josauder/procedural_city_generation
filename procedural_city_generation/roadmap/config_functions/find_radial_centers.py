import numpy as np
def find_radial_centers(singleton):
    '''Intended to find areas where the rule-image is blue and return the center of such areas'''
    img=singleton.img
    Aufloesung=singleton.center_find_resolution
    quadrate=[]
    for x1 in range( np.shape(img)[0] //Aufloesung ):
        for x2 in range( np.shape(img)[1]//Aufloesung):
            quadrate.append([x1, x2])

    quadrate= [q for q in quadrate if np.argmax(img[q[0]*Aufloesung][q[1]*Aufloesung]) == 2] #auf blaue reduzieren

    areas=[]

    while len(quadrate)>0:   #Flaechen finden, also Quadrate auf Flaechen aufteilen
        areas.append([quadrate[0]])
        quadrate.pop(0)
        h=0
        while h<len( areas[len(areas)-1] ):
            q=areas[len(areas)-1][h]
            for nachbar in[[q[0]-1, q[1]], [q[0]+1, q[1]], [q[0], q[1]-1], [q[0], q[1]+1]]:
                if nachbar in quadrate:
                    areas[len(areas)-1].append(nachbar)
                    quadrate.remove(nachbar)
            h+=1

    centers=   [ np.array([sum( [x[0] for x in y])/len(y)*Aufloesung, sum([x[1] for x in y])/len(y)*Aufloesung]) for y in areas]
    return centers
