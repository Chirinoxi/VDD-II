from import_modules import *

class GlaubenDataPrep:
  def __init__(self, mode, data_dir):
    self.mode = mode
    self.data_dir = data_dir # C:/Users/ignac/downloads/test.csv
    self.filename = data_dir.split('/')[-1] #TODO: implementar algo con OS

  def loadData(self):
    """
      Función destinada a cargar los datos almacenados en el directorio data_dir.
    """
    data = pd.read_csv(self.data_dir)
    return data

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
    str_colums = ["Timestamp", "Month", "Day"]
    df_columns = [i for i in df_data_orig.columns.tolist() if i not in str_colums]
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