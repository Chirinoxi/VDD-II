import io
import os
import locale
import base64
from tkinter import CENTER
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc

from GlaubenDataPrep import GlaubenDataPrep

from dash_extensions.snippets import send_bytes
from dash import Dash, Input, Output, State, dcc, html, dash_table

df_original = pd.DataFrame([])

H1_STYLE = { 
            "width": "90vw",
            "margin": "1.5rem auto",
            "padding": "2px 0",
            "text-align": "center"
            }

BUTTON_STYLE = { 
                "position": "relative",
                }

CENTERING = {
    "width": "600px",
    "margin": "1.5rem auto",
    "padding": "5px 0",
    "text-align": "center"
}

TABLE_STYLE = {
    "margin": "1.5rem",
    "padding": "0"
}

# Variables SDI

important_features = ['Timestamp', 'Day', 'Flujo de rechazo', 'Temperatura entrada', 
                    'Conductividad de permeado', 'Presion de entrada', 'SDI Entrada RO']

# -------------------------- Archivos de datos -----------------------

df_raw_data = pd.DataFrame(columns = [])
df_clean_data = pd.DataFrame(columns = [])

data_dir = ''
glauben_data_prep = GlaubenDataPrep(data_dir)

# --------------------------------- ° ---------------------------------

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

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
        html.Button('Generar limpieza', style=BUTTON_STYLE, id="clean-data-button"),
        dcc.Download(id="download-cleaned-data"),
        ], id="clean-data-container", style=CENTERING),

    # Elemento para compartir datos entra callbacks (evitar utilizar variables globales).
    dcc.Store(id='original-data-file')
])

def parse_data(contents, filename):
    try:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        print("content_type:", content_type)
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
    Output("original-data-file", "data"),
    [Input("upload-button", "contents"), State("upload-button", "filename")],
)
def update_table(contents, filename):
    data, df_columns = [], []
    df_raw_data = pd.DataFrame([])
    if contents != None and filename != None:
        try:
            df_raw_data = parse_data(contents, filename)
            df_data = df_raw_data.copy(deep=True).iloc[:15, :][:6]
            data = df_data.to_dict('records')
            df_columns = [{'name': i, 'id': i} for i in df_data.columns]
        except Exception as e:
            print("e:", e)
    return (data, df_columns, df_raw_data.to_json(orient='split'))

@app.callback(
    Output("download-cleaned-data", "data"),
    [Input("clean-data-button", "n_clicks"),
     Input("original-data-file", "data")],
    prevent_initial_call=True,
)
def clean_data(n_clicks, json_data):
    print("n_clicks:", n_clicks)
    if n_clicks != None:
        df_data = pd.read_json(json_data, orient='split')
        df_clean_data = glauben_data_prep.filterByGauss(df_data, n_desv_est=3)
        #df_clean_data_csv = df_clean_data.to_csv(index=False)
        #print("df_clean_data_csv:", df_clean_data_csv)
        dictionary = dcc.send_data_frame(df_clean_data.to_csv, "Datos-Limpios.csv")
        return dictionary
    return

if __name__ == '__main__':
    app.run_server(debug=True)