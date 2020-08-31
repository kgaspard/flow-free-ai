from sklearn.model_selection import train_test_split
from dataParser import parse_files
import numpy as np
import tensorflow as tf
from tensorflow import keras

def process_data_for_training(max_board_size=15):
    problems,solutions = parse_files(max_board_size=max_board_size)
    features=[]
    labels=[]

    features = np.array(problems).reshape(len(problems),max_board_size,max_board_size,1)
    labels = np.array(solutions).reshape(len(solutions),max_board_size,max_board_size,1)
    
    del(problems)
    del(solutions)    

    x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.1, random_state=42)
    return x_train, x_test, y_train, y_test

def get_model(max_board_size=15):

    model = keras.models.Sequential()

    model.add(keras.layers.Conv2D(64, kernel_size=(3,3), activation='relu', padding='same', input_shape=(max_board_size,max_board_size,1)))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Conv2D(64, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Conv2D(128, kernel_size=(1,1), activation='relu', padding='same'))

    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(max_board_size*max_board_size*max_board_size))
    model.add(keras.layers.Reshape((-1, max_board_size)))
    model.add(keras.layers.Activation('softmax'))
    
    return model

def train_model():

    x_train, x_test, y_train, y_test = process_data_for_training()

    model = get_model()

    adam = keras.optimizers.Adam(lr=.001)
    model.compile(loss='sparse_categorical_crossentropy', optimizer=adam)

    model.fit(x_train, y_train, batch_size=32, epochs=2)

    model.save('model_1')

    # model.load('mymodel.model')

train_model()