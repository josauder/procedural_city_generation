__author__ = 'jonathan'

class LinalgTools(object):

    def __init__(self, floor, polygons):
        self.floor=floor
        self.polygons=polygons
    
    def shrinkwrap(self):
        for p in self.polygons:
            if p.texture.shrinkwrap:
                #do linalg shit
                pass
        return 0
    
    def triangulate(self):
        pass
        
