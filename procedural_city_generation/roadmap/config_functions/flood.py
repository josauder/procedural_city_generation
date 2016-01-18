


def flood(heightmap, pos, h):
    """
    pos is a pair of indices on heightmap (position where it gets flooded)
    h is the corresponding height
    """
    flooded=np.zeros(heightmap.shape)

    stencil=np.array([
    [-1, 0],
    [1, 0],
    [0, 1],
    [0, -1]
    ])

    front=[pos]
    while len(front)>0:
        new_front=[]
        for x in front:
            if heightmap[x]<h:
                flooded[x]=True
                new_front.extend(
                [new for new in x+stencil if not flooded[new] and not np.any(x<0) and not x[0]>heightmap.shape[0] and not x[1]>heightmap.shape[1]]
                )
        front=new_front

    return flooded
