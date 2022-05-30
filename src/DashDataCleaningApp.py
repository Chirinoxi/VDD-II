import io
import os
import locale
import base64
from tkinter import CENTER
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc


from dash_extensions.snippets import send_bytes
from dash import Dash, Input, Output, State, dcc, html, dash_table

H1_STYLE = { 
            "width": "90vw",
            "margin": "1.5rem 1.5rem",
            "padding": "auto",
            "text-align": "center"
            }

BUTTON_STYLE = { 
                "position": "relative",
                "margin": "auto",
                "float" : "center"
                }

CENTERING = {
    "width": "300px",
    "margin": "1.5rem auto",
    "padding": "0",
}

TABLE_STYLE = {
    "margin": "1.5rem",
    "padding": "0"
}

# Variables SDI

important_features = ['Timestamp', 'Day', 'Flujo de rechazo', 'Temperatura entrada', 
                 'Conductividad de permeado', 'Presion de entrada', 'SDI Entrada RO']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
# app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "Demo limpieza"
app.layout = html.Div([

    html.H1("Demo limpieza de datos", style=H1_STYLE),
    html.Hr(),

    html.Div([
        html.P("Este demo tiene como finalidad ejecutar la limpieza de un archivo CSV el cual debe ser subido a esta aplicación."),
        html.Div([
            dcc.Upload(
                id="upload-button",
                children=html.Button('Subir archivo', style=BUTTON_STYLE),
                multiple=False
                ),
        ], style=CENTERING),
    ]),

    html.Hr(),
    html.Div([
        html.H2("Datos ingresados", style=CENTERING),
        dash_table.DataTable(id='raw-data-table')
    ], id="table-container", style=TABLE_STYLE),

    html.Hr(),
    html.Div([
        html.Button('Generar limpieza', style=BUTTON_STYLE)
        ], id="clean-data-container", style=CENTERING)
])

def parse_data(contents, filename):
    try:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        if "csv" in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" or "xlsx" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif "txt" or "tsv" in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), delimiter=r"\s+")
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])
    return df

@app.callback(
    Output("raw-data-table", "data"), 
    Output("raw-data-table", "columns"),
    [Input("upload-button", "contents"), State("upload-button", "filename")],
)
def update_table(contents, filename):
    data, df_columns = [], []
    if contents != None and filename != None:
        try:
            df_data = parse_data(contents, filename)
            df_data = df_data.iloc[:15, :][important_features]
            data = df_data.to_dict('records')
            df_columns = [{'name': i, 'id': i} for i in df_data.columns]
            print("df_columns:", df_columns)
        except Exception as e:
            print("e:", e)
    return (data, df_columns)

if __name__ == '__main__':
    app.run_server(debug=True)