from src.import_modules import *

class GlaubenDataModeling:

    def __init__(self, data):
        """ Constructor de la clase GlaubenDataModeling.

            Parámetros:
              - data: Lista de dataframes con los datos de cada planta para el modelado de datos.
        """
        self.data = data

        self.X
        self.y
        self.X_normalized = None
        self.model = None

        # Conjuntos de datos para entrenamiento.
        self.X_train = []
        self.X_val   = []
        self.X_test  = []

        self.y_train = []
        self.y_val   = []
        self.y_test  = []

    def createModel(self, name):
        # TODO: Creamos modelo con respecto al nombre entregado por parámetro.
        self.model = tf.keras.Sequential()
        # TODO: Agregar capas dependiendo de modelo seleccionado.
        return

    def normalizeData(normalization_name: str):
        # TODO: Implementar clausula if para crear los objetos Scaler,
        # dependiendo del valor de normalization_name y retornamos los datos normalizados.
        X_norm = []
        return X_norm

    def trainModel(epochs: int, b_size: int, learning_rate: float, callbacks: list, optimizer_name: str, cv=True):
        """
          Función que se encarga de entrenar nuestro modelo neuronal. Puede implementarse
          cross-validation con el parámetro cv.

          Retorna:
            - model: tf.keras....

        """
        # Implementar clausula if para los casos en los que se desee implementar CV o no.
        # self.model.fit()
        return

    def loadWeights(model_weights_dir):
        # self.model.load_weights(model_weights_dir)
        return

    def saveModel(model_dir: str):
        # self.model.save(model_dir)
        return
