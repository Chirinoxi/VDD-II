from turtle import title
from src.import_modules import *

class GlaubenDataVisualization:
  def __init__(self, mode, data):
    self.mode = mode # 'mpl' o 'plotly'
    self.data = data
  
  def plotWithScatter(self, x_name, y_name):
    if self.mode == "plotly":
      if type(y_name) == list: 
        fig = px.scatter(self.data, x=x_name, y=y_name, width=1200, height=600, title= (x_name + " vs " + str(', '.join(y_name))+"."))  
      else:
        fig = px.scatter(self.data, x=x_name, y=y_name, width=1200, height=600, title= (x_name + " vs " + y_name+"."))
      fig.update_layout(title_x=0.5)
      fig.update_xaxes(
        tickangle = 315,
        title_text = "Días",
        title_font = {"size": 20},
        title_standoff = 25
      )
      fig.show()
        
    elif self.mode == "mpl":
      print()
      #TODO
    return
