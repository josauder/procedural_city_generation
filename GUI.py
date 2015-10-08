import sys
from window import *
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
matplotlib.use("QT4Agg")
from matplotlib.figure import Figure
import UI

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s



class GUI(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        sys.stdout=StdoutRedirector(self.ui.console)


        #### 1: ROADMAP ####
        UI.setRoadmapGUI(self)
        self.ui.roadmap_widget.hide()
        self.ui.roadmap_Run.clicked.connect(self.start_roadmap)
        
        
        #### 2: POLYGONS ####
        UI.setPolygonsGUI(self)
        self.ui.polygons_widget.hide()
        self.ui.polygons_Run.clicked.connect(self.start_polygons)
        
        #### 3: BUILDING_GENERATION ####
        self.ui.building_generation_Run.clicked.connect(UI.building_generation)
        
        #### 4: VISUALIZATION ####
        self.ui.visualization_Run.clicked.connect(UI.visualization)

        
    def plot(self,x,y,linewidth=1,color="red"):
        self.active_widget.canvas.ax.plot(x,y,linewidth=linewidth,color=color)
       
    def clear(self):
        self.active_widget.canvas.ax.clear()
                
    def start_roadmap(self):
        self.active_widget=self.ui.roadmap_widget
        self.active_widget.show()
        self.clear()
        UI.roadmap()
        
    def start_polygons(self):
        self.active_widget=self.ui.polygons_widget
        self.active_widget.show()
        self.clear()
        UI.polygons()
        
    def set_xlim(self,tpl):
        self.active_widget.canvas.ax.set_xlim(tpl)
        
    def set_ylim(self,tpl):
        self.active_widget.canvas.ax.set_ylim(tpl)
        
    def update(self):
        self.active_widget.canvas.draw()
        global app
        app.processEvents()


class FigureSaver:
	class __FigureSaver:
		def __init__(self, fig=None):
			self.plot=fig.plot
			self.show=fig.show
	instance=None
	
	def __init__(self,fig=None):
		if not FigureSaver.instance and (fig is not None):
			print "inst",FigureSaver.instance, fig
			FigureSaver.instance=FigureSaver.__FigureSaver(fig)
			

	def __getattr__(self,name):
		return getattr(self.instance,name)
		
	def __setattr__(self,name,value):
		setattr(self.instance,name,value)	

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


class StdoutRedirector:
	"""
	Redirects all "print" outputs from Terminal into the Tkinter window
	that is given as constructor.
	"""
	def __init__(self,label_obj):
		"""
		Parameters
		----------
		label_obj : Tkinter-Object with config method
			Any Tkinter Object whose text can be changed over label_obj.config(text=String)
		"""
		self.label_obj=label_obj
		
		
	def write(self,out):
		"""
		Method to be called by sys.stdout when text is written by print.
		
		Parameters
		----------
		out : String
			Text to be printed
		"""
		self.label_obj.insertPlainText(out)
		global app
		app.processEvents()
		


if __name__ == "__main__":
    global app
    app = QtGui.QApplication(sys.argv)
    myapp = GUI()
    myapp.show()
    app.exec_()
