from platform import platform
from turtle import title, width
from src.import_modules import *


class GlaubenDataVisualization:
    """
        Constructor para asignar el objevo tipo pd.DataFrame y qué gráfico se mostrará (mpl o plotly)

        Parámetros
          - mode: variable tipo string que determinará qué gráfico se desplegará (mpl o plotly)
          - data: objeto de tipo pd.DataFrame que posee los datos
    """
    def __init__(self, mode, data):
        self.mode = mode  # 'mpl' o 'plotly'
        self.data = data

    def plotWithScatter(self, x_name, y_name, sep=1):
        """
          Esta función crea un gráfico de plotly o mpl (especificado en el constructor) de dispersión (Scatter), 
          donde los datos del eje y pueden ser de un array, dataframe, etc. y múltiples de ellos.

          Parámetros
            - x_name: objeto de tipo pd.DataFrame que posee los datos a graficar en el eje x.
            - y_name: objeto de tipo pd.DataFrame que posee los datos a graficar en el eje y.
            - sep:    variable de tipo int que separará los datos en el eje x en caso de utilizar mpl.

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
            xpos = np.arange(0, len(self.data[x_name]), sep)
            plt.figure(figsize=(12,6))
            ax, fig = plt.gca(), plt.gcf()
            if type(y_name) == list:
                for i in range(len(y_name)):
                    fig = plt.scatter(x=self.data[x_name], y=self.data[y_name[i]], s=15, alpha=0.3,
                        label=y_name[i], edgecolor='white', c=('C'+str(i)))
                ax.set_title(x_name + " vs " + str(', '.join(y_name)) +".")
            else:
                fig = plt.scatter(x=self.data[x_name], y=self.data[y_name], s=15, alpha=0.3, c='C3',
                    label=y_name, edgecolor='white')
                ax.set_title(x_name + " vs " + y_name+".")
            ax.set_xlabel(x_name)
            ax.set_ylabel('Valor')
            plt.xticks(xpos)
            plt.grid(True, linestyle=':')
            ax.set_axisbelow(True)
            plt.xticks(rotation = 45)
            ax.legend(loc='lower right', bbox_to_anchor=(1.37, 0.0))
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
                for i in range(len(y_name)):
                    nombre_columna = y_name[i]
                    cantidad = self.data[nombre_columna].notnull().sum()
                    count_data.append(cantidad)
                fig = px.bar(x=y_name, y=count_data, width=1200, height=600, title=(
                    "Cantidades no nulas de todas las columnas."), color=y_name)
            else:
                all_data = False
                cantidad = self.data[y_name].notnull().sum()
                nombres = [y_name]
                cantidades = [cantidad]
                fig = px.bar(x=nombres, y=cantidades, width=1200, height=600, title=(
                    "Cantidad no nulos de" + y_name+"."))

            if all_data:
                fig.update_layout(title="Cantidad de datos no nulos por columna",
                                  title_x=0.5, width=1200, height=800, title_font={"size": 25})
                fig.update_xaxes(
                    tickangle=315,
                    title_font={"size": 20},
                    title_standoff=25,
                    title_text='Columnas'
                )
            else:
                fig.update_layout(title_x=0.5)
                fig.update_xaxes(
                    tickangle=0,
                    title_font={"size": 20},
                    title_standoff=25,
                    title_text='Columna',
                )
            fig.update_yaxes(
                title_font={"size": 20},
                title_standoff=25,
                title_text='Cantidades'
            )
            fig.update_traces(showlegend=False)
            fig.show()

        elif self.mode == "mpl":
            if type(y_name) == list:
                if len(y_name) == 0:
                    all_data = True
                    y_name = self.data.columns.tolist()
                else:
                    all_data = False
                plt.figure(figsize=(12,6))
                ax, fig = plt.gca(), plt.gcf()
                count_data = []
                colores = []
                for i in range(len(y_name)):
                    nombre_columna = y_name[i]
                    cantidad = self.data[nombre_columna].notnull().sum()
                    count_data.append(cantidad)
                    colores.append('C'+str(i)) 
                if all_data:
                    ax.set_title('Cantidad de no nulos de todas la columnas.', fontsize=18)
                else:
                    ax.set_title('Cantidad de no nulos de columnas seleccionadas.', fontsize=18)
                ax.set_xlabel('Cantidades', fontsize=13)
                ax.set_ylabel('Columnas', fontsize=13)
                ax.barh(y_name, count_data, alpha=0.5, color=colores, align='center')
                    
            else:
                plt.figure(figsize=(6,6))
                ax, fig = plt.gca(), plt.gcf()
                cantidad = self.data[y_name].notnull().sum()
                nombres = [y_name]
                cantidades = [cantidad]
                ax.barh(nombres, cantidades, alpha=0.5, color='C3', align='center')
                ax.set_title('Cantidad de no nulos de '+y_name, fontsize=18)
                ax.set_xlabel('Cantidad', fontsize=13)
                ax.set_ylabel('Columna', fontsize=13)
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

    def subPlots(self, y_name, type='scatter'):
        """
        Función para graficar multiples columnas al mismo tiempo, el tipo de gráfico será determinado por la variable type.
        Se recomienda graficar 6 o menos gráficos.

        Parámetros
            - y_name: variable tipo lista, que contiene los valores de las columnas para graficar.
            - type:   variable tipo String, que contiene el tipo de gráfico a utilizar.
        """
        size = len(y_name)/2
        size = math.ceil(size)
        fig_size_x = size*10
        fig_size_y = size*4
        if len(y_name) == 2:
            size = 2
            fig_size_x = 18
            fig_size_y = 6
        plt.figure(figsize=(fig_size_x, fig_size_y))
        for i in range(len(y_name)):
            curr_feature = y_name[i]
            data = self.data[curr_feature]
            x = np.arange(0, len(data))
            plt.subplot(size, size, i+1)
            if(type == 'scatter'):
                plt.scatter(x, data, s=15, alpha=0.4,
                            label=curr_feature, edgecolor='white',
                            linewidths=0.25, c='C{}'.format(i))
            elif(type == 'line'):
                plt.plot(x, data, alpha=0.4,
                            label=curr_feature, c='C{}'.format(i))
            ax = plt.gca()
            ax.set_axisbelow(True)
            ax.grid(True, linestyle='-.', alpha=0.6)
            ax.legend(loc='upper left')
            ax.set_xlabel('Enumeración')
            ax.set_ylabel(curr_feature)
            ax.set_title(curr_feature)
        fig = plt.gcf()
        #filename = 'Scatter plots 4 variables post limpieza.png'
        #filename = join(figures_dir, filename)
        #fig.savefig(filename, format='png', bbox_inches="tight",
        #            transparent=False, dpi=300)
        plt.subplots_adjust(bottom=0.0, top=1.4)
        plt.show()
        return