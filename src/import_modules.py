import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
from os.path import join, isdir, isfile, exists, splitext

import math
import logging
import numpy as np
import pandas as pd
from sklearn import linear_model
import multiprocessing as mp, time, ctypes, os
import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
 
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error,\
                            r2_score, mean_absolute_percentage_error

#import tensorflow as tf
#from tensorflow import keras
#from tensorflow.keras.layers import Dense, BatchNormalization,\
#                                    LSTM, Dropout, GRU, SimpleRNN,\
#                                    InputLayer, Conv1D, MaxPooling1D,\
#                                    AveragePooling1D, Flatten
#from tensorflow.keras.regularizers import l1, l2, l1_l2
#from tensorflow.keras.optimizers import Adam, Adagrad, Adamax, Adadelta, SGD, RMSprop
#from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
# import keras_tuner as kt