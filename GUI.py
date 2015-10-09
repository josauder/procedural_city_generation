import sys
from window import *
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
matplotlib.use("QT4Agg")
from matplotlib.figure import Figure
import UI
import json

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
        
        self.createTable("roadmap")
        self.ui.roadmap_table.hide()
        self.ui.roadmap_Options.clicked.connect(self.ui.roadmap_table.show)
        self.ui.roadmap_Options.clicked.connect(self.ui.roadmap_save_button.show)
        self.ui.roadmap_save_button.clicked.connect(self.saveOptions)
        #### 2: POLYGONS ####
        UI.setPolygonsGUI(self)
        self.ui.polygons_widget.hide()
        self.ui.polygons_Run.clicked.connect(self.start_polygons)
        
        #### 3: BUILDING_GENERATION ####
        self.ui.building_generation_Run.clicked.connect(UI.building_generation)
        
        #### 4: VISUALIZATION ####
        self.ui.visualization_Run.clicked.connect(UI.visualization)
    def saveOptions(self,submodule="roadmap"):
        #button=getattr(self.ui,submodule+"_save_button")
        self.ui.roadmap_save_button.hide()        
#        table=getattr(self.ui,submodule+"_table")
        self.ui.roadmap_table.hide()
     #   return saver
            
    def createTable(self,submodule):
        with open("procedural_city_generation/inputs/"+submodule+".conf",'r') as f:
            wb=json.loads(f.read())
        table=QtGui.QTableWidget(getattr(self.ui,submodule+"_frame"))
        save_button=QtGui.QPushButton(getattr(self.ui,submodule+"_frame"), text="Save")
        w=881
        h=400
        save_button.setGeometry(QtCore.QRect(w-100, h, 100, 31))
        save_button.hide()
        table.setGeometry(QtCore.QRect(0,0,w,h))        
        table.setColumnCount(4)
        table.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("Parameter Name"))
        table.setColumnWidth(0, int(0.2*w))
        table.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Description"))
        table.setColumnWidth(1, int(0.5*w))
        table.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem("Default Value"))
        table.setColumnWidth(2, int(0.125*w))
        table.setHorizontalHeaderItem(3, QtGui.QTableWidgetItem("Value"))
        table.setColumnWidth(3, int(0.125*w))
        table.setRowCount(len(wb.keys()))
        
        parammodule=__import__("procedural_city_generation."+submodule+"."+submodule+"_params",globals(),locals(),["params"])
        params=parammodule.params
        i=0
        for parameter in params:
             g=QtGui.QTableWidgetItem(str(parameter.name) )
             g.setFlags( g.flags() & ~QtCore.Qt.ItemIsEditable )
             g.setBackground(QtGui.QBrush(QtGui.QColor(235, 235, 235)))
             table.setItem( i, 0 , g)
             
             g=QtGui.QTableWidgetItem(str(parameter.description))
             g.setFlags( g.flags() & ~QtCore.Qt.ItemIsEditable)
             g.setBackground(QtGui.QBrush(QtGui.QColor(235, 235, 235)))
             table.setItem( i, 1 , g)
             
             g=QtGui.QTableWidgetItem(str(parameter.default))
             g.setFlags( g.flags() & ~QtCore.Qt.ItemIsEditable)
             g.setBackground(QtGui.QBrush(QtGui.QColor(235, 235, 235)))
             table.setItem( i, 2 , g)
             
             g=QtGui.QTableWidgetItem(str(wb[parameter.name]))
             table.setItem( i, 3 , g)
             i+=1
        setattr(self.ui,submodule+"_table",table)
        setattr(self.ui,submodule+"_save_button",save_button)
        
    def plot(self,x,y,linewidth=1,color="red"):
        self.active_widget.canvas.ax.plot(x,y,linewidth=linewidth,color=color)
       
    def clear(self):
        self.active_widget.canvas.ax.clear()
                
    def start_roadmap(self):
        self.ui.roadmap_table.hide()
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
