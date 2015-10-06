import sys
from window import *
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class GUI(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.roadmap_Run.clicked.connect( self.PlotFunc)

    def Plot_in_GUI(self,x,y,linewidth=1,color="red"):
        self.ui.roadmap_widget.canvas.ax.plot(x,y,linewidth,color)
        self.ui.roadmap_widget.canvas.draw()




class MplCanvas(FigureCanvas):

    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class matplotlibWidget(QtGui.QWidget):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = GUI	()
    myapp.show()
    sys.exit(app.exec_())
