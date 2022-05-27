from turtle import title, width
from src.import_modules import *


class GlaubenDataVisualization:
    def __init__(self, mode, data):
        self.mode = mode  # 'mpl' o 'plotly'
        self.data = data

    def plotWithScatter(self, x_name, y_name):
        """
          Esta función crea un gráfico de plotly o mpl (especificado en el constructor) de dispersión (Scatter), 
          donde los datos del eje y pueden ser de un array, dataframe, etc. y múltiples de ellos.

          Parámetros
            - x_name: objeto de tipo pd.DataFrame que posee los datos a graficar en el eje x.
            - y_name: objeto de tipo pd.DataFrame que posee los datos a graficar en el eje y.

        """
        if self.mode == "plotly":
            if type(y_name) == list:
                fig = px.scatter(self.data, x=x_name, y=y_name, width=1200, height=600, title=(
                    x_name + " vs " + str(', '.join(y_name))+"."))
            else:
                fig = px.scatter(self.data, x=x_name, y=y_name, width=1200, height=600, title=(
                    x_name + " vs " + y_name+"."))
            fig.update_layout(title_x=0.5)
            fig.update_xaxes(
                tickangle=315,
                title_text=x_name,
                title_font={"size": 20},
                title_standoff=25
            )
            fig.show()

        elif self.mode == "mpl":
            print()
            # TODO
        return

    def plotWithBar(self, y_name=[]):
        """
          Esta función crea un gráfico de plotly o mpl (especificado en el constructor) de barra (bar chart), 
          donde los datos del eje y pueden ser de un array, dataframe, etc. y múltiples de ellos.

          Parámetros
            - y_name: objeto de tipo pd.DataFrame que posee los datos a graficar en el eje y, estos datos serán contados y desplegados en el gráfico.
                      en el caso dejar en blanco, se graficarán todas las columnas del dataframe.

        """
        
        if self.mode == "plotly":
            if type(y_name) == list:
                if len(y_name) == 0:
                    all_data = True
                    y_name = self.data.columns.tolist()
                else:
                    all_data = False
                count_data = []
                x_ticks = np.arange(len(y_name))
                for i in range(len(y_name)):
                    nombre_columna = y_name[i]
                    cantidad = self.data[nombre_columna].notnull().sum()
                    count_data.append(cantidad)
                fig = px.bar(x=y_name, y=count_data, width=1200, height=600, title=("Cantidad no nulos de " + str(', '.join(y_name))+"."), color= y_name)
            else:
                all_data = False
                cantidad = self.data[y_name].notnull().sum()
                nombres = [y_name]
                cantidades = [cantidad]
                fig = px.bar(x=nombres, y=cantidades, width=1200, height=600, title=("Cantidad no nulos de" + y_name+"."))

            if all_data:
                fig.update_layout(title="Cantidad de datos no nulos por columna", title_x=0.5, width=1200, height=800)
                fig.update_xaxes(
                    tickangle=315,
                    title_font={"size": 20},
                    title_standoff=25
                )
            else:
                fig.update_layout(title_x=0.5)
                fig.update_xaxes(
                    tickangle=0,
                    title_font={"size": 20},
                    title_standoff=25
                )
            fig.update_traces(showlegend=False)
            fig.show()

        elif self.mode == "mpl":
            print()
            # TODO
        return

    def plotWithLine(self, x_name, y_name, t_title):
        fig = px.line(self.data, x=x_name, y=y_name, title=t_title)
        fig.update_xaxes(tickangle=-90)
        fig.update_layout(
            title={
                'text': t_title,
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
        fig.show()
        return

    def plotWithBox(self, x_name, y_name, t_title):
        df = self.data
        fig = px.box(df, x=x_name, y=y_name, title=t_title)
        fig.update_xaxes(tickangle=-90)
        fig.update_layout(
            title={
                'text': t_title,
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
        fig.show()
        return

    
