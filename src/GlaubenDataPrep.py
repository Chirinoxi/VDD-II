from src.import_modules import *


class GlaubenDataPrep:

    def __init__(self, data_dir):
        self.data_dir = data_dir  # C:/Users/ignac/downloads/test.csv
        # TODO: implementar algo con OS
        self.filename = data_dir.split('/')[-1]
        self.data = None
        self.clean_data = None

    def splitTimestamp(self, timestamp):
        splitted_timestamp = timestamp.split(' ')
        return splitted_timestamp[0]

    def addDayColum(self):
        data_cols = self.data.columns
        if ("Day" not in data_cols):
            self.data['Day'] = self.data['Timestamp'].apply(
                self.splitTimestamp)
        return

    def loadData(self):
        """
          Función destinada a cargar los datos almacenados en el directorio data_dir.
        """
        self.data = pd.read_csv(self.data_dir)
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
            result_df = result_df.drop(delete_indexes, axis=0)
        return result_df

    def filterByIQR():
        # TODO: implementar limpieza por rango IQR.
        result_df = ''
        return result_df
