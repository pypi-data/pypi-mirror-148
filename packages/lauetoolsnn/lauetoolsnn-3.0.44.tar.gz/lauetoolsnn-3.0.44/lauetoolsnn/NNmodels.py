# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 23:04:13 2022

@author: PURUSHOT

NN models and their prediction with numpy based calculations
Keras and tensorflow gets locked for prediction in Multi-thread mode

"""
import numpy as np
import os
## Keras import
tensorflow_keras = True
try:
    import tensorflow as tf
    import keras
    from keras.models import Sequential
    from tensorflow.keras.callbacks import Callback
    from keras.layers import Dense, Activation, Dropout
    from keras.regularizers import l2
    from keras.models import model_from_json
    from tensorflow.keras import Model
    # from tf.keras.layers.normalization import BatchNormalization
except:
    print("tensorflow not loaded; Training and prediction will not work")
    tensorflow_keras = False

import h5py

## GPU Nvidia drivers needs to be installed! Ughh
## if wish to use only CPU set the value to -1 else set it to 0 for GPU
## CPU training is suggested (as the model requires more RAM)
try:
    # Disable all GPUS
    tf.config.set_visible_devices([], 'GPU')
    visible_devices = tf.config.get_visible_devices()
    for device in visible_devices:
        assert device.device_type != 'GPU'
except:
    # Invalid device or cannot modify virtual devices once initialized.
    pass
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

metricsNN = [
            keras.metrics.FalseNegatives(name="fn"),
            keras.metrics.FalsePositives(name="fp"),
            keras.metrics.TrueNegatives(name="tn"),
            keras.metrics.TruePositives(name="tp"),
            keras.metrics.Precision(name="precision"),
            keras.metrics.Recall(name="accuracy"),
            ]

class LoggingCallback(Callback):
    """Callback that logs message at end of epoch.
    """
    def __init__(self, print_fcn, progress_func, qapp, model, fn_model):
        Callback.__init__(self)
        self.print_fcn = print_fcn
        self.progress_func = progress_func
        self.batch_count = 0
        self.qapp = qapp
        self.model = model
        self.model_name = fn_model
    
    def on_batch_end(self, batch, logs={}):
        self.batch_count += 1
        if self.progress_func != None:
            self.progress_func.setValue(self.batch_count)
        if self.qapp != None:
            self.qapp.processEvents()
        
    def on_epoch_end(self, epoch, logs={}):
        msg = "{Epoch: %i} %s" % (epoch, ", ".join("%s: %f" % (k, v) for k, v in logs.items()))
        if self.print_fcn != None:
            self.print_fcn(msg)
        model_json = self.model.to_json()
        with open(self.model_name+".json", "w") as json_file:
            json_file.write(model_json)            
        # serialize weights to HDF5
        self.model.save_weights(self.model_name+"_"+str(epoch)+".h5")
        
def model_arch_general(n_bins, n_outputs, kernel_coeff = 0.0005, bias_coeff = 0.0005, lr=None, verbose=1,
                       write_to_console=None):
    """
    Very simple and straight forward Neural Network with few hyperparameters
    straighforward RELU activation strategy with cross entropy to identify the HKL
    Tried BatchNormalization --> no significant impact
    Tried weighted approach --> not better for HCP
    Trying Regularaization 
    l2(0.001) means that every coefficient in the weight matrix of the layer 
    will add 0.001 * weight_coefficient_value**2 to the total loss of the network
    """
    if n_outputs >= n_bins:
        param = n_bins
        if param*15 < (2*n_outputs): ## quick hack; make Proper implementation
            param = (n_bins + n_outputs)//2
    else:
        # param = n_outputs ## More reasonable ???
        param = n_outputs*2 ## More reasonable ???
        # param = n_bins//2
        
    model = Sequential()
    model.add(keras.Input(shape=(n_bins,)))
    ## Hidden layer 1
    model.add(Dense(n_bins, kernel_regularizer=l2(kernel_coeff), bias_regularizer=l2(bias_coeff)))
    # model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.3)) ## Adding dropout as we introduce some uncertain data with noise
    ## Hidden layer 2
    model.add(Dense(((param)*15 + n_bins)//2, kernel_regularizer=l2(kernel_coeff), bias_regularizer=l2(bias_coeff)))
    # model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.3))
    ## Hidden layer 3
    model.add(Dense((param)*15, kernel_regularizer=l2(kernel_coeff), bias_regularizer=l2(bias_coeff)))
    # model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.3))
    ## Output layer 
    model.add(Dense(n_outputs, activation='softmax'))
    ## Compile model
    if lr != None:
        otp = tf.keras.optimizers.Adam(learning_rate=lr)
        model.compile(loss='categorical_crossentropy', optimizer=otp, metrics=[metricsNN])
    else:
        model.compile(loss='categorical_crossentropy', optimizer="adam", metrics=[metricsNN])
    
    if verbose == 1:
        model.summary()
        stringlist = []
        model.summary(print_fn=lambda x: stringlist.append(x))
        short_model_summary = "\n".join(stringlist)
        if write_to_console!=None:
            write_to_console(short_model_summary)
    return model

def model_arch_CNN_DNN_optimized(shape, 
                                 layer_activation="relu", 
                                 output_activation="softmax",
                                 dropout=0.3,
                                 stride = [1,1],
                                 kernel_size = [5,5],
                                 pool_size=[2,2],
                                 CNN_layers = 2,
                                 CNN_filters = [32,64],
                                 DNN_layers = 3,
                                 DNN_filters = [1000,500,100],
                                 output_neurons = 11,
                                 learning_rate = 0.001,
                                 output="DNN"):            
    inputs = keras.layers.Input(shape, name="InputLayer")
    
    for lay in range(CNN_layers):
        if lay == 0:
            conv1 = keras.layers.Conv1D(filters=CNN_filters[lay], kernel_size=kernel_size[lay], 
                                        strides=stride[lay], 
                                        activation=layer_activation, name="Conv_"+str(lay+1))(inputs)
            pool1 = keras.layers.MaxPooling1D(pool_size=pool_size[lay], \
                                              name="Pool_"+str(lay+1))(conv1)
        else:
            conv1 = keras.layers.Conv1D(filters=CNN_filters[lay], kernel_size=kernel_size[lay], 
                                        strides=stride[lay], 
                                        activation=layer_activation, name="Conv_"+str(lay+1))(pool1)
            pool1 = keras.layers.MaxPooling1D(pool_size=pool_size[lay], \
                                              name="Pool_"+str(lay+1))(conv1)
    flatten = keras.layers.Flatten(name="Flatten")(pool1)

    for lay in range(DNN_layers):
        if lay == 0:
            ppKL = keras.layers.Dense(DNN_filters[lay], activation=layer_activation, \
                                      name="Dense_"+str(lay+1))(flatten)
            ppKL = keras.layers.Dropout(dropout, name="Dropout"+str(lay+1))(ppKL)   
        else:
            
            ppKL = keras.layers.Dense(DNN_filters[lay], activation=layer_activation, \
                                      name="Dense_"+str(lay+1))(ppKL)
            ppKL = keras.layers.Dropout(dropout, name="Dropout"+str(lay+1))(ppKL) 
    ## Output layer 
    if output != "CNN":
        if DNN_layers == 0:
            outputs = keras.layers.Dense(output_neurons, activation=output_activation, name="Dense_out")(flatten)
        else:
            outputs = keras.layers.Dense(output_neurons, activation=output_activation, name="Dense_out")(ppKL)
    else:
        outputs = keras.layers.Conv1D(filters=output_neurons, kernel_size=1, 
                                    strides=1, activation=output_activation, name="Conv_out")(flatten)
    model = Model(inputs, outputs)
    ## Compile model
    otp = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(loss='categorical_crossentropy', optimizer=otp, metrics=[metricsNN])
    model.summary()
    return model

def model_arch_general_optimized(n_bins, n_outputs, kernel_coeff = 0.0005, bias_coeff = 0.0005, lr=None, verbose=1,
                        write_to_console=None):
    """
    Very simple and straight forward Neural Network with few hyperparameters
    straighforward RELU activation strategy with cross entropy to identify the HKL
    Tried BatchNormalization --> no significant impact
    Tried weighted approach --> not better for HCP
    Trying Regularaization 
    l2(0.001) means that every coefficient in the weight matrix of the layer 
    will add 0.001 * weight_coefficient_value**2 to the total loss of the network
    1e-3,1e-5,1e-6
    """
    if n_outputs >= n_bins:
        param = n_bins
        if param*15 < (2*n_outputs): ## quick hack; make Proper implementation
            param = (n_bins + n_outputs)//2
    else:
        param = n_outputs*2 ## More reasonable ???
        
    model = Sequential()
    model.add(keras.Input(shape=(n_bins,)))
    ## Hidden layer 1
    model.add(Dense(n_bins, kernel_regularizer=l2(kernel_coeff), bias_regularizer=l2(bias_coeff)))
    # model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.3)) ## Adding dropout as we introduce some uncertain data with noise
    ## Hidden layer 2
    model.add(Dense(((param)*15 + n_bins)//2, kernel_regularizer=l2(kernel_coeff), bias_regularizer=l2(bias_coeff)))
    # model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.3))
    ## Hidden layer 3
    model.add(Dense((param)*15, kernel_regularizer=l2(kernel_coeff), bias_regularizer=l2(bias_coeff)))
    # model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.3))
    ## Output layer 
    model.add(Dense(n_outputs, activation='softmax'))
    ## Compile model
    if lr != None:
        otp = tf.keras.optimizers.Adam(learning_rate=lr)
        model.compile(loss='categorical_crossentropy', optimizer=otp, metrics=[metricsNN])
    else:
        model.compile(loss='categorical_crossentropy', optimizer="adam", metrics=[metricsNN])
    
    if verbose == 1:
        model.summary()
        stringlist = []
        model.summary(print_fn=lambda x: stringlist.append(x))
        short_model_summary = "\n".join(stringlist)
        if write_to_console!=None:
            write_to_console(short_model_summary)
    return model

def model_arch_general_onelayer(n_bins, n_outputs, 
                                kernel_coeff = 0.0005, 
                                bias_coeff = 0.0005, lr=None, verbose=1,
                                write_to_console=None):
    """
    Very simple and straight forward Neural Network with few hyperparameters
    straighforward RELU activation strategy with cross entropy to identify the HKL
    Tried BatchNormalization --> no significant impact
    Tried weighted approach --> not better for HCP
    Trying Regularaization 
    l2(0.001) means that every coefficient in the weight matrix of the layer 
    will add 0.001 * weight_coefficient_value**2 to the total loss of the network
    1e-3,1e-5,1e-6
    """
    model = Sequential()
    model.add(keras.Input(shape=(n_bins,)))
    ## Hidden layer 1
    model.add(Dense(n_bins, kernel_regularizer=l2(kernel_coeff), bias_regularizer=l2(bias_coeff)))
    # model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.3)) ## Adding dropout as we introduce some uncertain data with noise
    ## Output layer 
    model.add(Dense(n_outputs, activation='softmax'))
    ## Compile model
    if lr != None:
        otp = tf.keras.optimizers.Adam(learning_rate=lr)
        model.compile(loss='categorical_crossentropy', optimizer=otp, metrics=[metricsNN])
    else:
        model.compile(loss='categorical_crossentropy', optimizer="adam", metrics=[metricsNN])
    
    if verbose == 1:
        model.summary()
        stringlist = []
        model.summary(print_fn=lambda x: stringlist.append(x))
        short_model_summary = "\n".join(stringlist)
        if write_to_console!=None:
            write_to_console(short_model_summary)
    return model

def read_hdf5(path):
    weights = {}
    keys = []
    with h5py.File(path, 'r') as f: # open file
        f.visit(keys.append) # append all keys to list
        for key in keys:
            if ':' in key: # contains data if ':' in key
                weights[f[key].name] = f[key][:]
    return weights

def softmax(x):
    return (np.exp(x).T / np.sum(np.exp(x).T, axis=0)).T

def predict_DNN(x, wb, temp_key):
    # first layer
    layer0 = np.dot(x, wb[temp_key[1]]) + wb[temp_key[0]] 
    layer0 = np.maximum(0, layer0) ## ReLU activation
    # Second layer
    layer1 = np.dot(layer0, wb[temp_key[3]]) + wb[temp_key[2]] 
    layer1 = np.maximum(0, layer1)
    # Third layer
    layer2 = np.dot(layer1, wb[temp_key[5]]) + wb[temp_key[4]]
    layer2 = np.maximum(0, layer2)
    # Output layer
    layer3 = np.dot(layer2, wb[temp_key[7]]) + wb[temp_key[6]]
    layer3 = softmax(layer3) ## output softmax activation
    return layer3

def predict_DNN_onelayer(x, wb, temp_key):
    # first layer
    layer0 = np.dot(x, wb[temp_key[1]]) + wb[temp_key[0]] 
    layer0 = np.maximum(0, layer0) ## ReLU activation
    # Second layer
    layer1 = np.dot(layer0, wb[temp_key[3]]) + wb[temp_key[2]] 
    layer3 = softmax(layer1) ## output softmax activation
    return layer3

def predict_CNN_DNN(x, wb, temp_key):
    json_file = open(r"C:\Users\purushot\Desktop\github_version_simple\lauetoolsnn\multi_mat_LaueNN\Zr_alpha_ZrO2_mono\model_Zr_alpha_ZrO2_mono.json", 'r')
    load_weights = r"C:\Users\purushot\Desktop\github_version_simple\lauetoolsnn\multi_mat_LaueNN\Zr_alpha_ZrO2_mono\model_Zr_alpha_ZrO2_mono.h5"
    # # load json and create model
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(load_weights)
    # np.savez_compressed(r"C:\Users\purushot\Desktop\github_version_simple\lauetoolsnn\multi_mat_LaueNN\Zr_alpha_ZrO2_mono\model_Zr_alpha_ZrO2_mono.npz", x, prediction)
    return model.predict(x)


def predict_with_file(x, model_direc=None, material_=None):
    if model_direc!=None and material_!=None:
        if len(material_) > 1:
            prefix_mat = material_[0]
            for ino, imat in enumerate(material_):
                if ino == 0:
                    continue
                prefix_mat = prefix_mat + "_" + imat
        else:
            prefix_mat = material_[0]
        
        json_file = open(model_direc+"//model_"+prefix_mat+".json", 'r')
        load_weights = model_direc + "//model_"+prefix_mat+".h5"
        # # load json and create model
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)
        model.load_weights(load_weights)
        return model.predict(x)

if __name__ == "__main__":
    ## test of numpy prediction
    pass
    # codebar = np.load(r"C:\Users\purushot\Desktop\github_version_simple\lauetoolsnn\multi_mat_LaueNN\Zr_alpha_ZrO2_mono\model_Zr_alpha_ZrO2_mono.npz", allow_pickle=True)["arr_0"]
    # prediction = np.load(r"C:\Users\purushot\Desktop\github_version_simple\lauetoolsnn\multi_mat_LaueNN\Zr_alpha_ZrO2_mono\model_Zr_alpha_ZrO2_mono.npz", allow_pickle=True)["arr_1"]

    # # =============================================================================
    # #     ## keras tensorflow format
    # # =============================================================================
    # json_file = open(r"C:\Users\purushot\Desktop\github_version_simple\lauetoolsnn\multi_mat_LaueNN\Zr_alpha_ZrO2_mono\model_Zr_alpha_ZrO2_mono.json", 'r')
    # load_weights = r"C:\Users\purushot\Desktop\github_version_simple\lauetoolsnn\multi_mat_LaueNN\Zr_alpha_ZrO2_mono\model_Zr_alpha_ZrO2_mono.h5"
    # # # load json and create model
    # loaded_model_json = json_file.read()
    # json_file.close()
    # model = model_from_json(loaded_model_json)
    # model.load_weights(load_weights)
    # prediction1 = model.predict(codebar)
    
    # assert np.all(prediction == prediction1)
    
    # # =============================================================================
    # #     ### Numpy format
    # # =============================================================================
    # wb = read_hdf5(load_weights)
    # temp_key = list(wb.keys())
    
    # # first layer
    # layer0 = np.dot(x, wb[temp_key[1]]) + wb[temp_key[0]] 
    # layer0 = np.maximum(0, layer0) ## ReLU activation
    # # Second layer
    # layer1 = np.dot(layer0, wb[temp_key[3]]) + wb[temp_key[2]] 
    # layer1 = np.maximum(0, layer1)
    # # Third layer
    # layer2 = np.dot(layer1, wb[temp_key[5]]) + wb[temp_key[4]]
    # layer2 = np.maximum(0, layer2)
    # # Output layer
    # layer3 = np.dot(layer2, wb[temp_key[7]]) + wb[temp_key[6]]
    # layer3 = softmax(layer3) ## output softmax activation








