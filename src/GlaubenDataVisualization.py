from re import X
from sys import _xoptions

from pkg_resources import safe_extra
from src.import_modules import *


class GlaubenDataVisualization:
    def __init__(self, mode, data):
        self.mode = mode  # 'mpl' o 'plotly'
        self.data = data

    def plotWithScatter(self, numb_of_series):
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
# elif self.mode == 'mpl':

    def mplWithPlot(self, x_name, y_name, sep=1500):
        x_data = self.data[x_name]
        y_data = self.data[y_name]

        plt.figure(figsize=(12, 6))
        plt.plot(x_data, y_data, label=y_name)
        ax = plt.gca()
        ax.set_title(y_name, fontsize=13, pad=10)
        ax.legend(loc='upper right', fontsize=13, bbox_to_anchor=(1.28, 1.0))
        ax.set_xlabel(x_name)
        ax.set_ylabel(y_name)
        ax.grid(True, linestyle=':')
        ax.set_axisbelow(True)
        jump = len(x_data) // sep
        xlabels = x_data[::jump]
        ax.set_xticklabels(labels=xlabels, rotation=45, fontsize=13)
        xpos = np.arange(0, len(x_data), sep)
        plt.xticks(xpos)
        plt.show()
        return

    def mpltWithBox(self, x_name, y_name):
        df = self.data
        plt.figure(figsize=(30, 15))
        ax = sns.boxplot(x=x_name, y=y_name, data=df)
        ax.set_title(y_name, fontsize=13, pad=10)
        ax.margins(x=0.9)
        ax.grid(True, linestyle=':')
        ax.set_axisbelow(True)
        # Obtenemos las etiquetas actuales de nuestro gráfico
        x_labels = ax.get_xticklabels()
        ax.set_xticklabels(labels=x_labels, rotation=90, fontsize=13)
        plt.show()
        return

    def matrizDeCorr(self, c_corr=[]):
        if len(c_corr) == 0:
            df_data = self.data
        else:
            df_data = self.data[c_corr]
        corr = df_data.corr()
        plt.figure(figsize=(15, 8))
        sns.heatmap(corr, annot=True, fmt='.2f', cbar=False)
        title = ('Correlaciones para datos')
        plt.suptitle(title, fontsize=18)

        plt.show()
