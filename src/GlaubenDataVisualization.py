from src.import_modules import *

class GlaubenDataVisualization:
  def __init__(self, mode, data):
    self.mode = mode # 'mpl' o 'plotly'
    self.data = data
  
  def plotWithScatter(self, numb_of_series):
    return
  def plotWithLine(self, x_name, y_name, t_title):
    fig = px.line(self.data,x = x_name,y = y_name, title=t_title)
    fig.update_xaxes(tickangle= -90) 
    fig.update_layout(
    title={
        'text': t_title,
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    fig.show()
    return
  def plotWithBox(self, x_name, y_name, t_title):
    df=self.data
    fig = px.box(df,x = x_name,y = y_name, title=t_title)
    fig.update_xaxes(tickangle= -90) 
    fig.update_layout(
    title={
        'text': t_title,
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    fig.show()
    return