import numpy as np
from procedural_city_generation.additional_stuff.Singleton import Singleton

gui=None

def main(vertex_list=None):
    '''Input: list of vertices representing the Roadmap
    Output: List of all Polygon2Ds representing Lots,
    List of all Polygon2Ds representing Blocks
    List of all Polygon2Ds which are too large to be Lots
    Polygon2D representing the road-network'''
    singleton=Singleton("polygons")

    if vertex_list is None:
        from procedural_city_generation.additional_stuff import pickletools

        vertex_list=pickletools.reconstruct(singleton.input_name)
        print("Reconstructing of data structure finished")

    import os
    import procedural_city_generation
    path=os.path.dirname(procedural_city_generation.__file__)

    with open(path+"/temp/"+singleton.input_name+"_heightmap.txt", "r") as f:
        border=[int(x) for x in f.read().split("_")[-2:] if x is not '']
    print("Extracting Polygon2Ds")
    from procedural_city_generation.polygons import construct_polygons
    polylist=construct_polygons.getPolygon2Ds(vertex_list)

    print("Polygon2Ds extracted")




    #TODO: DISCUSS
    from procedural_city_generation.polygons.getLots import getLots as getLots
    "%s vertices" %(len(vertex_list))
    polygons=getLots(polylist, vertex_list)

    print("Lots found")
    sorted
    if singleton.plotbool:
        print("Plotting...")
        if gui is None:
            import matplotlib.pyplot as plt
            for g in polygons:
                g.selfplot(plt=plt)
            plt.show()
        else:
            i=0
            for g in polygons:
                g.selfplot(plt=gui)
                i+=1
                if i%singleton.plot_counter == 0:
                    gui.update()
            gui.update()

    import pickle
    with open(os.path.dirname(procedural_city_generation.__file__)+"/temp/"+singleton.input_name+"_polygons.txt", "wb") as f:
        import sys
        if sys.version[0] == "2":
            s = pickle.dumps(polygons)
            f.write(s)
        else:
            pickle.dump(polygons, f)

    return 0

if __name__ == '__main__':
    from procedural_city_generation.polygons.parent_path import parent_path
    import sys
    sys.path.append(parent_path(depth=3))
    main(None)


