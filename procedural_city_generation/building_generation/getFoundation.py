import numpy as np

from procedural_city_generation.polygons.Polygon2D import Polygon2D

def getFoundation(poly, grid_width=0.01, eps=10**-8):

    rect_area = 0
    rect_height = 0
    rect_x = [0, 0]
    rect_base = None

    #Iterate through edges which are bordering a road, find largest
    #rectangle for each one
    for base in sorted([edge for edge in poly.edges if edge.bordering_road],
                            key=lambda x: -x.length):

        #Initialize height
        height = grid_width
        done = False

        while not done:
            cuts = []
            for other in poly.edges:
                #Find all intersections
                if other is not base:
                    x = [0, 0]
                    try:
                        x = np.linalg.solve(np.array(((base.dir_vector), (-other.dir_vector))).T,
                                                        other[0] - (base[0] + base.n * height))
                    except np.linalg.LinAlgError:
                        pass
                    if eps < x[1] < 1 - eps:
                        #intersection found
                        if x[0] < eps:
                            cuts.append(0)
                        elif x[0] > 1 - eps:
                            cuts.append(1)
                        else:
                            cuts.append(x[0])

            if len(cuts) == 2:
                #Possible rectangle found
                width = abs(base.length*cuts[1] - base.length*cuts[0])
                this_area = width * height
                if this_area > rect_area:
                    rect_area = this_area
                    rect_height = height
                    rect_x = cuts
                    rect_base = base
                height += grid_width
            else:
                done = True
                break
    if rect_height:
        p1 = rect_base[0] + rect_x[1] * rect_base.dir_vector
        p2 = rect_base[0] + rect_x[0] * rect_base.dir_vector
        p3 = p2 + rect_height * rect_base.n
        p4 = p1 + rect_height * rect_base.n

        return Polygon2D([p1, p2, p3, p4])
    else:
        #TODO: assign issue to lenny ... why return false
        return False



if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from plot_poly import plot_poly
    from getBlock import getBlock
    from getLots import getLots
    import construct_polygons as cp

    polys, vertices = cp.main()

    lots = getLots(polys[:20], vertices)
    for poly in lots:
        if poly.poly_type == "lot":
            f = getFoundation(poly)
            if f:
                plot_poly(poly, mode="k")
                plot_poly(f, mode="g")
            else:
                plot_poly(poly, mode="r")
    plt.show()














