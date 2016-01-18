import matplotlib.pyplot as plt

def plot_edge(edge, color="k"):
    plt.plot((edge[0][0], edge[1][0]), (edge[0][1], edge[1][1]), color=color)

"""
def plot_self(self, mode="type"):
    if mode == "type":
        t = self.self_type

        if t == "lot" or t=="block":
            for edge in self.edges:
                plot_edge(edge, "g")
        elif t == "road":
            for edge in self.edges:
                plot_edge(edge, "k")
        else:
            for edge in self.edges:
                plot_edge(edge, "r")
    elif mode == "borders":
        for edge in self.edges:
            if edge.bordering_road:
                plot_edge(edge, 'k')
            else:
                plot_edge(edge, 'r')
    else:
        for edge in self.edges:
            plot_edge(edge, mode)
"""
def plot_self(self):
    color="r"
    t=self.self_type
    if t=="lot" or t=="block":
        color="g"
    elif t=="road":
        color="k"
    composite=np.array([edge for edge in self.edges]+[self.edges[0]])
    plt.plot(composite[:, 0], composite[:, 1], color)
