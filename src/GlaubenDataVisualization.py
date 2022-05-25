from import_modules import *

class GlaubenDataVisualization:
  def __init__(self, mode, data):
    self.mode = mode # 'mpl' o 'plotly'
    self.data = data
  
  def plotWithScatter(self, numb_of_series):
    return