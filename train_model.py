from sklearn.model_selection import train_test_split
from dataParser import parse_files
import numpy as np
import tensorflow as tf
from util import normalize_array,denormalize_array
from tensorflow import keras
import gpu

def process_data_for_training(max_board_size=15):
    problems,solutions = parse_files(max_board_size=max_board_size)
    features=[]
    labels=[]
    
    features = np.array(problems).reshape(len(problems),max_board_size,max_board_size,1)
    max_val = np.max(problems)
    features = normalize_array(features,max_val)

    labels = np.array(solutions).reshape(len(solutions),max_board_size*max_board_size,1)
    labels += 1 # add 1 to account for empty cells being represented by -1, not 0

    del(problems)
    del(solutions)    

    x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.05, random_state=42)
    return x_train, x_test, y_train, y_test, max_val

def get_model(max_board_size=15, max_number_of_colours=15):

    model = keras.models.Sequential()

    model.add(keras.layers.Conv2D(64, kernel_size=(3,3), activation='relu', padding='same', input_shape=(max_board_size,max_board_size,1)))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Conv2D(64, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Conv2D(128, kernel_size=(1,1), activation='relu', padding='same'))

    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(max_board_size*max_board_size*(max_number_of_colours+2)))
    model.add(keras.layers.Reshape((-1, (max_number_of_colours+2))))
    model.add(keras.layers.Activation('softmax'))
    
    return model

def train_model(epochs=2, model_name='model_1'):

    x_train, x_test, y_train, y_test, max_val = process_data_for_training()

    model = get_model(max_number_of_colours=max_val)

    adam = keras.optimizers.Adam(lr=.001)
    model.compile(loss='sparse_categorical_crossentropy', optimizer=adam)

    model.fit(x_train, y_train, batch_size=32, epochs=epochs)

    model.save(model_name)

def solve_game_sequentially(game,max_board_size=15, max_number_of_colours=15, model_name='model_1'):
    model = keras.models.load_model(model_name)
    while(1):
        out = model.predict(game.reshape((1,max_board_size,max_board_size,1)))
        out = out.squeeze()

        pred = np.argmax(out, axis=1).reshape((max_board_size,max_board_size))+1 
        prob = np.around(np.max(out, axis=1).reshape((max_board_size,max_board_size)), 2) 
        
        game = denormalize_array(game,max_number_of_colours).reshape((max_board_size,max_board_size))
        mask = (game==0)
     
        if(mask.sum()==0):
            break
            
        prob_new = prob*mask
    
        ind = np.argmax(prob_new)
        x, y = (ind//max_board_size), (ind%max_board_size)

        val = pred[x][y]
        game[x][y] = val
        game = normalize_array(game,max_number_of_colours)

    pred = pred-1
    return pred

def test_accuracy(feats, labels, model_name):
    correct = 0
    for i,feat in enumerate(feats):
        
        pred = solve_game_sequentially(game=feat,model_name=model_name)
        true = labels[i].reshape((15,15))
        
        if(abs(true - pred).sum()==0):
            correct += 1
        
    return correct/feats.shape[0]

# process_data_for_training()
gpu.limit_gpu()
# train_model(epochs=50,model_name='model_100_epochs2')
x_train, x_test, y_train, y_test, max_val = process_data_for_training()
# solve_game(x_test[0])
# print(solve_game(x_test[0]))
# print(y_train[0].squeeze().reshape(15,15)-1)
# print(denormalize_array(x_train[0],15).reshape(15,15))
print(test_accuracy(x_test[:10],y_test[:10],'model_100_epochs'))