from cgi import print_environ
from src.import_modules import *


class GlaubenDataPrep:

    def __init__(self, data_dir, feature='None'):
        """
            Constructor para asignar el objevo tipo pd.DataFrame y que característica se hara predicción (Para solo tomar las columnas necesarias para )

            Parámetros
            - mode: variable tipo string que determinará qué gráfico se desplegará (mpl o plotly)
            - data: objeto de tipo pd.DataFrame que posee los datos
        """
        self.data_dir = data_dir  # C:/Users/ignac/downloads/test.csv
        # TODO: implementar algo con OS
        self.filename = data_dir.split('/')[-1]
        self.data = None
        self.clean_data = None
        self.feature = feature

    def splitTimestamp(self, timestamp):
        splitted_timestamp = timestamp.split(' ')
        return splitted_timestamp[0]

    def addDayColum(self):
        data_cols = self.data.columns
        if ("Day" not in data_cols):
            self.data['Day'] = self.data['Timestamp'].apply(
                self.splitTimestamp)
        return

    def removeAccents(self, input_string):
        """Removemos tíldes ....."""
        formatted_string = unidecode.unidecode(input_string)
        return formatted_string

    def removeUndesiredStrings(self, undesired_strings: list):
        _col_names = []
        col_names = self.data.columns.tolist()
        for col_name in col_names:
            for _string in undesired_strings:
                if (_string is not None) and search(_string, col_name):
                    _col_name = col_name.replace(_string, "")
                    _col_name = self.removeAccents(_col_name)
                    break
                else:
                    _col_name = col_name
            _col_names.append(_col_name)
        print(_col_names)
        self.data.columns = _col_names
        return

    def loadData(self):
        """
          Función destinada a cargar los datos almacenados en el directorio data_dir.
        """
        encodings = ['utf-8', 'latin']
        for encode in encodings:
            try:
                self.data = pd.read_csv(self.data_dir, encoding=encode)
            except Exception as e:
                print("Exception:", e)
        return

    def dropNaNValues(self):
        """
          Función destinada a eliminar los valores NaN de nuestros datos.
        """
        self.data = self.data.dropna()
        return

    def filterByGauss(self, df_data_orig: pd.DataFrame, n_desv_est: int):
        """
          Esta función ejecuta una limpieza de los datos de entrada mediante una distribución normal.
          Cabe destacar que esta limpieza se realiza por cada columna existente en la variable df_data_orig y
          elimina una fila completa en caso de que un dato se encuentre fuera del rango establecido.

          Parámetros
            - df_data_orig: objeto de tipo pd.DataFrame que posee los datos originales.
            - n_desv_est: número de desviaciones estándar a utilizar.

          Retorna:
            - result_df: objeto de tipo pd.DataFrame que posee los datos "limpios".
        """
        orig_cols = df_data_orig.columns.tolist()
        str_colums = ["Timestamp", "Month", "Day",
                      "Tipo Operacion", "Nombre planta"]
        df_columns = [i for i in orig_cols if i not in str_colums]
        result_df = df_data_orig.copy(deep=True)

        for col in df_columns:
            col_df = result_df[col].copy(deep=True)
            col_mean = round(np.mean(col_df), 4)  # Obtenemos promedio
            col_std = round(np.std(col_df), 4)  # Obtenemos desviación estándar
            lower_limit = col_df > col_mean - n_desv_est * col_std
            upper_limit = col_df < col_mean + n_desv_est * col_std
            between_gauss = lower_limit & upper_limit
            # Esto genera que el DF no sea 'cuadrado' !
            # result_df[col] = col_df[between_gauss]
            # La siguiente línea asegura que el dataset sea simétrico !
            delete_indexes = between_gauss[~between_gauss].index.values
            print(len(delete_indexes))
            print(col)
            result_df = result_df.drop(delete_indexes, axis=0)
        return result_df


    def filterByIQR(self, df_data_orig: pd.DataFrame, filter_cols: list, n_desv_est: int):
        """
            Esta función ejecuta una limpieza de los datos de entrada mediante una distribución normal.
            Cabe destacar que esta limpieza se realiza por cada columna existente en la variable df_data_orig y
            elimina una fila completa en caso de que un dato se encuentre fuera del rango establecido.

            Parámetros
                - df_data_orig: objeto de tipo pd.DataFrame que posee los datos originales.
                - filter_cols; corresponde a una lista de python que contiene las variables que deseamos utilizar para el filtrado.
                - n_desv_est: número de desviaciones estándar a utilizar.

            Retorna:
                - result_df: objeto de tipo pd.DataFrame que posee los datos "limpios".
            """
        orig_cols = df_data_orig.columns.tolist()
        str_colums = ["Timestamp", "Month", "Day",
                      "Tipo Operacion", "Nombre planta"]
        df_columns = [i for i in filter_cols if i not in str_colums]
        result_df = df_data_orig.copy(deep=True)
        for col in df_columns:
            col_df = result_df[col].copy(deep=True)
            col_df = col_df.sort_values(ascending=True)
            col_q2 = col_df.median()
            col_q1, col_q3 = col_df.quantile(0.25), col_df.quantile(0.75)
            # Calculamos IQR y los límites siperior e inferior.
            col_IQR = col_q3 - col_q1
            sup_lim = col_q3 + col_IQR * 1.5
            inf_lim = col_q1 - col_IQR * 1.5
            lower_limit = col_df > inf_lim
            upper_limit = col_df < sup_lim
            between_range = lower_limit & upper_limit
            # Esto genera que el DF no sea 'cuadrado' !
            # result_df[col] = col_df[between_range]
            # La siguiente línea asegura que el dataset sea simétrico !
            delete_indexes = between_range[~between_range].index.values
            result_df = result_df.drop(delete_indexes, axis=0)
        return result_df

    def generateSet(self, feature_names):
        """
            Función para obtener un pd.DataFrame con las columnas especificadas por parámetro.
            Parámetros
            - feature_names: Variable tipo String que posee las columnas deseadas del DataFrame
        """
        df_result = self.clean_data[feature_names]
        return df_result

    def desiredColumns(self, desiredColum):
        self.data = self.data[desiredColum]
        return 