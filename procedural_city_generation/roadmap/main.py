#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
gui=None


def main():
    from procedural_city_generation.roadmap.config import config
    from copy import copy

    singleton=config()

    front=copy(singleton.global_lists.vertex_list)
    front.pop(0)
    front.pop()
    vertex_queue = copy(singleton.global_lists.vertex_queue)
    from procedural_city_generation.roadmap.iteration import iteration
    singleton.iterationszaehler=0


    if singleton.plot == 1:
        if gui is None:
            import matplotlib.pyplot as plt
            plt.close()
            fig=plt.figure()
            ax=plt.subplot(111)

            fig.canvas.draw()
            ax.set_xlim((-singleton.border[0], singleton.border[0]))
            ax.set_ylim((-singleton.border[1], singleton.border[1]))
        else:

            gui.set_xlim((-singleton.border[0], singleton.border[0]))
            gui.set_ylim((-singleton.border[1], singleton.border[1]))
    i=0
    while (front!=[] or singleton.global_lists.vertex_queue    !=[]):

        i+=1
        front=iteration(front)

        if singleton.plot == 1:
            if i%singleton.plot_counter == 0:
                if gui is None:
                    plt.pause(0.001)
                    try:
                        fig.canvas.blit(ax.bbox)
                        fig.canvas.flush_events()
                    except:
                        fig.canvas.draw()
                else:
                    gui.update()

            singleton.iterationszaehler=0

    from procedural_city_generation.additional_stuff.pickletools import save_vertexlist


    print("Roadmap is complete")
    save_vertexlist(singleton.global_lists.vertex_list, singleton.output_name, singleton.savefig)
    if gui is None and singleton.plot == 1:
        if singleton.plot == 1:
            plt.show()
    return 0


if __name__ == '__main__':
    import os, sys
    parentpath=os.path.join(os.getcwd(), ("../../"))
    sys.path.append(parentpath)
    main()
