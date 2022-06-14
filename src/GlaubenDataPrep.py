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
        self.data_dir = data_dir  # C:/Users/ignac/downloads/test.csv 'C:/Users/apa/Documents/Glauben ecology/Vertientes del desierto II/Data/Originales/Planta RO2 (Kilopaskales).csv'
        # TODO: implementar algo con OS
        self.filename = data_dir.split('/')[-1]
        self.data = None
        self.clean_data = None
        if feature == 'SDI':
            self.mode = 'SDI'
            self.feature = ['Timestamp', 'Day',
                            'Temperatura entrada',
                            'Flujo de Alimentacion',
                            'Presion de entrada',
                            'Conductividad de entrada',
                            'SDI Entrada RO']
        elif feature == 'FN':
            self.mode = 'FN'
            self.feature = ['Timestamp', 'Day',
                            'Conductividad de entrada',
                            'Flujo de Alimentacion',
                            'Presion de entrada',
                            'Flujo normalizado',
                            'pH entrada']
        else:
            self.feature = feature
            self.mode = 'None'

    def splitTimestamp(self, timestamp):
        """
            Función que separa la fecha de las horas, minutos y segundos, donde solo se tendría día, mes y año

            Parámetros
                - timestamp: Variable tipo string, que tendrá la fecha a separar (Date con formato String)
        """
        try:
            splitted_timestamp = timestamp.split(' ')
            return splitted_timestamp[0]
        except Exception as e:
            print("Exception split:", e)
        return


    def addDayColum(self):
        """
            Función que agrega la columna day, que contiene el día, mes y año que se obtiene de la función splitTimestamp
        """
        data_cols = self.data.columns
        if ("Day" not in data_cols):
            try:
                self.data['Day'] = self.data['Timestamp'].apply(self.splitTimestamp)
                pass
            except Exception as e:
                print("Exception:", e)
                
            try:
                self.data['Timestamp'] = self.data['Timestamp'].astype('datetime64[ns]')
                self.data['Timestamp'] = self.data['Timestamp'].apply(lambda x: x.strftime('%d/%m/%Y %H:%M:%S'))
                self.data['Day'] = self.data['Timestamp'].apply(
                    self.splitTimestamp)
            except Exception as e:
                print("Exception:", e)
        return


    def removeAccents(self, input_string):
        """
            Función para remover tíldes .....

            Parámetros
                - input_string: Variable tipo string que contiene la variable para remover los tildes.

            Return
                - El string sin los tildes
        """
        formatted_string = unidecode.unidecode(input_string)
        return formatted_string

    def removeUndesiredStrings(self, undesired_strings: list):
        """
            Removemos los strings iniciales de cada columna, se le entrega una lista que contiene los posibles strings

            Parámetros:
                - undesired_strings: Variable tipo lista, que contendrá los strings iniciales a remover.
        """
        #Todos los strings de las plantas que se han entregado.
        #'Planta 3 - Rack 9-','Planta 1 - Rack 1-', 'Planta 1 - Filtros 1er Etapa-', 'dd','Rack2-', 'Planta 0 - Filtros Cartucho-',
        #'Planta 0 - Filtros 1era Etapa-', 'Rack1-', 'Rack2-', 'Rack 1-', 'Rack1-', 'Planta 0 - Filtros Cartucho-', 'Planta 3 - Rack 9-'  
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
        self.data.columns = _col_names
        return

    def loadData(self):
        """
            Función destinada a cargar los datos almacenados en el directorio data_dir. El cual intentará con csv enconding etf-8, latin y con excel.
        """
        encodings = ['utf-8', 'latin']
        for encode in encodings:
            try:
                self.data = pd.read_csv(self.data_dir, encoding=encode)
                break
            except Exception as e:
                print("Exception:", e)
        try:
            self.data = pd.read_excel(self.data_dir, engine='openpyxl')
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
            #print(len(delete_indexes))
            #print(col)
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
            Función para obtener un pd.DataFrame con las columnas especificadas por parámetro de data.

            Parámetros
                - feature_names: Variable tipo String que posee las columnas deseadas del DataFrame
        """
        df_result = self.data[feature_names]
        return df_result

    def checkFeatures(self):
        """
            Revisa las columnas del dataframe, en caso de no tener flujo de alimentacion, pero tiene flujo de permeado
            y de rechazo, se calcula y se agrega la columna flujo de alimentacion. En caso no no estar SDI Entrada RO,
            pero se encuentra SDI Entrada, se le cambia el nombre por el respectivo.
            Si el promedio de la presión es menor a 1000, entonces corresponde a bar, por lo que se multiplica por 100
            para dejarlo en KPa.
        """
        dataCols = self.data.columns
        meanPresion = self.data['Presion de entrada'].mean()
        if not 'Flujo de Alimentacion' in dataCols:
            if 'Flujo de permeado' in dataCols and 'Flujo de rechazo' in dataCols:
                flujoAlimentacion = self.data['Flujo de permeado'] + self.data['Flujo de rechazo']
                self.data['Flujo de Alimentacion'] = flujoAlimentacion
        if 'SDI Entrada' in dataCols:
            columnDict = { 'SDI Entrada': 'SDI Entrada RO' }
            self.data.rename(columns = columnDict, inplace = True)
        if meanPresion < 1000:
            self.data['Presion de entrada'] = self.data['Presion de entrada']*100
        return

    def filterData(self, col, limInf, limSup):
        """
            Función para filtrar datos de columna entre un rango superior y uno inferior.
        """
        condicion = (self.clean_data[col] > limInf) & (self.clean_data[col] < limSup)
        self.clean_data = self.clean_data[condicion]
        return

    def prepData(self, limSuperior=0, limInferior=0.5):
        """
            función para preparar dataframes de forma semi-automática, ya que en caso de ser necesario se debe especificar
            el límite inferior para el filtrado de datos.

            Parámetros:
                - limSuperior: Variable tipo int que deberá tener en caso de ser necesario el límite superior para filtrar
                la data
                - limInferior: Variable tipo int que deberá tener en caso de ser necesario el límite inferior para filtrar
                la data
        """
        #SDI planta 2 y planta RO1 deben tener limite inferior de 1.8
        self.loadData()
        self.removeUndesiredStrings(['Planta 3 - Rack 9-','Planta 1 - Rack 1-', 'Planta 1 - Filtros 1er Etapa-', 'dd','Rack2-', 'Planta 0 - Filtros Cartucho-',
                                    'Planta 0 - Filtros 1era Etapa-', 'Rack1-', 'Rack2-', 'Rack 1-', 'Rack1-', 'Planta 0 - Filtros Cartucho-', 'Planta 3 - Rack 9-'])
        self.addDayColum()
        self.checkFeatures()
        self.clean_data = self.generateSet(self.feature)
        self.dropNaNValues()
        if self.mode == 'SDI':
            self.filterData(col = 'SDI Entrada RO', limInf = limInferior, limSup=15)
        elif self.mode == 'FN':
            if limSuperior != 0:
                self.filterData(col = 'Flujo normalizado', limInf = 0, limSup=limSuperior)
        self.clean_data = self.filterByGauss(self.clean_data, 3)
        return
