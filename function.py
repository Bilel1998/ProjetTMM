from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as figureCanvas

def makeFigure(layout): #permet d'afficher une figure a un widget
    fig = Figure()
    canvas = figureCanvas(fig)
    layout.addWidget(canvas)
    canvas.draw()
    return fig



