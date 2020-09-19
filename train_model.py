from sklearn.model_selection import train_test_split
from dataParser import parse_files,draw_game_from_2d_array
import numpy as np
import tensorflow as tf
from util import normalize_array,denormalize_array
from tensorflow import keras
import copy
import gpu

def process_data_for_training(max_board_size=15,file_list=[]):
    problems,solutions = parse_files(max_board_size=max_board_size,file_list=file_list)
    features=[]
    labels=[]
    
    features = np.array(problems).reshape(len(problems),max_board_size,max_board_size,1)
    max_val = np.max(problems)  # note we are using 1-indexed colours here
    features = normalize_array(features,max_val)

    labels = np.array(solutions).reshape(len(solutions),max_board_size*max_board_size,1)

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
    model.add(keras.layers.Dense(max_board_size*max_board_size*(max_number_of_colours+1)))
    model.add(keras.layers.Reshape((-1, (max_number_of_colours+1))))
    model.add(keras.layers.Activation('softmax'))
    
    return model

def train_model(epochs=2, model_path='model_1', max_board_size=15, file_list=[]):

    x_train, x_test, y_train, y_test, max_val = process_data_for_training(max_board_size=max_board_size, file_list=file_list)

    model = get_model(max_board_size=max_board_size, max_number_of_colours=max_val)

    adam = keras.optimizers.Adam(lr=.001)
    model.compile(loss='sparse_categorical_crossentropy', optimizer=adam)

    model.fit(x_train, y_train, batch_size=32, epochs=epochs)

    model.save(model_path)

def solve_game_sequentially(game_array,max_board_size=15, max_number_of_colours=15, model_path='model_1'):
    model = keras.models.load_model(model_path)
    sample = copy.copy(game_array)
    while(1):
        out = model.predict(sample.reshape((1,max_board_size,max_board_size,1)))
        out = out.squeeze()

        pred = np.argmax(out, axis=1).reshape((max_board_size,max_board_size))
        prob = np.around(np.max(out, axis=1).reshape((max_board_size,max_board_size)), 3) 
        
        sample = denormalize_array(sample,max_number_of_colours).reshape((max_board_size,max_board_size))
        mask = (sample==0)
     
        if(mask.sum()==0):
            break
            
        prob_new = prob*mask
    
        ind = np.argmax(prob_new)
        x, y = (ind//max_board_size), (ind%max_board_size)

        val = pred[x][y]
        sample[x][y] = val
        sample = normalize_array(sample,max_number_of_colours)

    return sample

def solve_game_by_square(game_array,max_board_size=15, max_number_of_colours=15, model_path='model_1'):
    model = keras.models.load_model(model_path)
    original_game_array = denormalize_array(game_array,max_number_of_colours).reshape(max_board_size,max_board_size)
    
    pred_distribution = model.predict(game_array.reshape((1,max_board_size,max_board_size,1)))
    pred_distribution = pred_distribution.squeeze().reshape(max_board_size,max_board_size,pred_distribution.shape[2])
    predicted_values = np.argmax(pred_distribution,axis=2)

    # don't predict valves
    is_valve = (original_game_array > 0).astype(int)
    prediction = is_valve*original_game_array + predicted_values*(1-is_valve)
    
    print(original_game_array)
    print(prediction)
    return prediction

def test_accuracy(feats, labels, model_path, max_board_size=15, max_number_of_colours=15):
    correct = 0
    for i,feat in enumerate(feats):
        
        pred = solve_game_sequentially(game_array=feat,max_board_size=max_board_size, max_number_of_colours=max_number_of_colours,model_path=model_path)
        true = labels[i].reshape((max_board_size,max_board_size))
        if(abs(true - pred).sum()==0):
            correct += 1
        
    return correct/feats.shape[0]

gpu.limit_gpu()

model_path = 'models\model_five_3'
# train_model(epochs=1000,model_path=model_path,max_board_size=5,file_list=['five.txt','afive.txt'])
x_train, x_test, y_train, y_test, max_val = process_data_for_training(max_board_size=5,file_list=['five.txt','afive.txt'])
# game_array = solve_game_sequentially(x_test[0],max_board_size=5,max_number_of_colours=max_val,model_path=model_path)
# denorm = denormalize_array(x_test[0].squeeze(),max_val)
# print(denorm)
# print(y_test[0].reshape(5,5))
# print(game_array.squeeze())
# game_array = solve_game_by_square(x_test[0],max_board_size=5,max_number_of_colours=max_val+1,model_path=model_path)


acc = test_accuracy(x_train[:10],y_train[:10],model_path,max_board_size=5,max_number_of_colours=max_val)
print(acc)